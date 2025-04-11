import pandas as pd

# Load the dataset
df = pd.read_csv("US_Accidents.csv")

# Display the first few rows
print(df.head())

# Check for missing values
print(df.isnull().sum())

# Get basic statistics
print(df.describe())

# Drop unnecessary columns
df.drop(columns=['ID', 'Source', 'Wind_Chill(F)', 'Number'], inplace=True)

# Convert datetime columns
df['Start_Time'] = pd.to_datetime(df['Start_Time'])
df['End_Time'] = pd.to_datetime(df['End_Time'])

# Fill missing values
df.fillna({'Weather_Condition': 'Unknown', 'Sunrise_Sunset': 'Unknown'}, inplace=True)

# Extract useful time-based features
df['Hour'] = df['Start_Time'].dt.hour
df['DayOfWeek'] = df['Start_Time'].dt.dayofweek
df['Month'] = df['Start_Time'].dt.month

import seaborn as sns
import matplotlib.pyplot as plt

sns.histplot(df['Hour'], bins=24, kde=True)
plt.title("Accidents by Hour of the Day")
plt.xlabel("Hour of the Day")
plt.ylabel("Accident Count")
plt.show()

top_weather_conditions = df['Weather_Condition'].value_counts().nlargest(10)

plt.figure(figsize=(10, 5))
sns.barplot(x=top_weather_conditions.index, y=top_weather_conditions.values)
plt.xticks(rotation=45)
plt.title("Top 10 Weather Conditions in Accidents")
plt.ylabel("Number of Accidents")
plt.show()

sns.countplot(y=df['Side'], palette="coolwarm")
plt.title("Accidents Based on Road Side")
plt.xlabel("Count")
plt.show()

import folium
from folium.plugins import HeatMap

# Sample a subset for better performance
df_sample = df[['Start_Lat', 'Start_Lng']].dropna().sample(10000)

# Create a map centered on the US
map_accidents = folium.Map(location=[37.0902, -95.7129], zoom_start=4)

# Add heatmap layer
HeatMap(data=df_sample.values, radius=10).add_to(map_accidents)

# Display the map
map_accidents
