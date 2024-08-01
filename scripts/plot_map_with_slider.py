# + tags=["parameters"]
# add default values for parameters here

# +
import pandas as pd
import folium
from folium.plugins import TimestampedGeoJson

def run(upstream, product):
    df = pd.read_csv(upstream['filter_data']['data'])
    df['date'] = pd.to_datetime(df['date'])

    # Create a map centered around the mean coordinates with a specific zoom level
    m = folium.Map(location=[df['YCoordinate'].mean(), df['XCoordinate'].mean()], zoom_start=4)

    # Define a function to determine color based on value
    def get_color(value):
        if value < 10:
            return 'green'
        elif 10 <= value < 20:
            return 'blue'
        elif 20 <= value < 30:
            return 'orange'
        else:
            return 'red'

    # Define a function to determine radius based on value
    def get_radius(value):
        if value < 10:
            return 8
        else:
            return 10

    features = []
    for i, row in df.iterrows():
        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [row['XCoordinate'], row['YCoordinate']]
            },
            'properties': {
                'time': row['date'].isoformat(),
                'popup': f"ID: {row['Id']} - {row['Name']}: ({row['XCoordinate']}, {row['YCoordinate']}) Value: {row['value']}",
                'icon': 'circle',
                'iconstyle': {
                    'color': get_color(row['value']),
                    'fillColor': get_color(row['value']),
                    'fillOpacity': 0.6,
                    'radius': get_radius(row['value'])
                }
            }
        }
        if 'highlight_id' in row and row['Id'] == row['highlight_id']:
            # Adding blinking effect for the highlighted ID
            feature['properties']['iconstyle']['className'] = 'blinking'
        features.append(feature)

    TimestampedGeoJson({
        'type': 'FeatureCollection',
        'features': features
    }, period='P1D', add_last_point=True, auto_play=False, loop=False).add_to(m)

    # Add legend to the map
    legend_html = '''
     <div style="position: fixed; 
                 bottom: 50px; right: 50px; width: 150px; height: 150px; 
                 border:2px solid grey; z-index:9999; font-size:14px;
                 background-color:white;
                 ">
     &nbsp;<b>Legend</b><br>
     &nbsp;<i class="fa fa-circle" style="color:green"></i>&nbsp; value < 10<br>
     &nbsp;<i class="fa fa-circle" style="color:blue"></i>&nbsp; 10 <= value < 20<br>
     &nbsp;<i class="fa fa-circle" style="color:orange"></i>&nbsp; 20 <= value < 30<br>
     &nbsp;<i class="fa fa-circle" style="color:red"></i>&nbsp; value >= 30
     </div>
     '''
    m.get_root().html.add_child(folium.Element(legend_html))

    # Add CSS for blinking effect
    blinking_css = '''
    <style>
    .blinking {
        animation: blinker 1s linear infinite;
    }
    @keyframes blinker {
        50% { opacity: 0; }
    }
    </style>
    '''
    m.get_root().html.add_child(folium.Element(blinking_css))

    m.save(product['html'])

if __name__ == "__main__":
    upstream = {
        'filter_data': {
            'data': 'data/filtered_data.csv'
        }
    }
    product = {
        'html': 'data/map.html'
    }
    run(upstream, product)

