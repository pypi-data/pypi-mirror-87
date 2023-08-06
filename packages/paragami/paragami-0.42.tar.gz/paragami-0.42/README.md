# "Parameter origami": `paragami`.

[![image](https://travis-ci.org/rgiordan/paragami.svg?branch=master)](https://travis-ci.org/rgiordan/paragami)
[![image](https://codecov.io/gh/rgiordan/paragami/branch/master/graph/badge.svg)](https://codecov.io/gh/rgiordan/paragami)

## Description.

Parameter folding and flattening, parameter origami: `paragami`\*!

This is a library (very much still in development) intended to make
sensitivity analysis easier for optimization problems. The core
functionality consists of tools for "folding" and "flattening"
collections of parameters -- i.e., for converting data structures of
constrained parameters to and from vectors of unconstrained parameters.

For background and motivation, see the following papers:

Covariances, Robustness, and Variational Bayes
Ryan Giordano, Tamara Broderick, Michael I. Jordan
<https://arxiv.org/abs/1709.02536>

A Swiss Army Infinitesimal Jackknife
Ryan Giordano, Will Stephenson, Runjing Liu, Michael I. Jordan, Tamara
Broderick
<https://arxiv.org/abs/1806.00550>

Evaluating Sensitivity to the Stick Breaking Prior in Bayesian
Nonparametrics
Runjing Liu, Ryan Giordano, Michael I. Jordan, Tamara Broderick
<https://arxiv.org/abs/1810.06587>

## Using the package.

We welcome new users\! However, please be aware that the package is
still in development. We encourage users to contact the author (github
user `rgiordan`) for advice, bugs, or if you're using the package for
something important.

### Installation.

To install the latest tagged version, install with `pip`:

`python3 -m pip install paragami`.

The `paragami` package is under rapid development, so you may want to
clone the respository and use the master branch instead.

**Note**: In order to use the functions in
`sparse_preconditioners_lib`, you must additionally manually install
[``scikit-sparse``](https://github.com/scikit-sparse/scikit-sparse/),
which requires the C++ libraries in ``libsuitesparse-dev``.
Most users will not require this functionality so `scikit-sparse` is not installed by default with `paragami` for simplicity.  See the
[``scikit-sparse`` requirements](https://scikit-sparse.readthedocs.io/en/latest/overview.html#requirements)
for more details on installation.

### Documentation and Examples.

For examples and API documentation, see
[readthedocs](https://paragami.readthedocs.io/).

Alternatively, check out the repo and run `make html` in `docs/`.

\*  Thanks to Stéfan van der Walt for the suggesting the package name.
