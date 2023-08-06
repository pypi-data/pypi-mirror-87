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
from typing import Any

import pandas
from pandas import DataFrame
from statsmodels.formula import api as sm
from statsmodels.iolib.summary2 import summary_col

from f4ratk.shared import first_period, last_period


class Analyzer:
    def analyze(self, stock_data: DataFrame, fama_data: DataFrame):
        log.info(
            f"Stock data range: {first_period(stock_data)} - {last_period(stock_data)}"
        )
        log.info(
            f"Fama data range : {first_period(fama_data)} - {last_period(fama_data)}"
        )

        combined: DataFrame = pandas.merge(
            stock_data, fama_data, left_index=True, right_index=True
        )

        log.info(
            f"Result date range: {first_period(combined)} - {last_period(combined)}"
        )

        combined['XsRet'] = combined['Returns'] - combined['RF']

        def model(formula: str, data: DataFrame) -> Any:
            return sm.ols(formula=formula, data=data).fit()

        CAPM = model(formula='XsRet ~ MKT', data=combined)
        FF3 = model(formula='XsRet ~ MKT + SMB + HML', data=combined)
        FF5 = model(formula='XsRet ~ MKT + SMB + HML + RMW + CMA', data=combined)
        FF6 = model(formula='XsRet ~ MKT + SMB + HML + RMW + CMA + WML', data=combined)

        CAPMtstat = CAPM.tvalues
        FF3tstat = FF3.tvalues
        FF5tstat = FF5.tvalues
        FF6tstat = FF6.tvalues

        CAPMcoeff = CAPM.params
        FF3coeff = FF3.params
        FF5coeff = FF5.params
        FF6coeff = FF6.params

        DataFrame(
            {
                'CAPMcoeff': CAPMcoeff,
                'CAPMtstat': CAPMtstat,
                'FF3coeff': FF3coeff,
                'FF3tstat': FF3tstat,
                'FF5coeff': FF5coeff,
                'FF5tstat': FF5tstat,
                'FF6coeff': FF6coeff,
                'FF6tstat': FF6tstat,
            },
            index=['Intercept', 'MKT', 'SMB', 'HML', 'RMW', 'CMA', 'WML'],
        )

        output = summary_col(
            [CAPM, FF3, FF5, FF6],
            stars=True,
            float_format='%0.4f',
            model_names=['CAPM', 'FF3', 'FF5', 'FF6'],
            info_dict={
                'N': lambda x: "{0:d}".format(int(x.nobs)),
                'Adjusted R2': lambda x: "{:.4f}".format(x.rsquared_adj),
            },
            regressor_order=['Intercept', 'MKT', 'SMB', 'HML', 'RMW', 'CMA', 'WML'],
        )

        print(output)
        print(FF6.summary())
