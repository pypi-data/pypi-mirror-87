import json
import requests
import numpy as np
from matplotlib import cm
from matplotlib.colors import rgb2hex

from shapely.geometry import Polygon
from shapely.algorithms import polylabel # Function to find pole of inaccessibility to approximate the centroid of a polygon

class DmaPlotter:
  
  def __init__(self, cmap=cm.get_cmap('cool')):
    # Get GeoJson
    r = requests.get("https://github.com/Mrk-Nguyen/dmamap/raw/master/nielsengeo.json")
    source_geo = json.loads(r.text)
    self.dmas_geo = [dict(type='FeatureCollection',features=[feat]) for feat in source_geo.get('features')]
    self.cmap = cmap
    
  def get_color(self, value, extreme):
    
    normalized_value = float(2*value - extreme)/float(extreme)
  
    return rgb2hex(self.cmap(normalized_value))
      
  def get_extreme_values(self, values):
    mean_val = np.mean(values)
    std_val = np.std(values)
    return mean_val + 2*std_val

  def get_dma_info(self, dma):
      #print(dma)
      dma_dicts = [d for d in self.dmas_geo if d.get('features')[0]['id'] == dma]
      if(len(dma_dicts) == 0):
        return None
      feature = dma_dicts[0]['features'][0]
  
      return dict(dma_code=int(feature.get('id')),
                  dma_name=feature.get('properties').get('dma1'),
                  lat_ctr=feature.get('properties').get('latitude'),
                  lon_ctr=feature.get('properties').get('longitude'),
                  geo_type=feature.get('geometry').get('type'),
                  geo_coords=feature.get('geometry').get('coordinates'))
                  
  def get_choropleths(self, dmas, metric, pretty_metric_name=''):
    
    data = []
    lat_centers = []
    lon_centers = []
    center_tooltips = []
  
    extreme = self.get_extreme_values(metric)

    for dma, value in zip(dmas, metric):
      
      dma_info = self.get_dma_info(dma)
      if(dma_info is None):
        continue;
      dma_info['perf_val'] = value
      dma_info['perf_color'] = self.get_color(value, extreme)

      # Extract all polygons in the DMA
      dma_traces = []
      
      if dma_info['geo_type'] == 'Polygon':
          x_coords, y_coords = zip(*dma_info['geo_coords'][0])
          
          data.append(self.create_area(x_coords,
                                  y_coords,
                                  dma_info.get('perf_color')))
      elif dma_info['geo_type'] == 'MultiPolygon':
          
          for polygon in dma_info['geo_coords']:
              x_coords, y_coords = zip(*polygon[0])
          
              dma_traces.append(self.create_area(x_coords,
                                            y_coords,
                                            dma_info.get('perf_color')))
      else:
          raise Exception(f'Unsupported geometry type: {geo_type}')
      
      data.extend(dma_traces)
                                                                                                          
      # Add markers on centroid for this DMA to enable hoverboxes within each DMA region
      lat_centers.append(dma_info.get('lat_ctr'))
      lon_centers.append(dma_info.get('lon_ctr'))
      center_tooltips.append('DMA {:d}: {:s}<br>{:s}: {:.5f}'.format(dma_info.get('dma_code'), dma_info.get('dma_name'),pretty_metric_name,dma_info.get('perf_val')))
  
    # Define the centers object for plotly to plot all this hidden markers to enable tooltips
    centers = dict(type='scatter',
                   mode='markers',
                   showlegend=False,
                   marker=dict(size=5,opacity=0),
                   text=center_tooltips,
                   x=lon_centers,
                   y=lat_centers,
                   hoverinfo='text',
                   hoverlabel=dict(bgcolor='white')
                  )
    
    data.append(centers)
      
    return data


  def create_area(self, x_coords,y_coords,perf_color):
      """
      Helper function to return an object that defines a Scatter trace for plotly. This Scatter trace creates a filled area defined by the x and y coordinates
      
      Parameters:
          x_coords (list): List of x coordinates
          y_coords (list): List of y coordinates
          perf_color (str): Color to fill the area
      
      Returns:
          area (object) plotly Scatter definition
      
      """
      return dict(type='scatter',
                  showlegend = False,
                  mode='lines',
                  line=dict(color='black',width=1),
                  x = x_coords,
                  y = y_coords,
                  fill='toself',
                  fillcolor=perf_color,
                  hoverinfo='none')
                
                
  def build_figure(self, dmas, metric, pretty_metric_name='', height=500, width=666, 
  plot_bgcolor='#191925', paper_bgcolor='#191925'):
    data = self.get_choropleths(dmas, metric, pretty_metric_name=pretty_metric_name)
    axis = dict(showgrid=False,showticklabels=False)
    
    layout = dict(height= height,
                  width = width,
                  hovermode='closest',
                  xaxis=axis,
                  yaxis=axis,
                  plot_bgcolor=plot_bgcolor,
                  paper_bgcolor=paper_bgcolor)
    
    return dict(data=data,layout=layout)