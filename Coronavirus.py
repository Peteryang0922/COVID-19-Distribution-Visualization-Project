import pandas as pd
import numpy as np
import folium
import math
import json
import webbrowser
from datetime import date, datetime,timedelta
from uszipcode import SearchEngine
import warnings

def catch_distribution():
    url = ("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/")
    try:
        df = pd.read_csv(url + date.today().strftime("%m-%d-%Y") +".csv", error_bad_lines=False)
    except:
        df = pd.read_csv(url + datetime.strftime(datetime.now() - timedelta(1), '%m-%d-%Y') +".csv", error_bad_lines=False)
    return df

def china_map():
    df_world = catch_distribution()
    df_china = df_world.loc[(df_world['Country/Region'] == 'Mainland China') | (df_world['Country/Region'] == 'Taiwan') | (df_world['Country/Region'] == 'Hong Kong') | (df_world['Country/Region'] == 'Macau')]
    fname = "chinamap.geojson" 
    with open(fname, encoding='utf-8') as data_file:
        china_geo = json.load(data_file)
    myscale = [0,10,100,1000,2000,100000]
    
    map1 = folium.Map(location=[34.001684, 108.736552], zoom_start = 4.3)
    
    map1.choropleth(geo_data = china_geo,
                      data = df_china,
                      columns = ['Province/State','Confirmed'],
                      key_on = 'feature.properties.Name_1',
                      fill_color = 'Reds',
                      threshold_scale = myscale,
                      fill_opacity = 0.7)
    
    for lat, lon, confirmed, death, recovered, name in zip(df_china['Latitude'], df_china['Longitude'], df_china['Confirmed'], df_china['Deaths'], df_china['Recovered'], df_china['Province/State']):
        folium.CircleMarker([lat, lon],
                            radius = 3,
                            popup = ('<strong>Province/City</strong>: ' + str(name) + '<br>'
                                    '<strong>Confirmed</strong>: ' + str(confirmed) + '<br>'
                                     '<strong>Deaths</strong>: ' + str(death) + '<br>'
                                     '<strong>Recovered</strong>: ' + str(recovered) + '<br>'),
                            color = 'red',
                            fill_color = 'red',
                            fill_opacity = 0.7 ).add_to(map1)
    
    map1.save('Coronavirus in China.html')
    webbrowser.open('Coronavirus in China.html')

def usa_map():
    df_world = catch_distribution()
    df_usa = df_world.loc[(df_world['Country/Region'] == 'US')]
    State = []
    for i in df_usa['Province/State']:
        State.append(i[i.find(',') + 2:i.find(',') + 4])
    df_usa.insert(loc = 8, column = 'State', value = np.asarray(State))
    
    d = {}
    for i in df_usa['State'].unique():
        d[i] = sum([df_usa['Confirmed'][j] for j in df_usa[df_usa['State'] == i].index])
    df_state = pd.Series(d).to_frame()
    df_state = df_state.reset_index()
    df_state.columns = ['State','Confirmed']
    
    fname = "usamap.geojson" 
    with open(fname, encoding='utf-8') as data_file:
        usa_geo = json.load(data_file)
    myscale = [0,5,10,40,100,200]
    map2 = folium.Map(location=[38.203457, -94.618874], zoom_start = 5)
    
    map2.choropleth(geo_data = usa_geo,
                      data = df_state,
                      columns = ['State','Confirmed'],
                      key_on = 'feature.properties.NAME_1',
                      fill = True,
                      fill_color = 'Reds',
                      nan_fill_color='white',
                      threshold_scale = myscale,
                      fill_opacity = 0.5)
    
    for lat, lon, confirmed, death, recovered, name in zip(df_usa['Latitude'], df_usa['Longitude'], df_usa['Confirmed'], df_usa['Deaths'], df_usa['Recovered'], df_usa['Province/State']):
        folium.CircleMarker([lat, lon],
                            radius = 3,
                            popup = ('<strong>City</strong>: ' + str(name) + '<br>'
                                    '<strong>Confirmed</strong>: ' + str(confirmed) + '<br>'
                                     '<strong>Deaths</strong>: ' + str(death) + '<br>'
                                     '<strong>Recovered</strong>: ' + str(recovered) + '<br>'),
                            color = 'red',
                            fill_color = 'red',
                            fill_opacity = 0.7 ).add_to(map2)
    
    map2.save('Coronavirus in USA.html')
    webbrowser.open('Coronavirus in USA.html')

def world_map():
    warnings.filterwarnings("ignore")
    df_world = catch_distribution()
    
    c = {}
    d = {}
    r = {}
    for i in df_world['Country/Region'].unique():
        c[i] = sum([df_world['Confirmed'][j] for j in df_world[df_world['Country/Region'] == i].index])
        d[i] = sum([df_world['Deaths'][j] for j in df_world[df_world['Country/Region'] == i].index])
        r[i] = sum([df_world['Recovered'][j] for j in df_world[df_world['Country/Region'] == i].index])
    df_Confirmed = pd.Series(c).to_frame()
    df_Confirmed = df_Confirmed.reset_index()
    df_Confirmed.columns = ['Country/Region','Confirmed']
    df_Deaths = pd.Series(d).to_frame()
    df_Deaths = df_Deaths.reset_index()
    df_Deaths.columns = ['Country/Region','Deaths']
    df_Recovered = pd.Series(r).to_frame()
    df_Recovered = df_Recovered.reset_index()
    df_Recovered.columns = ['Country/Region','Recovered']
    df_country = df_Confirmed
    df_country['Deaths'] = df_Deaths['Deaths']
    df_country['Recovered'] = df_Recovered['Recovered']
    
    f = {}
    g = {}
    for i in df_world['Country/Region'].unique():
        f[i] = np.mean([df_world['Latitude'][j] for j in df_world[df_world['Country/Region'] == i].index])
        g[i] = np.mean([df_world['Longitude'][j] for j in df_world[df_world['Country/Region'] == i].index])
    df_lat = pd.Series(f).to_frame()
    df_lat = df_lat.reset_index()
    df_lat.columns = ['Country/Region','Latitude']
    df_lgt = pd.Series(g).to_frame()
    df_lgt = df_lgt.reset_index()
    df_lgt.columns = ['Country/Region','Longitude']
    df_country['Latitude'] = df_lat['Latitude']
    df_country['Longitude'] = df_lgt['Longitude']
    
    fname = "worldmap.geojson" 
    with open(fname, encoding='utf-8') as data_file:
        world_geo = json.load(data_file)
    myscale = [0,10,100,1000,2000,100000]
    map3 = folium.Map(location=[36.070080, 45.611698], zoom_start = 2)
    
    map3.choropleth(geo_data = world_geo,
                      data = df_country,
                      columns = ['Country/Region','Confirmed'],
                      key_on = 'feature.properties.sovereignt',
                      fill = True,
                      fill_color = 'Reds',
                      nan_fill_color='white',
                      threshold_scale = myscale,
                      fill_opacity = 0.5)
    
    for lat, lon, confirmed, death, recovered, name in zip(df_country['Latitude'], df_country['Longitude'], df_country['Confirmed'], df_country['Deaths'], df_country['Recovered'], df_country['Country/Region']):
        folium.CircleMarker([lat, lon],
                            radius = 3,
                            popup = ('<strong>Contry/Region</strong>: ' + str(name) + '<br>'
                                    '<strong>Confirmed</strong>: ' + str(confirmed) + '<br>'
                                     '<strong>Deaths</strong>: ' + str(death) + '<br>'
                                     '<strong>Recovered</strong>: ' + str(recovered) + '<br>'),
                            color = 'red',
                            fill_color = 'red',
                            fill_opacity = 0.7 ).add_to(map3)
    
    map3.save('Coronavirus in World.html')
    webbrowser.open('Coronavirus in World.html')

def haversine(coord1, coord2):
    R = 6372800
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    phi1, phi2 = math.radians(lat1), math.radians(lat2) 
    dphi       = math.radians(lat2 - lat1)
    dlambda    = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + \
        math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))

def search_zip():
    search = SearchEngine(simple_zipcode=True)
    zipcode = str(input('Please enter your zip code: '))
    zone = search.by_zipcode(zipcode).to_dict()
    
    df_world = catch_distribution()
    df_usa = df_world.loc[(df_world['Country/Region'] == 'US')]
    
    map4 = folium.Map(location=[zone['lat'],zone['lng']], zoom_start = 10)
    for i,x,y in zip(df_usa['Province/State'],df_usa['Latitude'], df_usa['Longitude']):
        if haversine((x,y), (zone['lat'],zone['lng']))/1000 < 50:
            folium.Marker(location=[x,y],popup=i,icon = folium.Icon(color='red', icon='meh-o', prefix='fa')).add_to(map4)
    folium.Marker([zone['lat'],zone['lng']], popup='<strong>Your location</strong>: ' + zipcode + '<br>').add_to(map4)
    map4.save('Coronavirus Near You.html')
    webbrowser.open('Coronavirus Near You.html')

if __name__ == '__main__':
    print('COVID-19 Distribution Visualization Project')
    while(1):
        print('a.USA Map             b.China Map')
        print('c.World Map           d.Cases Near You')
        print('q.Quit the System')
        s = str(input('Please enter corresponding key to view the results: ')).lower()
        if s == 'a':
            usa_map()
        elif s == 'b':
            china_map()
        elif s == 'c':
            world_map()
        elif s == 'd':
            search_zip()
        elif s == 'q':
            break
        else:
            print('Invalid input, please enter again')