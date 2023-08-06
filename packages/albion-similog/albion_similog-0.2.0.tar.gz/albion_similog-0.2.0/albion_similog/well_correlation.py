"""Well correlation using FAMSA algorithm, originally developped in biological studies. For more
details, see https://github.com/refresh-bio/FAMSA.

"""

import os
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from pychangepoints.algo_changepoints import pelt
from skbio import read
from skbio.alignment import TabularMSA
from skbio.sequence import Protein
from sklearn import linear_model, preprocessing

from albion_similog.log import setup_logger


logger = setup_logger(__name__)

PROJECT_DIR = Path(os.path.dirname(os.path.realpath(__file__))).parent
FAMSA_PATH = PROJECT_DIR / "famsa-workdir"
FAMSA_PATH.mkdir(exist_ok=True)


# Classical DNA alphabet, used for dataseries transcription
DNA_ALPHABET_SEQUENCE = [
    "A",
    "R",
    "N",
    "D",
    "C",
    "Q",
    "E",
    "G",
    "H",
    "I",
    "L",
    "K",
    "M",
    "F",
    "P",
    "S",
    "T",
    "W",
    "Y",
    "V",
    "B",
    "Z",
    "X",
]


def pelt_ordered_indices(data, min_seg, pen=1e-3):
    """Produce segmentation indices using PELT algorithm.

    See more details on the related R documentation of this method:
    https://www.rdocumentation.org/packages/changepoint/versions/2.2.2/topics/PELT.

    Parameters
    ----------
    data : pd.DataFrame
        Data on which PELT algorithm must be run to find changepoints
    min_seg : int
        Minimum segment length (number of observations between changes)
    pen : float
        TODO
    """
    if pen < 1e-3:
        logger.warning(
            "Such a small value for 'pen' (%s) is probably not a good idea.", pen
        )
    indices, _ = pelt(data, pen, min_seg, "mll_mean")
    return np.sort(indices) - 1


def compute_mean_segmentation(vector, indices):
    """Aggregate the data contained in vector following the provided indices sequence. The resulting
    structure is a numpy array containing mean values of subsequence of the input vector.

    For example, if indices is [0, 10, 20, ...], the function produces an array that contains the
    mean over values of index 0 to 10 in the input vector, then the mean over values of index 10 to
    20 in this input vector, and so on.

    If indices is a list of values from 0 to len(vector), the function returns vector.

    Parameters
    ----------
    vector : np.array
        Data that has to be aggregated
    indices : np.array
        Aggregation indices
    Results
    -------
    np.array
        Aggregated data

    """
    assert np.all([idx < len(vector) for idx in indices])
    return np.array(
        [np.mean(vector[indices[j] : indices[j + 1]]) for j in range(len(indices) - 1)]
    )


def custom_SAX(data, thresholds, vect_alphabet):
    """Transcribe a dataseries into a list of letters defined in the given alphabet.

    Parameters
    ----------
    data : pd.Series
    thresholds : np.array
        List of thresholds that aim at subdivising the raw data series
    vect_alphabet : list
        Alphabet of reference, must contain at least as many items than thresholds

    Results
    -------
    str
        An encoded version of the input data, as a sequence of characters coming from the alphabet
    """
    resultat = ""
    for j in data:
        indice = 0
        vect_limit = np.concatenate((np.array([-1e8]), np.append(thresholds, 1e8)))
        while j > vect_limit[indice]:
            indice = indice + 1
        resultat += vect_alphabet[indice - 1]
    return resultat


class WellCorrelation:
    """WellCorrelation class."""

    def __init__(
        self,
        data_log,
        match_column="ILD",
        depth_column="MD",
        well_column="API",
        min_seg=1,
        pelt_sup=0.2,
        depth_min=10,
        depth_max=200,
        value_min=0,
        value_max=1000,
        quantile_list=(0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9),
        log_normalize=True,
        lr_normalize=True,
        segmentize_with_pelt=False,
    ):
        """Initialization method.

        Class attributes are initialized. For each well, one also writes raw and aggregated
        dataseries, as well as a segmentation sequence.

        Parameters
        ----------
        data_log : pd.DataFrame
            Raw log data, that provides a measure value for a range of depths, for a given set of
            wells.
        match_column : str
            Name of the column that contains measure values
        depth_column : str
            Name of the column that contains depth information
        well_column : str
            Name of the column that contains well identifiers
        depth_min : float
            Minimal depth from which data is considered, in a strict inequality scheme
        depth_max : float
            Maximal depth from which data is considered, in a strict inequality scheme
        value_min : float
            Lower threshold for measures, in a strict inequality scheme (default to 0: do not
            consider negative/null values)
        value_max : float
            Upper threshold for measures, in a strict inequality scheme (default to 1000: consider
            values strictly smaller than 1000)
        min_seg : int
            Positive integer giving the minimum segment length (number of observations between
            changes) ; used in PELT algorithm if ``segmentize_with_pelt`` is True, in a linear
            aggregation procedure otherwise
        pelt_sup : float
            Penalty term applied to the PELT procedure, when computing optimal consensus indices
        quantile_list : tuple
            Global quantiles used in order to discriminate log dataseries. By default, one adds
            0.01 and 0.975 as extrem quantile values. This sequence must contain 22 values at most,
            so as to fit the DNA sequence length.
        log_normalize : bool
            If True, log normalize the measure values at initialization.
        lr_normalize : bool
            If True, a linear regression over values at quantiles (see ``quantiles_list``) is done
            for each well, before transcribing measure values in DNA.
        segmentize_with_pelt : bool
            If True, the segmentation indices are computed with PELT algorithm at
            initialization. Otherwise a linear aggregation depending on ``min_seg`` is used.

        """
        self.match_column = match_column
        self.depth_column = depth_column
        self.min_seg = min_seg
        self.pelt_sup = pelt_sup
        self.quantiles_list = quantile_list
        self.lr_normalize = lr_normalize

        self.__PENALTY_PELT = int(1e-8)
        self.__CONSENSUS_per = 0.5

        # Reference log value associated to each alphabet item
        self.value_alphabet = pd.DataFrame({"alphabet": [], "quantile": []})
        # Well log sequence, as a list of Bio.SeqRecord.SeqRecord
        self.sequence_logs = []
        # Well log multi-sequence alignment, as a skbio.TabularMSA
        self.multi_sequence_alignment = TabularMSA("")
        # Dictionnary matching the letter in the alignment with the depth for each well
        self.depth_match_global = {}
        # Consensus
        self.consensus = pd.DataFrame(
            {self.match_column: [], self.depth_column: [], "freq": []}
        )
        # Markers
        self.markers = pd.DataFrame(
            {self.depth_column: [], "marker_name": [], "hole_id": []}
        )

        # For each well of the site of interest, compute normalized version of data series
        # The normalization is done by considering local mean values, depending on:
        # - the PELT algorithm (fancy version), see pelt, __PENALTY_PELT and min_seg attributes
        # - or on a fixed step (simple version), see min_seg attribute
        self.dict_data = {}
        self.dict_data_original = {}
        self.dict_segmentation = {}
        for idx_well, well_data in data_log.groupby(well_column):

            well_name = str(well_data[well_column].iloc[0])
            well_data.set_index(self.depth_column, inplace=True)
            well_data = well_data.loc[
                (depth_min < well_data.index)
                & (well_data.index < depth_max)
                & (value_min < well_data[self.match_column])
                & (well_data[self.match_column] < value_max)
            ].copy()
            well_data.dropna(inplace=True)
            # Depending on log_normalize parameter, consider logarithmic values
            if log_normalize:
                well_data[self.match_column] = np.log(well_data[self.match_column])
            # Define the raw data series for this well
            self.dict_data_original[well_name] = well_data

            # If pelt is True, this algorithm is run to extract segmentation sequence
            if segmentize_with_pelt:
                scaled_data = pd.DataFrame(
                    preprocessing.scale(well_data[[self.match_column]])
                )
                seg_match_small = pelt_ordered_indices(
                    scaled_data, self.__PENALTY_PELT, self.min_seg
                )
            # Otherwise, one uses a regular sampling sequence
            else:
                seg_match_small = np.arange(
                    0, len(well_data[[self.match_column]]), self.min_seg
                ).astype(int)
            self.dict_segmentation[well_name] = seg_match_small

            # Compute the normalized version of dataseries, knowing the segmentation sequence
            mean_query = compute_mean_segmentation(
                well_data[[self.match_column]].values, seg_match_small
            )
            # Define the preprocess data series for this well
            self.dict_data[well_name] = pd.DataFrame({self.match_column: (mean_query)})

    @property
    def sequence_filepath(self):
        return FAMSA_PATH / "short_seqs.fasta"

    @property
    def famsa_output_filepath(self):
        return FAMSA_PATH / "result_famsa.fasta"

    @property
    def vect_alphabet(self):
        return DNA_ALPHABET_SEQUENCE[: 1 + len(self.quantiles_list)]

    def run(self):
        """Run the full well correlation pipeline so as to generate consensus logs and markers for each
        well

        """
        self.prepare_logs()
        self.run_famsa()
        self.compute_depth_match()
        self.compute_consensus()
        self.compute_markers(self.tops_algn_position)

    def prepare_logs(self):
        """Prepare data logs: starting from segmented version of dataseries for each well, generate letter
        sequences and serialize them on the file system, as a fasta-formatted file.

        This method also defines a custom alphabet definition for each well, by associating each
        letter with a data quantiles.

        """
        if self.sequence_filepath.is_file():
            self.sequence_filepath.unlink()
        # Concatenate the normalized data and generate the quantiles of the resulting series
        all_squared_data = pd.concat(
            [dd[self.match_column] for _, dd in self.dict_data.items()]
        ).reset_index(drop=True)
        global_quantiles = all_squared_data.quantile(self.quantiles_list).values

        # The quantile vector is redefined with extrem quantiles.
        # From now one considers the center of each histogram class.
        extended_quantiles = np.concatenate(
            [
                np.array([all_squared_data.quantile(0.01)]),
                global_quantiles,
                np.array([all_squared_data.quantile(0.975)]),
            ]
        )
        global_quantiles_vect_value = (
            np.diff(extended_quantiles) / 2 + extended_quantiles[:-1]
        )
        self.value_alphabet = pd.DataFrame(
            {"alphabet": self.vect_alphabet, "quantile": global_quantiles_vect_value}
        ).set_index("alphabet")

        # Prepare RNA sequence logs
        # One first initializes a linear regression model
        lr = linear_model.LinearRegression()

        # For each well (and corresponding data), transcribe the dataseries with reference alphabet
        for key, well in self.dict_data.items():

            # If normalize is True, a normalized version of values are generated
            # using a linear regression over quantiles
            if self.lr_normalize:
                lr.fit(
                    well[self.match_column]
                    .quantile(self.quantiles_list)
                    .values.reshape(-1, 1),
                    global_quantiles.reshape(-1, 1),
                )
                well[self.match_column + "_norm"] = lr.predict(
                    well[[self.match_column]]
                )
            else:
                well[self.match_column + "_norm"] = well[[self.match_column]]

            sequence = custom_SAX(
                well[self.match_column + "_norm"],
                global_quantiles,
                self.vect_alphabet,
            )
            self.sequence_logs.append(SeqRecord(Seq(sequence), id=key, description=key))
        # Write sequences on a fasta file
        SeqIO.write(self.sequence_logs, self.sequence_filepath, "fasta")

    def run_famsa(self):
        """Run the FAMSA program in order to generate multi aligned sequences of log measures

        This method calls the FAMSA program, a non-Python dependencies that should be installed at
        the root of the albion_similog Python library.

        """
        # If famsa output file exists on the file system, remove it
        if self.famsa_output_filepath.is_file():
            self.famsa_output_filepath.unlink()
        # Run FAMSA program starting from the previously generated sequence file
        if not self.sequence_filepath.is_file():
            logger.info(
                "Input fasta sequence file (%s) does not exist, let's prepare it...",
                self.sequence_filepath,
            )
            self.prepare_logs()
        logger.info("Run FAMSA program on %s.", self.sequence_filepath)
        subprocess.call(
            [
                str(PROJECT_DIR / "famsa"),
                "-go",
                "20",
                "-ge",
                "5",
                "-r",
                "100",
                str(self.sequence_filepath),
                str(self.famsa_output_filepath),
            ]
        )
        # Import alignment
        self.multi_sequence_alignment = read(
            str(FAMSA_PATH / "result_famsa.fasta"),
            format="fasta",
            into=TabularMSA,
            constructor=Protein,
        )

    def compute_depth_match(self):
        """Compute the matching dictionary that links raw logs with segmentation indices computed during
        class initialization

        """
        # Set depth match global for each well
        self.df_align = {}
        for key, data in self.dict_data_original.items():
            # Extract DNA sequences as strings for each well
            sequence = [
                str(protein)
                for protein in self.multi_sequence_alignment
                if protein.metadata["id"] == key
            ]
            assert len(sequence) == 1
            global_align = np.array([item for item in sequence[0]])
            # Produce a DataFrame with the sequence, and generate smart indices
            df_align = pd.DataFrame({"letter": global_align})
            mask = df_align["letter"] != "-"
            df_align.loc[mask, "indices"] = np.arange(df_align[mask].shape[0])
            df_align.loc[0, "indices"] = 0
            df_align["indices"] = (
                df_align["indices"].fillna(method="ffill").astype("int")
            )
            self.df_align[key] = df_align["indices"].values
            # Here one gets non-empty letter indices,
            # one builds depth_match_global item starting from raw data
            seg_match = self.dict_segmentation[key][df_align["indices"].values]
            self.depth_match_global[key] = np.array(data.index[seg_match])

    def compute_consensus(self):
        """Compute the consensus log, which is a "mean" log that aggregates the logs from every well. This
        method also sets the value of tops_algn_position, which represents a raw marker set

        This method calls the PELT algorithm, developed in pychangepoints dependency.
        """
        # Prepare a DataFrame version of the alignment, with wells as indices
        df_msa = pd.DataFrame(self.multi_sequence_alignment.to_dict())
        df_msa.loc[:] = df_msa.values.astype(str)
        df_msa.columns = [
            protein.metadata["id"] for protein in self.multi_sequence_alignment
        ]
        # Compute letter frequency, for each position of the dataseries
        freq_df = df_msa.apply(pd.value_counts, axis=1)
        letter_frequency = freq_df[self.vect_alphabet].sum(axis=1)
        # Building consensus series: an index belongs to the consensus
        # if there is data on a significative (see __CONSENSUS_per attribute) part of wells
        mask_consensus = letter_frequency > (1 - self.__CONSENSUS_per) * df_msa.shape[1]
        consensus = (
            freq_df.drop(columns="-").fillna(0).dot(self.value_alphabet["quantile"])
            / letter_frequency
        )
        self.consensus = pd.DataFrame(
            {
                self.match_column: np.repeat(consensus[mask_consensus], self.min_seg),
                self.depth_column: np.linspace(
                    0, mask_consensus.sum() - 1, mask_consensus.sum()
                )
                / 10,
                "freq": np.repeat(
                    letter_frequency[mask_consensus] / df_msa.shape[1], self.min_seg
                ),
            }
        )
        self.consensus.set_index(self.depth_column, inplace=True)
        self.index_global_consensus = consensus[mask_consensus].index.values
        # Segmentize the consensus log to build the chronicle of aligned tops
        scaled_data = pd.DataFrame(
            preprocessing.scale(self.consensus[self.match_column])
        )
        seg_signal = pelt_ordered_indices(scaled_data, 2, self.pelt_sup)
        self.tops_algn_position = np.unique(
            self.index_global_consensus[seg_signal // self.min_seg]
        ).astype(int)

    def extract_top_indices(self, tops):
        """Given a list of depth positions, compute the corresponding indices in the consensus log. This
        function aims at providing a valid input parameter for ``compute_markers`` method.

        If the input list contains values that are not in consensus depth axis, these values are
        not considered.

        Parameters
        ----------
        tops : list
            Depths on the consensus log for which markers have to be expanded on the regular well
            logs

        """
        mask = self.consensus.index.isin(tops)
        idx_consensus = self.consensus.reset_index().loc[mask].index
        return self.index_global_consensus[idx_consensus]

    def compute_markers(self, aligned_positions):
        """Compute the final state of markers associated to the well set

        Parameters
        ----------
        aligned_positions : np.array
            Index on the consensus log taken as references for marker generation
        """
        # Finding the consensus marker for each well
        list_tops = []
        for key in self.dict_data:
            tops_current = self.depth_match_global[key][aligned_positions]
            # Filter duplicated values at the beginning of the marker chronicle
            m_tot = len(tops_current) - 1
            i_j = 1
            while (i_j < m_tot) & (tops_current[i_j] == tops_current[0]):
                i_j += 1
            # Filter duplicated values at the end of the marker chronicle
            j_i = m_tot - 1
            while (j_i > 1) & (tops_current[j_i] == tops_current[m_tot]):
                j_i = j_i - 1
            df_current = pd.DataFrame(
                {
                    "hole_id": key,
                    "from": tops_current[(i_j - 1) : (j_i + 2)],
                    "to": tops_current[(i_j - 1) : (j_i + 2)] + 0.1,
                    "code": np.arange(i_j - 1, j_i + 2),
                }
            )
            list_tops.append(df_current)
        self.markers = pd.concat(list_tops, ignore_index=True)
