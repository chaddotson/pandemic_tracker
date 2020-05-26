"""
Classes for downloading pandemic information about states
"""

from abc import ABC, abstractmethod
import pandas as pd


class PandemicDataDownloader(ABC):
    """
    Base class for pandemic data downloaders.  Results of all downloaders should be similar.
    """
    _MERGE_COLUMN = 'COUNTY'
    _MRRGED_COLUMNS_FROM_POPULATION = ['COUNTY', 'POPESTIMATE2019']
    _STATE = ""

    def __init__(self, population_dataframe):
        """
        Initialize the pandemic data downloader with the population dataframe.
        :param population_dataframe: A dataframe containing the population information by county.
        """
        self._population = population_dataframe

    def _merge_population_data(self, dataframe):
        """
        Merge critical population data onto the pandemic dataframe
        :param dataframe: A pandas dataframe containing the pandemic info by county.
        :return: A merged dataframe containing pandemic and population data.
        """

        grps = self._population.groupby("STNAME")
        grp = grps.get_group(self._STATE)

        return dataframe.merge(
            grp[self._MRRGED_COLUMNS_FROM_POPULATION],
            on=self._MERGE_COLUMN,
            how="left"
        )

    @abstractmethod
    def download(self):
        """
        Download the pandemic data.
        :return: A dataframe with the pandamic data by county.
        """
        pass


class TennesseePandemicDataDownloader(PandemicDataDownloader):
    """
    A pandemic data downloader for Tennessee.
    """
    _DATA_URL = 'https://www.tn.gov/content/dam/tn/health/documents/cedep/novel-coronavirus/datasets/Public-Dataset-County-New.XLSX'  # noqa: E501
    _SHEET_NAME = 'ALL_COUNTY_FINAL_PUBLIC'
    _STATE = "Tennessee"

    def download(self):
        """
        Download the pandemic data.
        :return: A dataframe with the pandamic data by county.
        """
        tennessee_pandemic_data = pd.read_excel(self._DATA_URL, sheet_name=self._SHEET_NAME)
        return self._merge_population_data(tennessee_pandemic_data)
        # return tennessee_pandemic_data


# def get_state_data():
#     data_url = 'https://www.tn.gov/content/dam/tn/health/documents/cedep/novel-coronavirus/datasets/Public-Dataset-County-New.XLSX'
#     # NOTE: Using requests is not required since pandas can read the URL directly.
#     daily_pandemic_data = requests.get(data_url)
#     dataframe = pd.read_excel(daily_pandemic_data.content, sheet_name='ALL_COUNTY_FINAL_PUBLIC')
#
#     return dataframe


