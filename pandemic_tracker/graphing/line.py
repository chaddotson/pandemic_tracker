from logging import getLogger
from typing import List

from matplotlib import pyplot as plt

logger = getLogger(__name__)


def create_single_county_graph(dataframe, series: List, xlimits=None, ylimits=None, title=''):
    logger.debug('Creating single-county chart.')
    ax = plt.gca()

    for line in series:
        dataframe[line].plot(
            legend=True,
            xlim=xlimits,
            label=line.replace('_', ' ').title()
        )

    plt.title(title)
    ax.legend(bbox_to_anchor=(1.0, 1.0), loc='upper left')

    if xlimits:
        ax.set_xlim(xlimits)

    if ylimits:
        ax.set_xlim(ylimits)


def create_multi_county_graph(dataframe, series: List, value_column, xlimits=None, ylimits=None, title=''):
    logger.debug('Creating multi-county chart.')
    ax = plt.gca()

    for county in series:
        logger.debug(' - series: %s', county)
        dataframe.get_group(county)[value_column].plot(
            legend=True,
            xlim=xlimits,
            label=county
        )

    plt.title(title)
    # ax.legend(bbox_to_anchor=(1, 1.1))
    ax.legend(bbox_to_anchor=(1.0, 1.0), loc='upper left')

    if xlimits:
        ax.set_xlim(xlimits)

    if ylimits:
        ax.set_xlim(ylimits)

    logger.info('Done')
