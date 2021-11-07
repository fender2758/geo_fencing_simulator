import geopandas as gpd

import matplotlib.pyplot as plt


def roads():
    plt.rcParams["font.family"] = 'NanumGothic'
    plt.rcParams["figure.figsize"] = (10, 10)
    file = "C:\\Users\\hyonj\\OneDrive - 중앙대학교\\CAU\\랩\\GIS\\Z_KAIS_TL_SPBD_EQB_경기"

    roads = gpd.read_file(file)

    ax = roads.convex_hull.plot(color='purple', edgecolor='w')
    ax.set_title('test')
    ax.set_axis_off()
    plt.show()


def cities():
    plt.rcParams["font.family"] = 'NanumGothic'
    plt.rcParams["figure.figsize"] = (10, 10)
    file = "C:\\Users\\hyonj\\OneDrive - 중앙대학교\\CAU\\랩\\GIS\\2020-TM-GR-MA-BA 행정경계(2019년 기준)_세계\\2020-TM-GR-MA-BA 행정경계(2019년기준_세계좌표)"

    cities = gpd.read_file(file)
    suwon = cities[cities.DISTRICT_N.str.contains('수원시')]



    #ax = suwon.convex_hull.plot(color='purple', edgecolor='w')

    ax = gpd.GeoSeries(suwon.unary_union).plot(color='purple', edgecolor='w')

    ax.set_title('test')

    plt.show()
    return suwon

def cities_and_roads():
    plt.rcParams["figure.figsize"] = (10, 10)
    file = "C:\\Users\\hyonj\\OneDrive - 중앙대학교\\CAU\\랩\\GIS\\2020-TM-GR-MA-BA 행정경계(2019년 기준)_세계\\2020-TM-GR-MA-BA 행정경계(2019년기준_세계좌표)"

    cities = gpd.read_file(file)
    cities = cities.to_crs(epsg=4326)
    suwon = cities.loc[cities.DISTRICT_N.str.contains('수원시'), 'geometry']
    suwon_union = suwon.unary_union
    file = "C:\\Users\\hyonj\\OneDrive - 중앙대학교\\CAU\\랩\\GIS\\Z_KAIS_TL_SPBD_BULD_경기"

    roads = gpd.read_file(file)
    roads = roads.to_crs(epsg=4326)
    print(roads.head())
    roads_suwon = roads[roads.within(suwon_union)]

    """
    ax = plt.subplot(1, 2, 1)
    x, y = suwon.exterior.xy
    plt.plot(x, y, color='purple', ax=ax)
    ax.set_title('suwon')
    ax.set_axis_off()
    """
    """
    ax = plt.subplot(1, 2, 1)
    roads_suwon.plot(color='purple', edgecolor='w', ax=ax)
    """
    x, y = suwon_union.exterior.xy
    plt.figure()
    plt.plot(x, y)
    ax = roads_suwon.plot(color='purple', edgecolor='w')
    ax.set_title('roads')
    ax.set_axis_off()

    plt.show()
    return roads_suwon

if __name__ == "__main__":
    cities_and_roads()
