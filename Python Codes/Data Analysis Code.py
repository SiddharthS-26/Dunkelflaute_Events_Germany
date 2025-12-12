# %% [markdown]
# Data review and validation

# %%
import xarray as xr
import numpy as np  
import matplotlib.pyplot as plt 
import pandas as pd

# %%

# %%
file = "germany_2024.grib"

# Load 10m wind (analysis)

ds_u10 = xr.open_dataset(
    file,
    engine="cfgrib",
    backend_kwargs={"filter_by_keys": {
        "shortName": "10u",
        "typeOfLevel": "surface",
        "dataType": "an"
    }}
)

ds_v10 = xr.open_dataset(
    file,
    engine="cfgrib",
    backend_kwargs={"filter_by_keys": {
        "shortName": "10v",
        "typeOfLevel": "surface",
        "dataType": "an"
    }}
)

ds_wind = xr.merge([ds_u10, ds_v10])

# Load solar radiation (forecast accumulated field)
ds_ssrd = xr.open_dataset(
    file,
    engine="cfgrib",
    backend_kwargs={"filter_by_keys": {
        "shortName": "ssrd",
        "typeOfLevel": "surface",
        "dataType": "fc"
    }}
)


# Merge datasets
ds = xr.merge([ds_wind, ds_ssrd], compat="override")

print(ds)

# %%

ds= ds.sortby('time')   

# 4. Fill remaining NaN values (e.g., solar night)
ds = ds.fillna(0)

print (ds)


# %%
# %%
ssrd_acc = ds['ssrd']
ssrd_diff = ssrd_acc.diff(dim='step')
ssrd_wm2 = ssrd_diff.isel(step=0) / 3600.0

# Use valid_time as the single time axis
#ssrd_wm2 = ssrd_wm2.assign_coords(time=ds["valid_time"].isel(step=0))
ssrd_wm2 = ssrd_wm2.swap_dims({"time": "time"})

ds = ds.assign(ssrd_wm2 = ssrd_wm2)

# %%
#ssrd_acc = ds['ssrd']
#ssrd_hourly_energy = ssrd_acc.diff(dim='step')
#ssrd_1h = ssrd_hourly_energy.isel(step=0)

# 4) Convert J/m² → W/m² (divide by seconds per hour)
#ssrd_wm2 = ssrd_1h / 3600.0

# 6) Add this corrected variable into dataset
ds = ds.drop_vars(['ssrd'])          # remove old accumulated radiation
ds = ds.drop_vars(['step'])          # remove step dimension now that it's not needed
ds = ds.assign(ssrd_wm2=ssrd_wm2)    # add correct radiation

# Calculate wind speed
ds['wind_speed'] = np.sqrt(ds['u10']**2 + ds['v10']**2) 
print(ds)


# %%
# Select whole year timeline 
ds_4m = ds.sel(time=slice("2024-01-01", "2024-12-31"))

# 2) Compute spatial mean (average over all grid points)
ds_mean = ds_4m.mean(dim=["latitude", "longitude"], keep_attrs=True)

# 3) Convert to a Pandas DataFrame
df = ds_mean.to_dataframe()

# 4) Save to CSV
output_file = "germany_2024.csv"
df.to_csv(output_file)

print("Export complete:", output_file)
print(df.head())



