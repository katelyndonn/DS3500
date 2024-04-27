import pandas as pd
import plotly.express as px



def getstickers(industry_data, ticker=None, sector=None):
    """ returns all tickers associated with one industry name """
    if ticker is None:
        ticker='A'

    if sector is None:
        tdata = industry_data[industry_data.Ticker == ticker]
        sector = tdata.Sector.values[0]

    tdata = industry_data[industry_data.Sector == sector]
    tickers = list(tdata.Ticker.values)
    return tickers


def getsector(industry_data, ticker):
    """ returns the industry name for one ticker label """
    tdata = industry_data[industry_data.Ticker == ticker]
    tsector = tdata.Sector.values[0]
    return tsector


def getname(industry_data, ticker):
    """ returns the company name for one ticker label """
    tdata = industry_data[industry_data.Ticker == ticker]
    tname = tdata.Name.values[0]
    return tname


def priceovertime(t, add_sectors, sector_data, stock_data, industry_data, x, y):
    """ interactive line plot for individual stock and overall industry performance
            t = list of tickers
            add_sectors = list of additional industry names
            x = 'Date'
            y = 'Adj Close'
    """

    # plots industry prices of the first stock in the t list
    tsector = getsector(industry_data, t[0])
    dateclose = sector_data[sector_data.Sector == tsector].drop('Sector', axis=1)
    dateclose.columns = [x, tsector]

    # for each stock in t, get the prices over time and merge into a dataframe
    for ticker in t:
        tsector, tname = getsector(industry_data, ticker), getname(industry_data, ticker)
        tclose = stock_data[stock_data.Ticker == ticker].drop('Ticker', axis=1)
        tclose.columns = [x, tname]
        dateclose = pd.merge(dateclose, tclose, how='outer')
        print(dateclose)

    # for each additional sector, get prices over time and merge into a dataframe
    if add_sectors is not None:
        for industry in add_sectors:
            industry_prices = sector_data[sector_data.Sector == industry].drop('Sector', axis=1)
            industry_prices.columns = [x, industry]
            dateclose = pd.merge(dateclose, industry_prices)

    # plot all the lines
    fig = px.line(dateclose, x=x, y=dateclose.columns[2:],
                  color_discrete_sequence=px.colors.qualitative.Dark2)

    fig.update_traces(opacity=.5)
    fig.add_scatter(x=dateclose[x], y=dateclose[tsector], name=tsector,
                    mode='lines', line=dict(width=3, color=px.colors.qualitative.Safe[9]))
    fig.update_layout(xaxis_title='Date', yaxis_title='Closing Price (Dollars)',
                      title={'text': 'Stock Prices Over Time', 'font':{'size':25},
                             'x': .5, 'xanchor': 'center'},
                      legend_title='Company or Sector Name',
                      font=dict(size=18))

    # display plot
    fig.show()


def display_bubble_chart():

    df = pd.read_csv('sp500_growth.csv')

    fig = px.scatter(df,
                     x='Growth (%)',
                     y='Close',
                     size='Count',
                     color='Growth (%)',
                     color_continuous_scale=px.colors.sequential.Viridis,
                     hover_name='Sector',
                     size_max=80,
                     text='Sector',
                     opacity=0.5
                     )

    # title the graph and label the axes
    fig.update_layout(xaxis_title='Percent Growth (2010 to 2020)',
                      yaxis_title=f'Average Closing Price (2020)',
                      title={'text': 'Stock Growth by Industry from 2010 to 2020',
                             'font': {'size': 20}, 'x': .5, 'xanchor': 'center'},
                      font=dict(size=10))

    return fig