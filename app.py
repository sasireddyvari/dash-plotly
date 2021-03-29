import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
# pip install dash pandas plotly dash-core-components dash-html-components
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
# from flask_cors import CORS, cross_origin

app = dash.Dash(__name__)
server = app.server
# reading data
df = pd.read_csv("covid_rep.csv")

df = df.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code'])[['% of Impact']].mean()
df.reset_index(inplace=True)
print(len(df['State'].value_counts()))

# App layout
app.layout = html.Div([
    html.H1("Dashboards with Plotly-Dash", style={'text-align': 'center','color': 'brown'}),
    html.P("An Interactive web application framework to build dashboards and display plotly's visualizations",
           style={'text-align': 'center','color': 'brown','font-size': 'x-large'}),
       html.Div([
                html.Div([
                    html.P("Select the year to visualize the Covid Impact of USA States:",
                           style={'font-size': 'large','color': 'maroon'}),
                ]),
                dcc.Dropdown(id="slct_year",
                 options=[
                     {"label": "2017", "value": 2017},
                     {"label": "2018", "value": 2018},
                     {"label": "2019", "value": 2019},
                     {"label": "2020", "value": 2020},
                     {"label": "2021", "value": 2021}],
                 multi=False,
                 value=2017,
                 style={'width': "30%",'margin':'5px','background-color': 'papayawhip !'}
                 ),
        ],
        style=dict(display='flex')),
    html.Div(id='output_container', children=[],style={'font-size': 'large','color': 'maroon'}),
    html.Br(),
    html.Div(children=[
            dcc.Graph(id="covid_map",figure={}, style={'align':'left','display': 'inline-block'}),
        # html.Br(),
            dcc.Graph(id="covid1_map",figure={}, style={'align': 'right', 'display': 'inline-block'}),
            html.Br(),
            dcc.Graph(id="covid2_map", figure={}, style={'align': 'right', 'display': 'inline-block'}),
            dcc.Graph(id="covid3_map", figure={}, style={'align': 'right', 'display': 'inline-block'}),
    ]),
])
# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='covid_map', component_property='figure'),
     Output(component_id='covid1_map', component_property='figure'),
     Output(component_id='covid2_map', component_property='figure'),
     Output(component_id='covid3_map', component_property='figure')
     ],
    [Input(component_id='slct_year', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The covid stats of the year : {}".format(option_slctd)

    dff = df.copy()
    dff = dff[dff["Year"] == option_slctd]
    dff = dff[dff["Affected by"] == "Covid"]

    # Plotly Express
    fig = px.choropleth(
           data_frame=dff,
           locationmode='USA-states',
           locations='state_code',
           title='Covid Analysis state wise through a grahical map',
           scope="usa",
           color='% of Impact',
           hover_data=['State', '% of Impact'],
           color_continuous_scale=px.colors.sequential.YlOrRd,
           labels={'% of Impact': '% of affect by covid'},
           template='plotly_dark',
           width=650  # figure width in pixels
           # height=600
       )

    # Plotly Graph Objects (GO)
    # fig = go.Figure(
    #      data=[go.Choropleth(
    #      locationmode='USA-states',
    #      locations=dff['state_code'],
    #      z=dff["% of Impact"].astype(float),
    #      colorscale='Reds',
    #      )]
    #  )
    # bar chart
    fig1 = px.bar(dff,
                    x='State',
                    y='% of Impact',
                    color='% of Impact',
                    range_y=[0, 100],
                    title='State Wise Covid Analysis of USA through Bar Chart',
                    color_continuous_scale=px.colors.sequential.YlOrRd,
                    width=650  # figure width in pixels
                    # height=600
                )
    fig2 = px.scatter_3d(
        data_frame=dff,
        x='Year',
        y='% of Impact',
        z='State',
        color="% of Impact",
        # color_discrete_sequence=['magenta', 'green'],
        color_discrete_map={'Europe': 'black', 'Africa': 'yellow'},
        color_continuous_scale=px.colors.sequential.YlOrRd,
        # opacity=0.3,              # opacity values range from 0 to 1
        # symbol='Year',            # symbol used for bubble
        # symbol_map={"2005": "square-open", "2010": 3},
        # size='resized_pop',       # size of bubble
        # size_max=50,              # set the maximum mark size when using size
        # log_x=True,  # you can also set log_y and log_z as a log scale
        # range_z=[9,13],           # you can also set range of range_y and range_x
        # template='ggplot2',  # 'ggplot2', 'seaborn', 'simple_white', 'plotly',
        # 'plotly_white', 'plotly_dark', 'presentation',
        title='State Wise Covid Analysis of USA through Scatter Plot',
        # labels={'% of Impact': '% of affect by covid'},
        hover_name='State',  # values appear in bold in the hover tooltip
        height=650,  # height of graph in pixels
        width=650
        # animation_frame='Year',   # assign marks to animation frames
        # range_x=[500,100000],
        # range_z=[0,14],
        # range_y=[5,100]

    )
    fig4 = px.pie(
        data_frame=dff,
        #values='% of Impact',
        names='State',
        color='% of Impact',  # differentiate markers (discrete) by color
        # color_discrete_sequence=["red", "green", "blue", "orange"],  # set marker colors
        # color_discrete_map={"WA":"yellow","CA":"red","NY":"black","FL":"brown"},
        hover_name='State',  # values appear in bold in the hover tooltip
        # hover_data=['positive'],            #values appear as extra data in the hover tooltip
        # custom_data=['total'],              #values are extra data to be used in Dash callbacks
        labels={"state": "States"},  # map the labels
        #title='State Wise Covid Analysis of USA through Pie Chart',  # figure title
        #template='presentation',  # 'ggplot2', 'seaborn', 'simple_white', 'plotly',
        # 'plotly_white', 'plotly_dark', 'presentation',
        # 'xgridoff', 'ygridoff', 'gridon', 'none'
        width=650,  # figure width in pixels
        height=500,  # figure height in pixels
        hole=0.2  # represents the hole in middle of pie
    )

    return container, fig,fig1,fig2,fig4


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)

