# Albion Similog

This project is dedicated to the generation of possible edges within the
[Albion](https://gitlab.com/Oslandia/albion) framework, through the way of
[FAMSA](https://github.com/refresh-bio/FAMSA) algorithm.

`albion_similog` works with Python3.8.

## Installation

### Dependencies

This package works with a few dependencies from the biology ecosystem, like `biopython` or
`scikit-bio`. They are installable easily through `pip`.

There is a notable exception with `FAMSA`, that should be patched for specific Albion purpose, and
compiled. Everything is managed through the `Makefile`.

### Debian/Ubuntu

```
$ virtualenv .venv
$ source .venv/bin/activate
(.venv) $ make install
```

### Windows

TODO
