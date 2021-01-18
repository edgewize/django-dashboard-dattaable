import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import numpy as np

class NationalWeatherService():
    def __init__(self):
        self.base_url = 'https://water.weather.gov/ahps2/hydrograph_to_xml.php'

    def _format_columns(self, columns):
        format_cols = []
        for i in columns:
            col = i.replace('|', '').replace(
                '-', '').replace('(', '_').replace(')', '').lower()
            format_cols.append(col)
        return format_cols

    def gage_forecast(self, gage_id):
        params = {
            'gage': gage_id,
            'output': 'tabular'
        }
        req = requests.get(self.base_url, params=params)
        soup = BeautifulSoup(req.text, 'html.parser')
        table = soup.find('table')
        dfs = pd.read_html(str(table))
        actual = dfs[1]
        actual.columns = self._format_columns(actual.loc[1])
        actual = actual.drop([0, 1])
        forecast = dfs[2]
        forecast.columns = self._format_columns(forecast.loc[1])
        forecast = forecast.rename(
            columns={'flow': 'forecast_flow', 'stage': 'forecast_stage'})
        forecast = forecast.drop([0, 1])
        data = actual.set_index('date_utc').join(
            forecast.set_index('date_utc'), how='outer').reset_index()
        today = datetime.datetime.now()
        data['date_utc'] = data['date_utc'].apply(
            lambda x: pd.to_datetime(f"{x.split(' ')[0]}/{today.year}"))
        for col in ['flow', 'forecast_flow']:
            data[col] = data[col].apply(lambda x: x.split('c')[0] if type(
                x) == str else x).apply(lambda x: str(x).split('k')[0])
            data[col] = pd.to_numeric(data[col].apply(
                lambda x: np.nan if x == 'nan' else x))
        data = data.set_index('date_utc').resample('d').mean()
        return data


if __name__ == '__main__':
    gage = 'bigi1'
    nws = NationalWeatherService()
    data = nws.gage_forecast(gage)
    print(data)
