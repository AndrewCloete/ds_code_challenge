"""
References
https://stackoverflow.com/questions/53818682/pandas-read-csv-with-multiple-headers
https://stackoverflow.com/questions/22676/how-to-download-a-file-over-http
https://stackoverflow.com/questions/17834995/how-to-convert-opendocument-spreadsheets-to-a-pandas-dataframe
https://stackoverflow.com/questions/47379476/how-to-convert-bytes-data-into-a-python-pandas-dataframe#49689699
"""


from io import BytesIO
import urllib.request

import pandas as pd

WIND_DATA_URL = 'https://www.capetown.gov.za/_layouts/OpenDataPortalHandler/DownloadHandler.ashx?DocumentName=Wind_direction_and_speed_2020.ods&DatasetDocument=https%3A%2F%2Fcityapps.capetown.gov.za%2Fsites%2Fopendatacatalog%2FDocuments%2FWind%2FWind_direction_and_speed_2020.ods'

class WindDataRepository:
    def __init__(self):
        pass

    def get_as_dataframe(self) -> pd.DataFrame:
        with urllib.request.urlopen(WIND_DATA_URL) as f:
            bytes_data = BytesIO(f.read())
            df = pd.read_excel(bytes_data, engine="odf", skiprows=2, header=None)
            cols = tuple(zip(df.iloc[0], df.iloc[2]))
            header = pd.MultiIndex.from_tuples(cols, names=['area', 'metric'])
            df.drop([0,1,2], inplace=True)
            df.columns = header
            return df
