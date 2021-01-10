import app.lib.hydrofunctions.__init__ as hydrofunctions
import pandas as pd
import plotly.io as pio
import plotly.express as px


def format_site_data(hf_request, freq='D'):
    meta = hf_request.meta
    df = hf_request.df('discharge').reset_index()
    df['date'] = df['datetimeUTC'].apply(lambda x: pd.to_datetime(x.date()))
    df = df.drop('datetimeUTC', 1)
    # import pdb; pdb.set_trace()
    chart = px.line(
        df, x="date", y=df.columns[0], title=meta)
    chart_html = pio.to_html(chart)
    discharge_col = df.columns[0]
    format_data = df.rename(
        columns={discharge_col: 'discharge'}).set_index('date')
    aggregate_dates = format_data.resample(freq).mean()
    aggregate_dates.index = [str(i.date()) for i in aggregate_dates.index]
    data = {
        'meta': meta,
        'timeSeries': aggregate_dates.to_dict(),
        'chart': chart_html
    }
    return data


if __name__ == '__main__':
    flow = hydrofunctions.NWIS("13206000",  'dv', period="P10D")