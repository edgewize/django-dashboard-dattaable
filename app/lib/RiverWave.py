import app.lib.hydrofunctions.__init__ as hydrofunctions
import pandas as pd
import plotly.io as pio
import plotly.express as px
from app.models import Wave


class Analysis():
    def change_over_days(self, df, periods=5):
        df['rolling_avg'] = df['CFS'].rolling(window=periods).mean()
        most_recent = df.loc[df.index.max()]['CFS']
        compare_to = df.loc[df.index[-periods]]['CFS']
        cfs_diff = most_recent - compare_to
        pct_diff = (cfs_diff / compare_to) * 100
        return {
            'cfs_diff': cfs_diff,
            'pct_diff': pct_diff,
            'periods': periods
        }

    def time_in_session(self, df, session_level):
        cfs = df['CFS']
        df['in_session'] = cfs.apply(
            lambda x: 1 if x > session_level else 0)
        df['session_rate'] = cfs.apply(
            lambda x: x / session_level)
        pct_in_session = (df.sum()['in_session'] / len(df)) * 100
        # df = df.set_index('datetimeUTC')['in_session'].to_frame().T
        df['month'] = df['datetimeUTC'].apply(
            lambda x: f'{x.year}{x.month}')
        df['day'] = df['datetimeUTC'].apply(lambda x: x.day)
        df = df.groupby(['month', 'day']).mean()['session_rate'].unstack()
        chart = pio.to_html(px.imshow(df))
        return {
            'pct_in_session': pct_in_session,
            'chart': chart
        }


class View(hydrofunctions.NWIS):

    def avg_cfs(self, freq='D'):
        df = pd.DataFrame(self.df(), copy=True)
        aggregate_dates = df.resample(freq).mean()
        df = aggregate_dates.reset_index().rename(
            columns={df.columns[0]: 'CFS'})
        return df

    def chart(self, freq='D'):
        df = self.avg_cfs(freq)
        chart = px.line(
            df, x="datetimeUTC", y='CFS')
        chart_html = pio.to_html(chart)
        return chart_html

    def settings(self):
        site_id = str(self.site)
        return Wave.objects.get(site_id=site_id)

    def determine_status(self, cfs):
        settings = self.settings()
        if cfs > settings.awesome_level:
            return 'Wave is epic'
        elif cfs > settings.in_level:
            return 'Wave is in'
        else:
            return 'Wave is out'

    def info(self):
        info = self.meta[list(self.meta.keys())[0]]
        settings = self.settings()
        avg_cfs = self.avg_cfs()
        current = avg_cfs.loc[avg_cfs.index.max()]['CFS']
        info['site_id'] = self.site
        info['change'] = Analysis().change_over_days(avg_cfs)
        info['current'] = current
        info['settings'] = settings
        info['session'] = Analysis().time_in_session(
            avg_cfs, settings.in_level)
        info['status'] = self.determine_status(current)
        info['pct_in_level'] = (current / settings.in_level) * 100
        info['pct_awesome_level'] = (current / settings.awesome_level) * 100
        return info

    def build(self):
        info = self.info()
        chart = self.chart('D')
        return {
            'info': info,
            'chart': chart
        }


if __name__ == "__main__":
    wave = RiverWave("13206000",  'dv', period="P10D")
    data = wave.chart()
