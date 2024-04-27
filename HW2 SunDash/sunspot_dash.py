from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# making the app
app = Dash(__name__)
app.layout = html.Div([
    # Naming the Dash
    html.H1('SunDash'),

    # connecting dash to the both sunspots functions
    # making the two graphs side by side
    html.Div(children=[
        dcc.Graph(
            id='ss_counts',
            style={'display': 'inline-block'
                   }),
        dcc.Graph(
            id='ss_cycles',
            style={'display': 'inline-block'
                   })
    ]),

    # creating the sliders and connecting them to the function
    # making the two sliders side by side
    html.Div(children=[

        # adding sliders for years and cycles
        # i couldn't figure out a way to make the titles side by side
        # AND the sliders side by side with html,
        # which is the title of the sliders is condensed into one html line
        html.P('# yrs & # cycles'),
        html.Div((dcc.Slider(id='yrs', min=1749, max=2023, step=137, value=2023,
                             marks={i: '{}'.format(i) for i in range(1749, 2023, 30)})),
                 style={'width': '40%', 'display': 'inline-block'}),

        # where i originally tried to put the html.P('# cycles') line
        html.Div(dcc.Slider(id='cyc', min=5, max=15, step=1, value=11),
                 style={'width': '40%', 'display': 'inline-block'}),

        # adding slider for months
        html.P("# months"),
            html.Div(dcc.Slider(id='mn', min=1, max=12, step=1, value=1),
                     style={'width': '40%'})
    ]),

    # Q3: import images of realtime sun
    html.H4('RealTime Sun'),
    html.Div(children=[
        html.Img(src=r'assets/EIT171.jpeg', alt='image',
                 style={'height': '20%', 'width': '20%', 'display': 'inline-block'}),
        html.Img(src=r'assets/EIT195.jpeg', alt='image',
                 style={'height': '20%', 'width': '20%', 'display': 'inline-block'}),
        html.Img(src=r'assets/EIT284.jpeg', alt='image',
                 style={'height': '20%', 'width': '20%', 'display': 'inline-block'}),
        html.Img(src=r'assets/EIT304.jpeg', alt='image',
                 style={'height': '20%', 'width': '20%', 'display': 'inline-block'}),
        html.Img(src=r'assets/realtime_sun.jpeg', alt='image',
                 style={'height': '20%', 'width': '20%', 'display': 'inline-block'})
    ])
])

# read in data
sunspot = pd.read_csv('SN_m_tot_V2.0.csv', sep=';',
                      names=['year', 'month', 'date_frac', 'mean_tot_ss',
                             'mean_stan_dev', 'num_obs', 'def_prov'])


# connecting dash to sunspot count
@app.callback(
    Output('ss_counts', 'figure'),
    Input('yrs', 'value'),
    Input('mn', 'value')
)
def sunspot_count(yrs, mn):
    """
    :param yrs: # of years, user inputted
    :param mn: # of months, user inputted
    :return: a figure
    """

    # Q1: creating line graph of sunspot mean totals over
    # user-selected num of years
    fig = go.Figure(
        data=[go.Scatter(
            x=sunspot[sunspot.year <= yrs]['year'],
            y=sunspot['mean_tot_ss'],
            mode='lines',
            name='monthly'
        )],
        layout_title_text='# of Sunspots',
        layout_xaxis_title='Time (Years)',
        layout_yaxis_title='Sunspot Number',
        layout_width=800,
        layout_height=600
    )

    # add smoothing line
    fig.add_scatter(
        x=sunspot[sunspot.year <= yrs]['year'],
        y=(sunspot['mean_tot_ss'].rolling(12).mean())/mn,
        mode='lines',
        name='smoothed'
    )

    return fig


# connecting sunspot cycle function to dash
@app.callback(
    Output('ss_cycles', 'figure'),
    Input('cyc', 'value')
)
def sunspot_cycle(cyc):
    """
    :param cyc: # of cycles, user inputted
    :return: a figure
    """

    # Q2: making scatter plot of cycles
    fig = go.Figure(
        data=[go.Scatter(
            x=sunspot['date_frac'] % cyc,
            y=sunspot['mean_tot_ss'],
            mode='markers',
            marker=dict(size=3)
        )],
        layout_title_text='Sunspot Cycle: {}'.format(cyc),
        layout_xaxis_title='Years',
        layout_yaxis_title='# of Sunspots',
        layout_width=600,
        layout_height=600
    )

    return fig


# run the server
app.run_server(debug=True)
