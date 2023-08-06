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
from enum import Enum, unique

import pandas
from pandas import DataFrame, DatetimeIndex

from f4ratk.data_reader import fama_french_reader


@unique
class DataSource(Enum):
    DEVELOPED_5_DAILY = 'Developed_5_Factors_Daily'
    DEVELOPED_5_MONTHLY = 'Developed_5_Factors'

    DEVELOPED_MOM_DAILY = 'Developed_Mom_Factor_Daily'
    DEVELOPED_MOM_MONTHLY = 'Developed_Mom_Factor'

    US_5_DAILY = 'F-F_Research_Data_5_Factors_2x3_daily'
    US_5_MONTHLY = 'F-F_Research_Data_5_Factors_2x3'

    US_MOM_DAILY = 'F-F_Momentum_Factor_daily'
    US_MOM_MONTHLY = 'F-F_Momentum_Factor'

    EU_5_DAILY = 'Europe_5_Factors_Daily'
    EU_5_MONTHLY = 'Europe_5_Factors'

    EU_MOM_DAILY = 'Europe_Mom_Factor_Daily'
    EU_MOM_MONTHLY = 'Europe_Mom_Factor'


@unique
class Region(Enum):
    DEVELOPED = 'Developed'
    EU = 'Europe'
    US = 'United States'


@unique
class Frequency(Enum):
    DAILY = 'Daily'
    MONTHLY = 'Monthly'


class FamaReader:
    def fama_data(self, region: Region, frequency: Frequency) -> DataFrame:
        if region == Region.DEVELOPED:
            if frequency == Frequency.DAILY:
                return self._fama_data(
                    frequency,
                    DataSource.DEVELOPED_5_DAILY,
                    DataSource.DEVELOPED_MOM_DAILY,
                )
            elif frequency == Frequency.MONTHLY:
                return self._fama_data(
                    frequency,
                    DataSource.DEVELOPED_5_MONTHLY,
                    DataSource.DEVELOPED_MOM_MONTHLY,
                )
        elif region == Region.US:
            if frequency == Frequency.DAILY:
                return self._fama_data(
                    frequency, DataSource.US_5_DAILY, DataSource.US_MOM_DAILY
                )
            elif frequency == Frequency.MONTHLY:
                return self._fama_data(
                    frequency, DataSource.US_5_MONTHLY, DataSource.US_MOM_MONTHLY
                )
        elif region == Region.EU:
            if frequency == Frequency.DAILY:
                return self._fama_data(
                    frequency, DataSource.EU_5_DAILY, DataSource.EU_MOM_DAILY
                )
            elif frequency == Frequency.MONTHLY:
                return self._fama_data(
                    frequency, DataSource.EU_5_MONTHLY, DataSource.EU_MOM_MONTHLY
                )

        raise NotImplementedError

    def _fama_data(
        self,
        frequency: Frequency,
        source: DataSource,
        momentum_source: DataSource = None,
    ) -> DataFrame:
        data_ff = self._fama_ff_data(source, frequency)
        data_mom = (
            self._fama_momentum_data(momentum_source, frequency)
            if momentum_source
            else DataFrame()
        )

        data: DataFrame = pandas.merge(
            data_ff, data_mom, left_index=True, right_index=True
        )

        log.debug(f"Fama data of set '{source}' ends at\n%s", data.tail())

        return data

    def _fama_ff_data(self, source: DataSource, frequency: Frequency) -> DataFrame:
        data = self._load_fama_data(source, frequency)
        data.rename(columns={'Mkt-RF': 'MKT'}, inplace=True)
        return data

    def _fama_momentum_data(
        self, source: DataSource, frequency: Frequency
    ) -> DataFrame:
        data: DataFrame = self._load_fama_data(source, frequency)

        if source == DataSource.US_MOM_DAILY or source == DataSource.US_MOM_MONTHLY:
            data = data.rename(columns={'Mom   ': 'WML'})

        return data

    def _load_fama_data(self, source: DataSource, frequency: Frequency) -> DataFrame:
        data: DataFrame = fama_french_reader(returns_data=source.value).read()[0]

        if isinstance(data.index, DatetimeIndex):
            frequency = 'B' if frequency == Frequency.DAILY else 'M'
            data = data.to_period(freq=frequency)
            log.debug(
                f"Fama reader returned DatetimeIndex for source '{source}', converted to frequency '{frequency}'"  # noqa: E501
            )

        return data
