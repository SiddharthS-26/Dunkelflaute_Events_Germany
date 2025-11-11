# %% [markdown]
# Hello All, 
# 
# This codes connects with CDSAPI and gathers our wind speed and solar radiation downwards data which we use for further analysis. 
# 
# The code is created with the help and references from the api documentation available at the CDS website and along with some LLM use to resolve this Bug and other queries. 
# 
# This code will save the data in a grib format for the user to work on further analysis for the detection of dunkelflaute events, and save its with the naming convention provided at the end of the application. 

# %%
import cdsapi 

client = cdsapi.Client()

dataset = "reanalysis-era5-single-levels"

for year in range(2018, 2025):  # 2018 to 2024
    request = {
        "product_type": ["reanalysis"],
        "variable": [
            "10m_u_component_of_wind",
            "10m_v_component_of_wind",
            "surface_solar_radiation_downwards"
        ],
        "year": [str(year)],
        "month": [
            "01", "02", "03",
            "04", "05", "06",
            "07", "08", "09",
            "10", "11", "12"
        ],
        "day": [
            "01", "02", "03",
            "04", "05", "06",
            "07", "08", "09",
            "10", "11", "12",
            "13", "14", "15",
            "16", "17", "18",
            "19", "20", "21",
            "22", "23", "24",
            "25", "26", "27",
            "28", "29", "30",
            "31"
        ],
        "time": [
            "00:00", "01:00", "02:00",
            "03:00", "04:00", "05:00",
            "06:00", "07:00", "08:00",
            "09:00", "10:00", "11:00",
            "12:00", "13:00", "14:00",
            "15:00", "16:00", "17:00",
            "18:00", "19:00", "20:00",
            "21:00", "22:00", "23:00"
        ],
        "data_format": "grib",
        "download_format": "unarchived",
        "area": [55, 5, 47, 15]
    }

    print(f"\n➡️ Downloading Germany ERA5 for {year} ...")
    client.retrieve(dataset, request, f"germany_{year}.grib")
    print(f"✅ Saved file: germany_{year}.grib")



