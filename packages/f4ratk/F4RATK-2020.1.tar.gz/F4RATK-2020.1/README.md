# F4RATK

[![Build status](https://img.shields.io/appveyor/build/toroettg/f4ratk)](https://ci.appveyor.com/project/toroettg/f4ratk)
[![License: AGPL](https://img.shields.io/badge/License-AGPL--3.0--only-informational.svg)](https://spdx.org/licenses/AGPL-3.0-only.html)

A Fama/French Finance Factor Regression Analysis Toolkit.

## Here be dragons

This project is experimental: it does not provide any guarantees and its
results are not rigorously tested. It should not be used by itself as a
basis for decision‐making.

If you would like to join, please see [CONTRIBUTING] for guidelines.

## Quickstart

### Installation

Obtain the latest released version of F4RATK using pip:

`pip install f4ratk`

### Usage

Run the program to see an interactive help. Note that each listed
command also provides an individual help.

`f4ratk --help`

```lang-none
Usage: f4ratk [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --verbose  Increases output verbosity.
  --help         Show this message and exit.

Commands:
  file    Analyze data of a CSV file.
  ticker  Analyze data for a ticker symbol.

```

Adjust the program arguments according to your problem.
Then run your regression analysis similar to the following.

#### Examples

```lang-sh
f4ratk ticker USSC.L US USD
f4ratk file ./input.csv DEVELOPED EUR PRICE --frequency=MONTHLY

```

## License

This project is licensed under the GNU Affero General Public License
version 3 (only). See [LICENSE] for more information and [COPYING]
for the full license text.

## Notice

Based on the works of [Rand Low] and [DD].

[CONTRIBUTING]: https://codeberg.org/toroettg/F4RATK/src/branch/main/CONTRIBUTING.md
[LICENSE]: https://codeberg.org/toroettg/F4RATK/src/branch/main/LICENSE
[COPYING]: https://codeberg.org/toroettg/F4RATK/src/branch/main/COPYING

[Rand Low]: https://randlow.github.io/posts/finance-economics/asset-pricing-regression
[DD]: https://www.codingfinance.com/post/2019-07-01-analyze-ff-factor-python
