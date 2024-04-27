"""
Avril Mauro, ...
DS 3500 Final Project
S&P 500 Stock Analysis
April 19th, 2023

This file deploys the final dashboard for
analysis of stocks in the S&P 500
"""

from dash import Dash, dcc, html, Input, Output
from utils import num_filter
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import charts

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# S&P Industries by Ticker and Company
industry_df = pd.read_csv('sp500_Industries.csv').rename(columns={'Symbol': 'Ticker'})
sector_list = list(set(industry_df['Sector'].values)) + ['All']

# S&P Individual Stock Prices
price_df = pd.read_csv('sp500_Price.csv').drop('Unnamed: 0', axis=1)

# S&P Individual Stock Prices and their industry (sector)
close_df = pd.merge(price_df, industry_df, on='Ticker')

# S&P 500 Index Price (2010 to 2020)
index_df = pd.read_csv('spIndex_Price.csv')
index_df = num_filter(index_df, 'Date', ['2010-01-01', '2020-12-31'])

# LAYOUT
app.layout = dbc.Container([
    # GRAPH: LINE CHART
    dbc.Row([
        dbc.Col(html.Div([
            html.H1('S&P 500 Stock Analysis'),
            dcc.Graph(id='BubbleSectors',
                      figure=charts.display_bubble_chart()),
        ]), width=9),
        dbc.Col(html.Div([
            html.H4('Bubble Chart'),
            html.P('The S&P500 is a collection of stocks divided among 11 industry sectors'),
            html.P('bubble size: number of stocks which are in a specific industry sector'),
            html.P('y-axis: aggregated average closing price of all stocks in one sector during 2020'),
            html.P('x-axis: percent growth in closing price (aggregated average of 2020 vs. 2010)'),
        ], style={"marginTop": 100}, ), width=3),
    ]),

    dbc.Row([
        # SLIDER: range of years
        dbc.Col(html.Div([
            html.P('Start and End Year'),
            dcc.Input(id='Year0', type='number', placeholder=2010, min=2010, max=2020),
            dcc.Input(id='Year1', type='number', placeholder=2020, min=2010, max=2020),
            dcc.Graph(id='Bullet'),
        ]), width=3),
        dbc.Col(html.Div([
            html.P("Industry"),
            dcc.Dropdown(sector_list, id='IndustryPicker', placeholder='All'),
            dcc.Graph(id='Table'),
        ]), width=9),
    ]),
    dbc.Row([
        # SLIDER: range of years
        dbc.Col(html.Div([
            dcc.Graph(id='Candlestick'),
        ]), width=6),
        dbc.Col(html.Div([
            dcc.Graph(id='Top_6'),
        ]), width=6),
    ])])


@app.callback(
    Output('Bullet', 'figure'),
    Input('Year0', 'value'),
    Input('Year1', 'value'),
    Input('IndustryPicker', 'value'))
def update_bullet(year0, year1, industry):
    # set defaults
    if year0 is None:
        year0 = 2010

    if year1 is None:
        year1 = 2020

    if industry is None:
        industry = 'All'

    if industry == 'All':
        # filter on years for the entire S&P index
        t0 = num_filter(index_df, 'Date', [f'{year0}-01-01', f'{year0}-12-31'])
        t1 = num_filter(index_df, 'Date', [f'{year1}-01-01', f'{year1}-12-31'])

        # retrieve closing price of year0 and year1 for entire S&P Index
        p0 = ((t0['Close']).mean())
        p1 = ((t1['Close']).mean())

    else:
        # filter on years for the stock specific data
        t0 = num_filter(close_df, 'Date', [f'{year0}-01-01', f'{year0}-12-31'])
        t1 = num_filter(close_df, 'Date', [f'{year1}-01-01', f'{year1}-12-31'])

        # retrieve avg adjusted closing price per industry for year0
        c0 = pd.DataFrame(t0.groupby('Sector').mean(numeric_only=True)['Adj Close']).reset_index()
        c0.columns = ['Sector', 'Adj Close']

        # retrieve avg adjusted closing price per industry for year1
        c1 = pd.DataFrame(t1.groupby('Sector').mean(numeric_only=True)['Adj Close']).reset_index()
        c1.columns = ['Sector', 'Adj Close']

        # retrieve closing price of year0 and year1 for specific industry
        p0 = (c0[c0.Sector == industry]['Adj Close']).iloc[0]
        p1 = (c1[c1.Sector == industry]['Adj Close']).iloc[0]

    # plot the bullet chart
    fig = go.Figure(go.Indicator(
        mode="number+delta",
        value=p1,
        title={"text": f"{industry} Sector<br><span style='font-size:0.8em; \
                              color:gray'>Change in Avg. Closing Price</span><br><span \
                              style='font-size:0.8em;color:gray'>{year0} to {year1}</span>"},
        number={'prefix': "$"},
        delta={'position': "top", 'reference': p0},
        domain={'x': [0, 1], 'y': [0, 1]})
    )

    return fig


@app.callback(
    Output('Table', 'figure'),
    Input('Year0', 'value'),
    Input('Year1', 'value'),
    Input('IndustryPicker', 'value'))
def update_table(year0, year1, industry):
    df = pd.DataFrame()

    # set defaults
    if year0 is None:
        year0 = 2010

    if year1 is None:
        year1 = 2020

    if industry is None:
        industry = 'All'

    # retrieve data from year0 and year1 using stock specific dataframe
    t0 = num_filter(price_df, 'Date', [f'{year0}-01-01', f'{year0}-12-31'])
    t1 = num_filter(price_df, 'Date', [f'{year1}-01-01', f'{year1}-12-31'])

    # retrieve avg adjusted closing price for each ticker in year 1
    year0_close = pd.DataFrame(t0.groupby('Ticker').mean(numeric_only=True)['Adj Close']).reset_index()
    year0_close.columns = ['Ticker', f'{year0} Adj Close']

    # retrieve avg adjusted closing price for each ticker in year 2
    year1_close = pd.DataFrame(t1.groupby('Ticker').mean(numeric_only=True)['Adj Close']).reset_index()
    year1_close.columns = ['Ticker', f'{year1} Adj Close']

    # merge year0 and year1 dataframes and calculate change in closing prices
    df = pd.merge(year0_close, year1_close, how='outer')
    df['Change'] = df[f'{year1} Adj Close'] - df[f'{year0} Adj Close']
    df = df.round(2)

    # add sector label to the tickers
    df = pd.merge(df, industry_df, on='Ticker')
    df = df.iloc[:, [-1, 0, -2, 1, 2, 3]]

    if industry != 'All':
        # filter by sector and display table (positive change = green, negative change = red)
        df = df[df.Sector == industry]

    fill_color = ['#E6F2FD' for _ in range(len(df.columns) - 1)]
    change_color = ['#D0FDC1' if change >= 0 else '#FFC2C2' for change in df['Change']]
    fill_color.append(change_color)

    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                    font=dict(color='rgb(45,45,45)'),
                    ),
        cells=dict(values=list(df.to_dict('list').values()),
                   font=dict(color='black'),
                   fill=dict(color=fill_color)))])

    return fig


@app.callback(
    Output('Candlestick', 'figure'),
    Input('IndustryPicker', 'value')
)
def update_candlestick(industry):
    """ create candlestick chart """

    # set default industry
    if industry is None:
        industry = 'All'

    if industry == 'All':
        fig = go.Figure(data=[go.Candlestick(x=index_df['Date'],
                                             open=index_df['Open'],
                                             high=index_df['High'],
                                             low=index_df['Low'],
                                             close=index_df['Close'])])

        fig.update_layout(
            title={
                'text': "S&P 500 Stock Price"})
    else:
        # closing Prices per Industry
        sector_prices = pd.DataFrame(close_df.groupby(['Sector', 'Date']).mean(numeric_only=True)).reset_index()
        sector_prices = sector_prices[sector_prices['Sector'] == industry]
        fig = go.Figure(data=[go.Candlestick(x=sector_prices['Date'],
                                             open=sector_prices['Open'],
                                             high=sector_prices['High'],
                                             low=sector_prices['Low'],
                                             close=sector_prices['Close'])])

        fig.update_layout(
            title={
                'text': f'{industry} Stock Price'})

    return fig


@app.callback(
    Output('Top_6', 'figure'),
    Input('IndustryPicker', 'value')
)
def update_top_6(industry):
    """ create top 6 companies line graph """

    # set default industry
    if industry is None:
        industry = 'All'

    if industry == 'All':
        ticker_prices = pd.DataFrame(price_df.groupby(['Ticker']).mean(numeric_only=True)).reset_index()
        tickers = list(ticker_prices.sort_values(by=['Adj Close'], ascending=False).head(6)['Ticker'])
        top_6 = price_df.loc[price_df['Ticker'].isin(tickers), :]
        fig = px.area(top_6, x="Date", y="Close", color="Ticker", facet_col="Ticker", facet_col_wrap=2,
                      title='Top 6 Performing Stocks in S&P 500')

    else:
        sector_df = close_df[close_df['Sector'] == industry]
        sector_prices = pd.DataFrame(sector_df.groupby(['Ticker']).mean(numeric_only=True)).reset_index()
        tickers = list(sector_prices.sort_values(by=['Adj Close'], ascending=False).head(6)['Ticker'])
        top_6 = price_df.loc[price_df['Ticker'].isin(tickers), :]
        fig = px.area(top_6, x="Date", y="Close", color="Ticker", facet_col="Ticker", facet_col_wrap=2,
                      title=f'Top 6 Performing Stocks in {industry} Sector')

    return fig


def main():
    app.run_server(debug=True, port=8051)


if __name__ == '__main__':
    main()
