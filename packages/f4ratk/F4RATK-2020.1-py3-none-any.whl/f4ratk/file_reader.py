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

from datetime import date
from enum import Enum, unique

from pandas import DataFrame, merge

from f4ratk.data_reader import CsvFileReader
from f4ratk.exchange import Currency, ExchangeReader
from f4ratk.fama import Frequency


@unique
class ValueFormat(Enum):
    PRICE = 'Prices'
    RETURN = 'Returns'


class FileReader:
    def __init__(
        self,
        csv_reader: CsvFileReader,
        exchange_reader: ExchangeReader,
        currency: Currency,
        value_format: ValueFormat,
    ):
        self._csv_reader = csv_reader
        self._exchange_reader = exchange_reader
        self._currency = currency
        self._value_format = value_format

    def read(
        self, start: date = None, end: date = None, frequency=Frequency.DAILY
    ) -> DataFrame:
        data = self._csv_reader.read().sort_index()

        data = self._convert_index_to_periods(data, frequency=frequency)

        if self._currency is not Currency.USD:
            data = self._convert_currency(
                data=data, currency=self._currency, start=start, end=end
            )

        if self._value_format == ValueFormat.PRICE:
            data = data[['Returns']].pct_change() * 100

        return data.dropna()

    def _convert_currency(
        self, data: DataFrame, currency: Currency, start: date, end: date
    ) -> DataFrame:
        exchange_data = self._exchange_reader.exchange_data(currency, start, end)

        data = merge(data, exchange_data, left_index=True, right_index=True)

        data['Returns'] = data['Returns'] * data[ExchangeReader.EXCHANGE_RATE_COLUMN]

        return data[['Returns']]

    def _convert_index_to_periods(
        self, data: DataFrame, frequency: Frequency
    ) -> DataFrame:
        frequency_label = self._to_frequency_label(frequency)
        return data.to_period(freq=frequency_label)

    def _to_frequency_label(self, frequency: Frequency) -> str:
        if frequency == Frequency.DAILY:
            return 'B'
        elif frequency == Frequency.MONTHLY:
            return 'M'

        raise NotImplementedError
