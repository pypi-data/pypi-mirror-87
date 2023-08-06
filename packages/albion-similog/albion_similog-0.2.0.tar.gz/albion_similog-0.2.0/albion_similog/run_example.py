import argparse
from pathlib import Path

from albion_similog.log import setup_logger
from albion_similog.prepare_data import read_and_prepare_data
from albion_similog.well_correlation import WellCorrelation


logger = setup_logger(__name__)


def valid_path(path_str):
    """Produces a ``pathlib.Path``` object that corresponds to folder ``path_str``.

    Parameters
    ----------
    path_str : str
        Input path as a string.

    Returns
    -------
    pathlib.Path
        Input path as a ``pathlib.Path``.
    """
    path_ = Path(path_str)
    if not path_.is_dir() and not path_.is_file():
        msg = 'Le chemin "{}" n\'existe pas'.format(str(path_))
        raise argparse.ArgumentTypeError(msg)
    return path_.resolve()


def run(data, outputdir, experiment=None):
    """Run well correlation algorithm

    Parameters
    ----------
    data : pandas.DataFrame
        Input data for the algorithm.
    outputdir : pathlib.Path
        Path to the folder where the output files must be saved.
    experiment : str
        Name of the experiment, to distinguish the output files.
    """
    algo_corr = WellCorrelation(
        data,
        match_column="ILD",
        depth_column="MD",
        well_column="API",
        depth_min=10,
        depth_max=200,
        min_seg=1,
        pelt_sup=0.2,
        lr_normalize=True,
        segmentize_with_pelt=False,
    )
    algo_corr.run()
    logger.info("Save the results...")
    suffix = ""
    if experiment is not None:
        suffix = "_" + experiment
    consensus_batch_filepath = outputdir / ("consensus_batch" + suffix + ".csv")
    algo_corr.consensus.to_csv(consensus_batch_filepath)
    tops_unsupervised_filepath = outputdir / ("tops_unsupervised" + suffix + ".csv")
    algo_corr.markers.to_csv(tops_unsupervised_filepath, index=False)
    logger.info("End of the procedure.")


def main(args):
    """Main procedure.

    Parameters
    ----------
    args : argparse.Namespace
        Arguments of the procedure.
    """
    df = read_and_prepare_data(args.inputfile)
    run(df, args.outputdir, args.experiment)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog="similog",
        description="Compute consensus log from FAMSA algorithm",
    )
    sub_parsers = parser.add_subparsers(dest="command")
    parser.add_argument(
        "-e",
        "--experiment",
        help="Name of the experiment (used as a suffix in output file names",
    )
    parser.add_argument(
        "-i",
        "--inputfile",
        required=True,
        type=valid_path,
        help="Path towards the input data file",
    )
    parser.add_argument(
        "-o",
        "--outputdir",
        default=valid_path("output"),
        type=valid_path,
        help="Path towards the output directory",
    )
    args = parser.parse_args()
    main(args)
