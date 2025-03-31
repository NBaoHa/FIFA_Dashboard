import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Load the FIFA World Cup data
# Winners and their # of wins
df_winners = pd.DataFrame({
    'Country': ['Brazil', 'Germany', 'Italy', 'Argentina', 'France', 'Uruguay', 'England', 'Spain'],
    'Wins': [5, 4, 4, 3, 2, 2, 1, 1]
})

# Runner Ups and their # of running up
df_runners_up = pd.DataFrame({
    'Country': ['Germany', 'Argentina', 'Netherlands', 'Italy', 'Brazil', 'France', 'Czech Republic', 'Hungary'],
    'RunnerUps': [4, 3, 3, 2, 2, 1, 2, 2]
})

# Additional dataset with winners and runner-ups per year
df_runners_up_years = pd.DataFrame({
    'Year': [2018, 2014, 2010, 2006, 2002, 1998, 1994, 1990, 1986, 1982],
    'Winner': ['France', 'Germany', 'Spain', 'Italy', 'Brazil', 'France', 'Brazil', 'Germany', 'Argentina', 'Italy'],
    'Runner-up': ['Croatia', 'Argentina', 'Netherlands', 'France', 'Germany', 'Brazil', 'Italy', 'Argentina', 'Germany', 'West Germany']
})

# Ensure Germany and West Germany are treated as one
df_runners_up_years.replace({'West Germany': 'Germany'}, inplace=True)

# Create a choropleth map for winners
fig_winners = px.choropleth(df_winners, locations='Country', locationmode='country names',
                             color='Wins', hover_name='Country',
                             color_continuous_scale='Blues',
                             title='FIFA World Cup Winners by Country')

# Create a choropleth map for runner-ups
fig_runners_up = px.choropleth(df_runners_up, locations='Country', locationmode='country names',
                               color='RunnerUps', hover_name='Country',
                               color_continuous_scale='Reds',
                               title='FIFA World Cup Runner-Ups by Country')

# Define callback functions: Support Graphical User Interface Functions 

def display_wins(country):
    if country:
        wins = df_winners[df_winners['Country'] == country]['Wins'].values[0]
        return f'{country} has won {wins} times.'
    return ''

def display_runner_ups(country):
    if country:
        runner_ups = df_runners_up[df_runners_up['Country'] == country]['RunnerUps'].values[0]
        return f'{country} has been runner-up {runner_ups} times.'
    return ''

def display_winner_runner_up(year):
    if year:
        row = df_runners_up_years[df_runners_up_years['Year'] == year]
        winner = row['Winner'].values[0]
        runner_up = row['Runner-up'].values[0]
        return f'In {year}, {winner} won the World Cup, and {runner_up} was the runner-up.'
    return ''


# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('FIFA World Cup Dashboard'),
    dcc.Tabs([
        dcc.Tab(label='Winners', children=[dcc.Graph(id='choropleth-map-winners', figure=fig_winners)]),
        dcc.Tab(label='Runner-Ups', children=[dcc.Graph(id='choropleth-map-runners-up', figure=fig_runners_up)])
    ]),
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': c, 'value': c} for c in df_winners['Country']],
        placeholder='Select a country'
    ),
    html.Div(id='win-output'),
    dcc.Dropdown(
        id='runner-up-dropdown',
        options=[{'label': c, 'value': c} for c in df_runners_up['Country']],
        placeholder='Select a country'
    ),
    html.Div(id='runner-up-output'),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': str(y), 'value': y} for y in df_runners_up_years['Year']],
        placeholder='Select a year'
    ),
    html.Div(id='year-output')
])

@app.callback(
    [
        dash.Output('win-output', 'children'),
        dash.Output('runner-up-output', 'children'),
        dash.Output('year-output', 'children')
    ],
    [
        dash.Input('country-dropdown', 'value'),
        dash.Input('runner-up-dropdown', 'value'),
        dash.Input('year-dropdown', 'value')
    ]
)
def update_outputs(country, runner_up_country, year):
    win_text = display_wins(country)
    runner_up_text = display_runner_ups(runner_up_country)
    year_text = display_winner_runner_up(year)
    return win_text, runner_up_text, year_text

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8051)
