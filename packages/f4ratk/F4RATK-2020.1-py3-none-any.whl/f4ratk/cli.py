##############################################################################
# Copyright (C) 2020 Tobias Röttger <dev@roettger-it.de>
#
# This file is part of F4RATK.
#
# F4RATK is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License version 3
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
##############################################################################

from datetime import date, datetime
from pathlib import Path
from typing import Optional

from click import Choice, DateTime, Path as PathArg, argument, group, option

from f4ratk.exchange import Currency
from f4ratk.f4ratk import (
    Config,
    FileConfig,
    analyze_file,
    analyze_ticker_symbol,
    configure_logging,
)
from f4ratk.fama import Frequency, Region
from f4ratk.file_reader import ValueFormat
from f4ratk.ticker import Stock


class Date(DateTime):
    name = "date"

    def __init__(self, formats=None):
        formats = formats or ["%Y-%m-%d"]
        super().__init__(formats)

    def convert(self, value, param, ctx):
        date: Optional[datetime] = super().convert(value, param, ctx)
        return date.date() if date else None

    def __repr__(self):
        return 'Date'


@group()
@option('-v', '--verbose', is_flag=True, help="Increases output verbosity.")
def cli(verbose: bool):
    configure_logging(verbose)


@cli.command(name="ticker", help="Analyze data for a ticker symbol.")
@argument('symbol')
@argument('region', type=Choice(('DEVELOPED', 'US', 'EU'), case_sensitive=False))
@argument('currency', type=Choice(('USD', 'EUR'), case_sensitive=False))
@option(
    '--start', type=Date(formats=('%Y-%m-%d',)), help="Start of period under review."
)
@option('--end', type=Date(formats=('%Y-%m-%d',)), help="End of period under review.")
@option(
    '--frequency',
    type=Choice(('DAILY', 'MONTHLY'), case_sensitive=False),
    default='DAILY',
    show_default=True,
    help="Conduct analysis with given sample frequency.",
)
def stock_cli(
    symbol: str,
    currency: str,
    region: str,
    start: Optional[date],
    end: Optional[date],
    frequency: str = 'DAILY',
):
    config = Config(
        stock=Stock(ticker_symbol=symbol, currency=Currency[currency]),
        region=Region[region],
    )

    analyze_ticker_symbol(
        config=config, frequency=Frequency[frequency], start=start, end=end
    )


@cli.command(
    name="file",
    short_help="Analyze data of a CSV file.",
    help="""
         Analyze data of a CSV file.

         Expects a row to be formatted in ISO 8601 with optional day for monthly input
         at the first column; and percentage in US notation with arbitrary-precision
         decimal number value at the second column, where the value may represent
         either prices or returns in percentage:

         'YYYY-MM[-DD],####.####', e.g.,

         '2020-09-11,3.53'
         '2020-09,-0.282'
         """,
)
@argument('path', type=PathArg(dir_okay=False))
@argument('region', type=Choice(('DEVELOPED', 'US', 'EU'), case_sensitive=False))
@argument('currency', type=Choice(('USD', 'EUR'), case_sensitive=False))
@argument('value_format', type=Choice(('PRICE', 'RETURN'), case_sensitive=False))
@option(
    '--start', type=Date(formats=('%Y-%m-%d',)), help="Start of period under review."
)
@option('--end', type=Date(formats=('%Y-%m-%d',)), help="End of period under review.")
@option(
    '--frequency',
    type=Choice(('DAILY', 'MONTHLY'), case_sensitive=False),
    default='DAILY',
    show_default=True,
    help="Conduct analysis with given sample frequency.",
)
def file_cli(
    path: str,
    currency: str,
    region: str,
    value_format: ValueFormat,
    start: Optional[date],
    end: Optional[date],
    frequency: str = 'DAILY',
):
    config = FileConfig(
        path=Path(path),
        region=Region[region],
        currency=Currency[currency],
        value_format=ValueFormat[value_format],
    )

    analyze_file(config=config, frequency=Frequency[frequency], start=start, end=end)
