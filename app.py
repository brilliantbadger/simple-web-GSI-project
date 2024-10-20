from flask import Flask, render_template, request
import folium
import rasterio
import numpy as np
from folium.plugins import MiniMap, Fullscreen
from folium.raster_layers import ImageOverlay
import os

app = Flask(__name__)
app.config['upload'] = 'uploads'

@app.route('/', methods=['GET', 'POST'])
def index():
    startCoord = [19.6853317, -80.0477797]
    startZoom = 13
    # create map object
    m = folium.Map(location = startCoord, zoom_start = startZoom, tiles = None)

    if request.method == 'POST':
        formType = request.form.get('formType')

        if formType == 'coord':
            latitude = request.form.get('latitude')
            longitude = request.form.get('longitude')

            if latitude and longitude:
                m = folium.Map(location = [latitude, longitude], zoom_start = 7, tiles = None)

        elif formType == 'file':
            upload = request.files['file']
            name = upload.filename

            if upload and name.endswith('.tif'):
                filepath = os.path.join(app.config['upload'], name)
                upload.save(filepath)

                img = rasterio.open(filepath)
                #  set bounds
                bounds = img.bounds

                # read + combine multiple bands to create color
                red = img.read(1)
                green = img.read(2)
                blue = img.read(3)
                
                data = np.stack((red, green, blue), axis=-1)
                data = (data - data.min()) / (data.max() - data.min())
                data = (data * 255).astype(np.uint8)

                m = folium.Map(location = [(bounds.top+bounds.bottom)/2, (bounds.left+bounds.right)/2], zoom_start = startZoom, tiles = None)

                # create overlay with uploaded files
                overlay = folium.raster_layers.ImageOverlay(
                    image = data,
                    bounds = [[bounds.bottom, bounds.left], [bounds.top, bounds.right]],
                    opacity = 0.8, # need opacity or it looks like ass
                    name = name[:-4]
                ).add_to(m)

    # map markers
    folium.Marker([19.6853317, -80.0477797],
                  popup = '<strong>Little Cayman</strong>',
                  tooltip = 'Click for More Info').add_to(m),
    folium.Marker([19.6853317, -80.06],
                  popup = '<strong>Test Location 1</strong>',
                  tooltip = 'Click for More Info',
                  icon = folium.Icon(icon='cloud')).add_to(m),
    folium.Marker([19.7, -80.03],
                  popup = '<strong>Test Location 2</strong>',
                  tooltip = 'Click for More Info',
                  icon = folium.Icon(color='purple')).add_to(m),
    folium.Marker([19.7, -80.02],
                  popup = '<strong>Test Location 3</strong>',
                  tooltip = 'Click for More Info',
                  icon = folium.Icon(icon='leaf', color='green')).add_to(m)

    # marker with custom icon
    customIcon = folium.features.CustomIcon('static/icon.png', icon_size = (40, 40))
    folium.Marker([19.7, -80.01],
                  popup = '<strong>Test Location 4</strong>',
                  tooltip = 'Click for More Info',
                  icon = customIcon).add_to(m)

    # circle marker
    folium.CircleMarker(
        location = [19.68, -80.07],
        radius = 50,
        popup = '<strong>Test Location 5</strong>',
        color = '#ff69b4',
        fill = True,
        fill_color = '#ff69b4'
    ).add_to(m)

    # control map types using layers
    folium.TileLayer(
        tiles = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        attr = '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        name = 'Open Street Map',
        overlay = False,
        control = True
    ).add_to(m)

    folium.TileLayer(
        tiles = 'http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png',
        attr = '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="https://carto.com/attributions">CARTO</a>',
        name = 'CartoDB Positron',
        overlay = False,
        control = True
    ).add_to(m)

    folium.TileLayer(
        tiles = 'http://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png',
        attr = '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="https://carto.com/attributions">CARTO</a>',
        name = 'CartoDB DarkMatter',
        overlay = False,
        control = True
    ).add_to(m)  

    folium.TileLayer(
        tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr = '&copy; <a href="https://www.esri.com/">Esri</a>',
        name = 'Esri Satellite',
        overlay = False,
        control = True
    ).add_to(m)
 
    folium.LayerControl().add_to(m)

    # minimap
    mini = MiniMap()
    m.add_child(mini)

    # fullscreen control
    Fullscreen().add_to(m)

    # generate map
    map_html = m._repr_html_()
    return render_template('index.html', map_html = map_html)

if __name__ == '__main__':
    app.run(debug=True)