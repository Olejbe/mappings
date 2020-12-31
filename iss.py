import geopandas as gpd
import requests
from shapely.geometry import Point
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def find_iss() -> tuple:
    response = requests.get("http://api.open-notify.org/iss-now.json")
    result = response.json()
    lat = float(result['iss_position']['latitude'])
    lon = float(result['iss_position']['longitude'])
    return lat, lon


def create_current_iss_point() -> gpd.GeoDataFrame:
    # Fetches the lat and lon of ISS (important ot get the correct values as a mix up may cause bugs")
    iss_lat, iss_lon = find_iss()
    print(f"Fetched lat {iss_lat} and lon {iss_lon}")

    # create a gpd dataframe that can be plotted
    create_iss_pointer = Point(iss_lon, iss_lat)
    iss_dict = {'name': ['iss'], 'geometry': [create_iss_pointer]}
    iss_gpd = gpd.GeoDataFrame(iss_dict, crs="EPSG:4326")
    return iss_gpd


fig, ax = plt.subplots(figsize=(15, 10))
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))


def iss_animate(i):
    plt.cla()
    #read and create world plot and then smack the iss_gpd on top of that.
    iss_gpd = create_current_iss_point()
    world.plot(ax=ax, color='blue', linewidth=0.5, edgecolor='white')
    ax.set_axis_off()
    iss_gpd.plot(ax=ax, color='red', markersize=10)

ani = FuncAnimation(fig, iss_animate, interval=5000)


plt.show()



