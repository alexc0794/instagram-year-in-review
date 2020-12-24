import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from parsers.stories import StoriesParser, WEEKDAYS

stories_parser = StoriesParser(username='')
YEARS = ['2017', '2018', '2019', '2020']
frequencies = []
years = []
weekdays = []
for year in YEARS:
    stories_parser.process(year=year)
    frequencies += stories_parser.weekday_to_story_frequency
    years += [year] * len(stories_parser.weekday_to_story_frequency)
    weekdays += WEEKDAYS

app = dash.Dash(__name__)
df = pd.DataFrame({
    "Day": weekdays,
    "Frequency": frequencies,
    "Years": years
})
fig = px.bar(df, x="Day", y="Frequency", color="Years", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Instagram Stories by Weekday'),

    html.Div(children='''
        Charted across the past few years
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
