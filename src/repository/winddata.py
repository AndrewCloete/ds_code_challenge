"""
References
https://stackoverflow.com/questions/53818682/pandas-read-csv-with-multiple-headers
https://stackoverflow.com/questions/22676/how-to-download-a-file-over-http
https://stackoverflow.com/questions/17834995/how-to-convert-opendocument-spreadsheets-to-a-pandas-dataframe
https://stackoverflow.com/questions/47379476/how-to-convert-bytes-data-into-a-python-pandas-dataframe#49689699
"""


from io import BytesIO
import urllib.request
import pytz

import pandas as pd

WIND_DATA_URL = 'https://www.capetown.gov.za/_layouts/OpenDataPortalHandler/DownloadHandler.ashx?DocumentName=Wind_direction_and_speed_2020.ods&DatasetDocument=https%3A%2F%2Fcityapps.capetown.gov.za%2Fsites%2Fopendatacatalog%2FDocuments%2FWind%2FWind_direction_and_speed_2020.ods'

"""
Hardcoding the assumed timezone for now. Would obviously not do this in production.
"""
TIMEZONE_NAME = 'Africa/Johannesburg'

class WindDataRepository:
    def __init__(self):
        pass

    def get_bytes(self) -> bytes:
        with urllib.request.urlopen(WIND_DATA_URL) as f:
            return BytesIO(f.read())

    def get_as_dataframe(self) -> pd.DataFrame:
        bytes_data = self.get_bytes() 
        df = pd.read_excel(bytes_data, engine="odf", skiprows=2, header=None)


        # I dont have the krag to deal with MultiIndex headers now. 
        # cols = tuple(zip(df.iloc[0], df.iloc[2]))
        # header = pd.MultiIndex.from_tuples(cols, names=['area', 'metric'])
        df.iloc[:, 0] = df.iloc[:, 0].apply(lambda x: x.strip() if x == x else 'none')
        cols = [f"{k1}-{k2}" for k1, k2 in zip(df.iloc[0], df.iloc[1])]
        cols[0] = 'date'
        df.drop([0,1,2], inplace=True)
        df.columns = cols
        # Parse date, and drop rows with invalid dates
        df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y %H:%M', errors='coerce')
        df = df[~df['date'].isna()]
        df['date'] = df['date'].dt.tz_localize(pytz.timezone(TIMEZONE_NAME))
        return df

