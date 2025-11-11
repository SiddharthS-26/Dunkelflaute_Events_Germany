# %%
import pandas as pd
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt 

# %%
df = pd.read_csv("germany_2018_hourly_data.csv", index_col=0, parse_dates=True)

# %%
df['valid_time'] = pd.to_datetime(df['valid_time'])

df = df.sort_values('valid_time')

df = df[['valid_time', 'wind_speed', 'ssrd_wm2']]

# %%
# Defination of the dunkelflaute period 

df['low_wind'] = df['wind_speed'] < 2.5
df['low_solar'] = df['ssrd_wm2'] < 25

# Combined Dunkelflaute condition
df['dunkelflaute'] = df['low_wind'] & df['low_solar']


# %%
df['block'] = (df['dunkelflaute'] != df['dunkelflaute'].shift()).cumsum()

events = df[df['dunkelflaute']].groupby('block').agg(start=('valid_time', 'min'),
                                                      end=('valid_time', 'max'),
                                                      duration_hours=('valid_time',lambda x:len(x))).reset_index(drop=True)

events = events[events['duration_hours'] >= 24]

print(len(events))

# %%
# Plot data for a events of interest

plt.figure(figsize=(14,5))
plt.plot(df['valid_time'], df['wind_speed'], label='Wind Speed (m/s)')
plt.plot(df['valid_time'], df['ssrd_wm2'], label='Solar Radiation (W/m²)')

for _, event in events.iterrows():
    plt.axvspan(event['start'], event['end'], color='red', alpha=0.3)

plt.title("Dunkelflaute Events in Germany 2018")
plt.xlabel("Time")
plt.ylabel("Wind Speed (m/s) & Solar Radiation (W/m²)")
plt.legend()
plt.show()


