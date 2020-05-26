"""
Functions to create map plots for data and other associated utilities.
"""

from matplotlib import pyplot as plt
from matplotlib.patches import Polygon
from mpl_toolkits.basemap import Basemap
from typing import List

_default_state_boundry_options = dict(linewidth=0.5, linestyle="solid", color=(0, 0, 0),
                                      antialiased=1, ax=None, zorder=None)
_default_county_boundry_options = dict(linewidth=0.1, linestyle="solid", color=(0, 0, 0),
                                       antialiased=1, ax=None, zorder=None, drawbounds=False)


def make_basemap(lat_0, lon_0, lower_left_lon, lower_left_lat, upper_right_lon, upper_right_lat):
    """
    Makes the basic map constrained by the coordinates provided.
    :param lat_0:
    :param lon_0:
    :param lower_left_lon:
    :param lower_left_lat:
    :param upper_right_lon:
    :param upper_right_lat:
    :return:
    """
    m = Basemap(projection='lcc', lat_0=lat_0, lon_0=lon_0,
                resolution='h', area_thresh=0.1,
                llcrnrlon=lower_left_lon, llcrnrlat=lower_left_lat,
                urcrnrlon=upper_right_lon, urcrnrlat=upper_right_lat)

    # TODO: For some reason, new versions of basemap cause the following 2 lines to throw errors. Not critical atm.
    # m.drawcoastlines()
    # m.drawcountries()
    m.drawstates(**_default_state_boundry_options)
    m.drawcounties(**_default_county_boundry_options)
    m.drawmapboundary()

    return m


def generate_poly_map_from_basemap(map: Basemap):
    """
    This pulls the map of polygons from the specified basemap
    :param map: The basemap to interrogate.
    :return: Returns a map: county to list of polygons
    """
    county_poly_map = {}
    for i, county in enumerate(map.counties_info):
        county_hash = make_county_hash(county["STATE"], county["NAME"])

        if county_hash not in county_poly_map:
            county_poly_map[county_hash] = [map.counties[i]]
        else:
            county_poly_map[county_hash].append(map.counties[i])
    return county_poly_map


def get_rgb(val: float, min: float, max: float) -> List[float]:
    """
    Scale the value between min and max
    :param val:
    :param min:
    :param max:
    :return:
    """
    mid = min + (max - min) / 2

    if val > mid:
        perc_left = (max - val) / (max - mid)
        b = 0
        g = 1.0 * perc_left
        r = 1.0 * (1 - perc_left)

    elif val < mid:
        perc_left = (mid - val) / (mid - min)
        b = 1.0 * perc_left
        g = 1.0 * (1 - perc_left)
        r = 0

    else:
        r = 0
        g = 1
        b = 0

    return [r, g, b]


def make_county_hash(state: str, county: str) -> str:
    """
    Make the hash for the county that matches the one generated from the basemap.
    :return: The hash for the state/county combo.
    """
    if type(state) == str:
        state = bytes(state, "UTF8")
    if type(county) == str:
        county = bytes(county, "UTF8")
    return (state + b"_" + county).lower()


def get_rscale(val: float, scale_low: float, scale_high: float) -> List[float]:
    """
    Get a scaled RGB in the red spectrum.
    :param val:
    :param scale_low:
    :param scale_high:
    :return:
    """
    val = min(max(val, scale_low), scale_high)

    r = (val-scale_low) / (scale_high-scale_low)
    return [1, 1-r, 1-r]


def create_state_heat_map(dataframe, field='TOTAL_ACTIVE', title='', min=None, max=None):
    """
    Create the heatmap for a state.
    :param dataframe:
    :param field:
    :param title:
    :param min:
    :param max:
    :return:
    :note: Right now this is hardcoded for TN based on the coordinates.
    """

    # TODO: fix hardcoded coords.
    state_map = make_basemap(lat_0=39.1622, lon_0=-86.5292,
                             lower_left_lon=-90.60, lower_left_lat=34.80,
                             upper_right_lon=-81.31, upper_right_lat=36.71)
    ax = plt.gca()

    min_scale_value = min if min else 0
    max_scale_value = max if max else dataframe[field].max()

    county_poly_map = generate_poly_map_from_basemap(state_map)

    for county, data in dataframe.groupby('COUNTY'):
        if county == "Out of State" or county == "Pending":
            continue
        last_value = data[field].values[-1]
        color = get_rscale(last_value, min_scale_value, max_scale_value)

        segments = county_poly_map[make_county_hash("tn", county)]
        for segment in segments:
            # poly = Polygon(seg, facecolor=get_rgb(count, minimum, maximum), edgecolor=(0.9, 0.9, 0.9))
            poly = Polygon(segment,
                           facecolor=color,
                           edgecolor=(0.9, 0.9, 0.9))

            ax.add_patch(poly)

    plt.title(title)

    if min or max:
        # ax.text(6, 8, f"*Artificially constricted min:{min}, max:{max}", fontsize=10)
        plt.text(
            0.50,
            0.25,
            f"*Artificially constricted min:{min_scale_value}, max:{max_scale_value}",
            fontsize=8,
            horizontalalignment='center',
            verticalalignment='center',
            bbox={'facecolor': 'red', 'alpha': 0.2, 'pad': 10},
            transform=plt.gcf().transFigure
        )

    return state_map
