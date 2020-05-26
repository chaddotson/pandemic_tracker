import pandas as pd


class CensusPopulationDownloader(object):
    _DATA_URL = "https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/co-est2019-alldata.csv"  # noqa: E501
    _ENCODING = "ISO-8859-1"

    def download(self):
        data_url = self._DATA_URL
        dataframe = pd.read_csv(data_url, encoding=self._ENCODING)
        self._apply_fixes(dataframe)
        return dataframe

    def _apply_fixes(self, dataframe):
        # population["COUNTY"] = population["COUNTY"].loc(.str.replace("DeKalb", "Dekalb")
        dataframe["COUNTY"] = dataframe["CTYNAME"].str.replace(" County", "")

        # TODO: Fix this more specifically...
        # dataframe.loc[dataframe["STNAME"] == "Tennessee"].loc[dataframe["COUNTY"] == "DeKalb"]["COUNTY"] = dataframe.loc[dataframe["STNAME"] == "Tennessee"].loc[dataframe["COUNTY"] == "DeKalb"]["COUNTY"].str.replace("DeKalb", "Dekalb")
        dataframe["COUNTY"] = dataframe["COUNTY"].str.replace("DeKalb", "Dekalb")


# def get_population_data():
#     data_url = "https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/co-est2019-alldata.csv"  # noqa: E501
#     population_data = requests.get(data_url)
#     dataframe = pd.read_csv(data_url, encoding="ISO-8859-1")
#         # return dataframe
#     grps = dataframe.groupby("STNAME")
#     grp = grps.get_group("Tennessee")
#     return grp
