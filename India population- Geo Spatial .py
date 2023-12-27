#!/usr/bin/env python
# coding: utf-8

# # India Population: Visualization through Geo Spatial Data
# 
# In this project, I want to explore the population and other attributes for the country of India. I want to visualize these attributes through geospatial data and plot them on interactive maps. 
# 
# For this project, the most important attributes are the population of each state and their geospatial geometry. 
# 
# 1) Dataset containing Population: [Population of India](https://www.kaggle.com/datasets/rdatta871/population-of-india): This dataset contains the population distribution by state, gender, sex & region
# 
# 2) Dataset containing the Geospatial coordinates of each State and Union Terrirtory: [India GIS Data](https://www.kaggle.com/datasets/nehaprabhavalkar/india-gis-data/data): This dataset contains the geospatial data of each state of India

# Importing the relevant modules required

# In[1]:


import geopandas as gpd
import pandas as pd


# I imported the geospatial coordinates of each state of India into a variable 'india_map'

# In[2]:


# Read the shapefile or GeoJSON file of India
india_map = gpd.read_file('C:/Users/karan/Downloads/archive (3)/India States/Indian_states.shp')


# In[3]:


india_map


# After looking through the dataset, I noticed a some different format of State names and a few spelling mistakes in the names of states. Since I need to combine the file in india_map to the other dataset with the state population on the basis of state name, I need to make sure that both datasets have the same state names. 

# In[4]:


#Manually changing the names of the states

india_map.st_nm[0]='Andaman & Nicobar Islands'
india_map.st_nm[1]='Arunachal Pradesh'
india_map.st_nm[6]='Dadra and Nagar Haveli'
india_map.st_nm[23]='Delhi'


# In[5]:


india_map.st_nm


# Now importing the file with the population and other attributes of India and storing it in the variable 'population_data'

# In[6]:


population_data = pd.read_csv("C:/Users/karan/Downloads/archive (4)/Population of India.csv")


# In[7]:


population_data


# On the first look, the column names have unnecessary brackets or formats. Hence, I renamed them for better standardization

# In[8]:


population_data.rename(columns = {'State/UT':'State','Population[50]':'Population','Rural[51]':'Rural','Urban[51]':'Urban','Area[52] (km2)':'Area(km2)'}, inplace = True)


# In[9]:


population_data


# Also, the union terriroties have a '(UT)' placed after their name. Eg:'Lakshadweep (UT)' I want to get rid of this

# In[10]:


population_data['State'] = population_data['State'].str.replace(r'\([^)]*\)', '', regex=True).str.strip()


# In[11]:


population_data['State']


# After performing further data analysis, I realized that the first dataset used '&' inside the state's full names and the second dataset used 'and'. This will lead to merging issues because the merge function won't recognize them as one. Therefore, I decided to replace the 'and' with '&' in the state names.

# In[12]:


population_data['State'] = population_data['State'].apply(lambda x: x.replace(' and ', ' & '))


# I chose to replace ' and ' with spaces instead of 'and' because many of the states (eg. Uttarakhand) have 'and' in their name spelling. I don't want to replace that with the '&'. I only want to replace the 'and' with '&' in the names of the states where it is being used in spaces (eg. Jammu and Kashmir)

# In[13]:


population_data['State']


# In[14]:


population_data['Difference between male and female'] = population_data['Difference between male and female'].replace(r'\D', '', regex=True)


# In[15]:


population_data['Difference between male and female']


# In[16]:


population_data.dtypes


# In[17]:


population_data


# In[18]:


merged_data = india_map.merge(population_data, how='inner', left_on='st_nm', right_on='State')


# In[19]:


merged_data


# In[20]:


merged_data.columns


# In[21]:


merged_data= merged_data.drop(columns=['Sl No'])


# In[22]:


merged_data.columns


# We finally have a variable 'merged_data' with all the information required to start plotting geographical visualizations.
# Firstly, I want to plot a choropleth map showcasing the total population of each state

# In[23]:


import matplotlib.pyplot as plt

# Plotting the choropleth map
fig, ax = plt.subplots(1, 1, figsize=(12, 8))

# Plot the choropleth map showing population variation
merged_data.plot(column='Population', cmap='YlOrRd', ax=ax, legend=True,
                 legend_kwds={'label': "Population by State", 'orientation': "vertical"})

plt.title("Population Variation Across Indian States")
leg = ax.get_legend()
ax.set_axis_off()
plt.show()


# In[24]:


fig, ax = plt.subplots(1, 1, figsize=(12, 8))

# Plot the choropleth map showing population variation
merged_data.plot(column='Percent (%)', cmap='Accent', ax=ax, legend=True,
                 legend_kwds={'label': "Population by State (%)", 'orientation': "vertical"})

plt.title("Population Percentage Variation Across Indian States")
leg = ax.get_legend()
ax.set_axis_off()
plt.show()


# In[25]:


merged_data['Rural_Urban_Difference'] = merged_data['Urban'] - merged_data['Rural']

# Plotting the choropleth map illustrating the distribution of rural and urban populations
fig, ax = plt.subplots(1, 1, figsize=(12, 8))

# Plot the choropleth map showing the difference between rural and urban populations
merged_data.plot(column='Rural_Urban_Difference', cmap='coolwarm', ax=ax, legend=True,
                 legend_kwds={'label': "Rural-Urban Population Difference", 'orientation': "vertical"})

ax.set_title("Distribution of Rural and Urban Populations Across States")
ax.set_axis_off()
plt.show()


# Now I want to generate the same map, except with the sex ratio of each state

# In[26]:


import matplotlib.pyplot as plt

# Plotting the choropleth map
fig, ax = plt.subplots(1, 1, figsize=(12, 8))

# Plot the choropleth map showing population variation
merged_data.plot(column='Sex ratio', cmap='plasma', ax=ax, legend=True,
                 legend_kwds={'label': "Sex Ratio by State", 'orientation': "vertical"})

plt.title("Sex Ratio Across Indian States")
color_continuous_scale='Viridis_r'
leg = ax.get_legend()
ax.set_axis_off()
plt.show()


# Lastly, a map showcasing the density of each state per kilometer squared. 

# In[27]:


fig, ax = plt.subplots(1, 1, figsize=(12, 8))

color_scale_range = [merged_data['Density (per km2)'].min(), merged_data['Density (per km2)'].max()]

# Plot the choropleth map showing population variation with adjusted color scale range
merged_data.plot(column='Density (per km2)', cmap='coolwarm', ax=ax, legend=True,
                 legend_kwds={'label': "Density by State", 'orientation': "vertical"},
                 vmin=color_scale_range[0], vmax=color_scale_range[1])

plt.title("Population Density Across Indian States")
leg = ax.get_legend()
ax.set_axis_off()
plt.show()


# Map showcasing the male, female and total population of India's choropleth map side to side

# In[28]:


fig, axes = plt.subplots(1, 3, figsize=(18, 6))  # Adjust figsize as needed for better visualization

# Parameters to compare: Population, Male population, Female population
parameters = ['Male', 'Female','Population']
titles = ['Male Population', 'Female Population','Total Population']
cmaps = ['Blues', 'Purples','binary']  # Colormaps for better differentiation

for i, param in enumerate(parameters):
    ax = axes[i]
    
    # Plot choropleth map for each parameter
    merged_data.plot(column=param, cmap=cmaps[i], legend=True,
                     legend_kwds={'label': titles[i], 'orientation': "vertical"}, ax=ax)
    
    ax.set_title(titles[i])
    ax.set_axis_off()

plt.tight_layout()
plt.show()


# The maps generated above give a great visualization of the different attributes relating to each state of India. However, I want to create a more interactive map. I am proceeding to create a choropleth map where we can hover our mouse over the map to get specific data. 

# Firstly, I have plotted a geographic map which shows the population and Area of the state when you hover your mouse over it

# In[29]:


import plotly.express as px

# Plotting the interactive choropleth map with hover information
fig = px.choropleth(
    merged_data,
    geojson=merged_data.geometry,
    locations=merged_data.index,
    color='Population',
    projection="mercator",
    hover_name='st_nm',  # State name on hover
    hover_data={'Population': True, 'Area(km2)': True},
    color_continuous_scale='Viridis_r', # Additional data on hover
)

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(title='Population Variation Across Indian States')
fig.show()


# Now, I have generated an interactive map with the Sex Ratio of each state 

# In[30]:


# Define the range for the color scale (modify this based on your data range)

color_scale_range = [800, 1000]  # Example range for sex ratio values

# Plotting the interactive choropleth map with hover information
fig = px.choropleth(
    merged_data,
    geojson=merged_data.geometry,
    locations=merged_data.index,
    color='Sex ratio',
    projection="sinusoidal",
    hover_name='st_nm',  # State name on hover
    hover_data={'Male': True, 'Female': True, 'Difference between male and female': True, 'Sex ratio': True},
    color_continuous_scale='Viridis_r',
    range_color=color_scale_range,# Set the custom range for the color scale
)

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(title='Sex Ratio Variation each State')
fig.show()


# Plotting area of each state over the interactive map

# In[31]:


# Plotting the interactive choropleth map with hover information

fig = px.choropleth(
    merged_data,
    geojson=merged_data.geometry,
    locations=merged_data.index,
    color='Area(km2)',
    projection="sinusoidal",
    hover_name='State',  # State name on hover
    hover_data={'Area(km2)','Density (per km2)'},
    color_continuous_scale='Viridis_r',# Set the custom range for the color scale
)

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(title='Total Area of each State Across Indian States')
fig.show()


# Generating map of population density of each map

# In[33]:


import numpy as np

# Define a logarithmic color scale range
color_scale_range_log = [np.log(merged_data['Density (per km2)'].min()), np.log(merged_data['Density (per km2)'].max())]

# Plotting with logarithmic color scale
fig = px.choropleth(
    merged_data,
    geojson=merged_data.geometry,
    locations=merged_data.index,
    color=np.log(merged_data['Density (per km2)']),
    projection="sinusoidal",
    hover_name='State',
    hover_data={'Area(km2)', 'Density (per km2)'},
    color_continuous_scale='Viridis_r',
    range_color=color_scale_range_log,
    color_continuous_midpoint=np.mean(color_scale_range_log),
)

# Update geos and layout, then display
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(title='Population Density variation across India')
fig.show()


# In[ ]:




