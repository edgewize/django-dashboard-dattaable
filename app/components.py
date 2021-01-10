from django_components import component
# https://pypi.org/project/django-reusable-components/


class WaveSummary(component.Component):
    def context(self, wave):
        return {
            'wave': wave,
        }

    def template(self, context):
        return "components/wave_summary/index.html"

component.registry.register(name="wave_summary", component=WaveSummary)

class WaveDetail(component.Component):
    def context(self, wave):
        return {
            'wave': wave,
        }

    def template(self, context):
        return "components/wave_detail/index.html"

component.registry.register(name="wave_detail", component=WaveDetail)

class ChartCard(component.Component):
    def context(self, title, chart):
        return {
            'title': title,
            'chart': chart
        }

    def template(self, context):
        return "components/utils/chart_card.html"

component.registry.register(name="chart_card", component=ChartCard)
