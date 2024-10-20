# A Simple Web GSI application

>***NOTE:*** *This is made as part of the application process for the Radio Telemetry Tracker research project. More information can be found [here](https://github.com/UCSD-E4E/radio-telemetry-tracker-docs/blob/main/docs/development-guides/intro-project.md)*

This application uses [Flask](https://flask.palletsprojects.com/en/3.0.x/) and [Folium](https://python-visualization.github.io/folium/latest/) to display a map in a web interface. [Rasterio](https://rasterio.readthedocs.io/en/latest/index.html) is also used to read and convert GeoTIFF files to a format that Folium can use and display. [Poetry](https://python-poetry.org/) is used for organization and dependency management.

**Features:**
1. Zoom in / Zoom out with buttons or the scroll wheel
2. Fullscreen button
3. Minimap on the bottom right of screen
4. Can load different webmap tiles (Open Street MapCarto, DB Positronarto, DB DarkMatter, Esri Satellite)
5. Different types of markers are displayed on the map
6. A GeoTIFF file can be uploaded and is shown on the main map as an overlay (can be toggled on or off by the user)
7. User can navigate the map using latitude and longitude coordinates

**Limitations:**
1. Other file formats (shapefile, GeoJSON) cannot be loaded in
2. Does not display landmarks
3. Users cannot ddirectly create markers on the map

**Minor Issues/Bugs:**
1. The selection for the webmap tiles does not stay consistent with most user interactions (i.e. uploading file or inputting coordinates reverts the webmap tile back to 'Esri Satellite')
2. There is nothing that prevents the user from inputting invalid latitude and longitude coordinates. Doing so incurs a ValueError.

## How to open the web application

>***NOTE:*** *[Python 3](https://www.python.org/downloads/) and [Poetry](https://python-poetry.org/docs/) should be installed on your system*

Clone this repository:

```
git clone https://github.com/brilliantbadger/simple-web-GSI-project.git
```

Navigate into the project directory:

```
cd simple-web-GSI-project
```

Install dependencies utilizing Poetry:

```
poetry install
```

Run app.py using Poetry

```
poetry run python app.py
```

Go to [localhost:5000](http://localhost:5000/) on a web browser of your choice.