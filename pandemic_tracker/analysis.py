# flake8: noqa: E501

import numpy as np


def add_derived_statistical_data_to_dataframe(dataframe):
    dataframe["ACTIVE_CASES_PER_10000"] = dataframe["TOTAL_ACTIVE"] / dataframe["POPESTIMATE2019"] * 10000
    dataframe["TOTAL_CASES_PER_10000"] = dataframe["TOTAL_CASES"] / dataframe["POPESTIMATE2019"] * 10000
    dataframe["TOTAL_DEATHS_PER_10000"] = dataframe["TOTAL_DEATHS"] / dataframe["POPESTIMATE2019"] * 10000

    grouped_by_county = dataframe.groupby('COUNTY')
    dataframe['14_DAY_ROLLING_NEW_ACTIVE'] = grouped_by_county['NEW_ACTIVE'].rolling(14).mean().reset_index(0, drop=True)

    dataframe['14_DAY_ROLLING_TOTAL_ACTIVE'] = grouped_by_county['TOTAL_ACTIVE'].rolling(14).mean().reset_index(0, drop=True)
    dataframe['7_DAY_ROLLING_TOTAL_ACTIVE'] = grouped_by_county['TOTAL_ACTIVE'].rolling(7).mean().reset_index(0, drop=True)
    dataframe['3_DAY_ROLLING_TOTAL_ACTIVE'] = grouped_by_county['TOTAL_ACTIVE'].rolling(3).mean().reset_index(0, drop=True)

    dataframe['3_DAY_ROLLING_SLOPE_TOTAL_ACTIVE'] = dataframe.groupby('COUNTY')['TOTAL_ACTIVE'].rolling(3).apply(lambda x: np.polyfit(range(len(x)), x, 1)[0]).reset_index(0, drop=True)
    dataframe['7_DAY_ROLLING_SLOPE_TOTAL_ACTIVE'] = dataframe.groupby('COUNTY')['TOTAL_ACTIVE'].rolling(7).apply(lambda x: np.polyfit(range(len(x)), x, 1)[0]).reset_index(0, drop=True)
    dataframe['14_DAY_ROLLING_SLOPE_TOTAL_ACTIVE'] = dataframe.groupby('COUNTY')['TOTAL_ACTIVE'].rolling(14).apply(lambda x: np.polyfit(range(len(x)), x, 1)[0]).reset_index(0, drop=True)

    dataframe['3_DAY_ROLLING_SLOPE_TOTAL_ACTIVE'] = dataframe.groupby('COUNTY')['TOTAL_ACTIVE'].rolling(3).apply(lambda x: np.polyfit(range(len(x)), x, 1)[0]).reset_index(0, drop=True)
    dataframe['7_DAY_ROLLING_SLOPE_TOTAL_ACTIVE'] = dataframe.groupby('COUNTY')['TOTAL_ACTIVE'].rolling(7).apply(lambda x: np.polyfit(range(len(x)), x, 1)[0]).reset_index(0, drop=True)
    dataframe['14_DAY_ROLLING_SLOPE_TOTAL_ACTIVE'] = dataframe.groupby('COUNTY')['TOTAL_ACTIVE'].rolling(14).apply(lambda x: np.polyfit(range(len(x)), x, 1)[0]).reset_index(0, drop=True)


