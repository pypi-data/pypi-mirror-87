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


import logging as log
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Optional

from f4ratk.analyze import Analyzer
from f4ratk.data_reader import CsvFileReader
from f4ratk.exchange import Currency, ExchangeReader
from f4ratk.fama import FamaReader, Frequency, Region
from f4ratk.file_reader import FileReader, ValueFormat
from f4ratk.shared import Downsampler, Normalizer, QualityChecker
from f4ratk.ticker import Stock, TickerReader


@dataclass(frozen=True)
class Config:
    stock: Stock
    region: Region


@dataclass(frozen=True)
class FileConfig:
    path: Path
    region: Region
    currency: Currency
    value_format: ValueFormat


def analyze_ticker_symbol(
    config: Config,
    frequency: Frequency,
    start: Optional[date] = None,
    end: Optional[date] = None,
) -> None:
    fama_reader = FamaReader()
    ticker_reader = TickerReader(
        ExchangeReader(frequency), Normalizer(), Downsampler(), QualityChecker()
    )
    analyzer = Analyzer()

    analyzer.analyze(
        ticker_reader.data(config.stock, frequency, start, end),
        fama_reader.fama_data(region=config.region, frequency=frequency),
    )


def analyze_file(
    config: FileConfig,
    frequency: Frequency,
    start: Optional[date] = None,
    end: Optional[date] = None,
) -> None:
    fama_reader = FamaReader()
    file_reader = FileReader(
        csv_reader=CsvFileReader(path=config.path),
        exchange_reader=ExchangeReader(frequency),
        currency=config.currency,
        value_format=config.value_format,
    )

    analyzer = Analyzer()

    analyzer.analyze(
        file_reader.read(start, end, frequency=frequency),
        fama_reader.fama_data(region=config.region, frequency=frequency),
    )


def configure_logging(verbose: bool) -> None:
    log.basicConfig(level=log.DEBUG if verbose else log.INFO)
    log.getLogger("urllib3").setLevel(log.INFO)
