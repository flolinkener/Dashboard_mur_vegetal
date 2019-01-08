import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
import datetime
import numpy as np
from dash.dependencies import Input, Output
import mongo_db_interactions as mongo
import fetch_citation as fc

external_stylesheets = [
'/assets/style.css'
]

def mean_humidity():
    humidity_1 = int(mongo.fetch_data_from_id('humidity','1'))
    humidity_2 = int(mongo.fetch_data_from_id('humidity','2'))
    humidity_3 = int(mongo.fetch_data_from_id('humidity','3'))
    humidity_4 = int(mongo.fetch_data_from_id('humidity','4'))
    humidity_5 = int(mongo.fetch_data_from_id('humidity','5'))
    humidity_6 = int(mongo.fetch_data_from_id('humidity','6'))
    humidity_7 = int(mongo.fetch_data_from_id('humidity','7'))
    humidity_8 = int(mongo.fetch_data_from_id('humidity','8'))
    humidity_9 = int(mongo.fetch_data_from_id('humidity','9'))
    humidity_list = [humidity_1,humidity_2,humidity_3,humidity_4,humidity_5,humidity_6,humidity_7,humidity_8,humidity_9]
    humidity_value = int(np.mean(humidity_list))
    return humidity_value


app = dash.Dash(__name__,external_stylesheets=external_stylesheets)
app.layout = html.Div([

    html.Div(id='refresh-data'),
        dcc.Interval(
            id='refresh-data-component',
            interval=10*1000, # in milliseconds
            n_intervals=0
    ),

    

    html.Div(id='leftBlock',className="col-lg-3",children = [

        html.Div(id='time'),
        dcc.Interval(
            id='interval-component',
            interval=10*1000, # in milliseconds
            n_intervals=0
        ),

        html.Div(id='temperatureBlock',children=
        [
            html.Div(id='temperatureValue', className="col-lg-6"),
                dcc.Interval(
                id='temperature-component',
                interval=10*1000, # in milliseconds
                n_intervals=0
            ),
            html.Div(id='temperatureImg',className="col-lg-6",children=
                html.Img(src='/assets/img/thermometer.png')
            )
        ]),

        html.Div(id='humidityBlock',children=
        [
            html.Div(id='humidityValue',className="col-lg-6"),
                dcc.Interval(
                    id='humidity-component',
                    interval=10*1000, # in milliseconds
                    n_intervals=0
            ),
            html.Div(id='humidityImg',className="col-lg-6",children=
                html.Img(src='/assets/img/water_drop.png')
            )

        ]),

        html.Div(id='batteryBlock',children=
        [
            html.Div(id='batteryValue',className="col-lg-6"),
                dcc.Interval(
                id='battery-component',
                interval=10*1000, # in milliseconds
                n_intervals=0
            ),
            html.Div(id='batteryImg',className="col-lg-6",children=
                html.Img(src='/assets/img/battery-symbol.png')
            )
        ])
    ]),

    html.Div(id='rightBlock',className='col-lg-9',children=
        html.Div(id='wall-mapping',children=[

            dcc.Graph(id='wall-mapping-left', className='col-lg-offset-1 col-lg-5'),
            dcc.Interval(
                id='wall-mapping-left-component',
                interval=10*1000, # in milliseconds
                n_intervals=0
            ),
            dcc.Graph(id='wall-mapping-right', className='col-lg-6'),
            dcc.Interval(
                id='wall-mapping-right-component',
                interval=10*1000, # in milliseconds
                n_intervals=0
            ),
            html.Div(id="legend", children = [
                html.P("Répartition de l'humidité sur le mur en %")])
        ]) 
    ),

    html.Div(id='footer', className='col-lg-12',children= [
       
       html.Div(id="containerFooter", children = [
            html.Div(id="citation"),        
                dcc.Interval(
                id='citation-component',
                interval=10*1000, # in milliseconds
                n_intervals=0
                ),      
        ]),
        
        html.Div(id='logo',className="col-lg-offset-4 col-lg-2", children=html.Img(src='/assets/img/image.png'))   
    ])

])

@app.callback(Output('time', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_date(n):
      return [html.P(datetime.datetime.now().strftime('%d-%m-%Y') + ' ' +  datetime.datetime.now().strftime('%H:%M'))]

@app.callback(Output('temperatureValue', 'children'),
              [Input('temperature-component', 'n_intervals')])
def update_temperature(n):
      return [html.P(str(mongo.fetch_data('temperature')) + '°C')]

@app.callback(Output('humidityValue', 'children'),
              [Input('humidity-component', 'n_intervals')])
def update_humidity(n):
      return [html.P(str(mean_humidity()) + '%')]

@app.callback(Output('batteryValue', 'children'),
              [Input('battery-component', 'n_intervals')])
def update_battery(n):
      return [html.P(str(mongo.fetch_data('battery')) + '%')]

@app.callback(Output('wall-mapping-left', 'figure'),
              [Input('wall-mapping-left-component', 'n_intervals')])
def update_wall_mapping_left(n):
    data =[ go.Heatmap(z = [[mongo.fetch_data_from_id('humidity','7'),mongo.fetch_data_from_id('humidity','8'),mongo.fetch_data_from_id('humidity','9')],  
    [mongo.fetch_data_from_id('humidity','4'),mongo.fetch_data_from_id('humidity','5'),mongo.fetch_data_from_id('humidity','6')],
    [mongo.fetch_data_from_id('humidity','1'),mongo.fetch_data_from_id('humidity','2'),mongo.fetch_data_from_id('humidity','3')]],
    opacity=0.5,
    showscale=False,
    reversescale=True
        )
        ]
    layout = go.Layout(
        margin = go.layout.Margin(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=0
        ),  
        images= [dict(source= '/assets/img/murdroit.jpg',
                opacity= 1,
                layer= "below",
                xref= "x",
                yref= "y",
                x= -0.5,
                y= -0.5,
                sizex= 3.5,
                sizey= 3.5,
                xanchor= "left",
                yanchor= "bottom"
            )],
    xaxis=dict(
        autorange=True,
        showgrid=False,
        zeroline=False,
        showline=False,
        ticks='',
        showticklabels=False
    ),
    yaxis=dict(
        autorange=True,
        showgrid=False,
        zeroline=False,
        showline=False,
        ticks='',
        showticklabels=False
    ),
    width= 500,
    height = 600
    )
    fig = go.Figure(data=data,layout=layout)
    return fig

@app.callback(Output('wall-mapping-right', 'figure'),
              [Input('wall-mapping-right-component', 'n_intervals')])
def update_wall_mapping_right(n):
    data =[ go.Heatmap(z = [[mongo.fetch_data_from_id('humidity','7'),mongo.fetch_data_from_id('humidity','8'),mongo.fetch_data_from_id('humidity','9')],  
    [mongo.fetch_data_from_id('humidity','4'),mongo.fetch_data_from_id('humidity','5'),mongo.fetch_data_from_id('humidity','6')],
    [mongo.fetch_data_from_id('humidity','1'),mongo.fetch_data_from_id('humidity','2'),mongo.fetch_data_from_id('humidity','3')]],
    opacity=0.5,
    reversescale=True    
        )
        ]
    layout = go.Layout(
         margin = go.layout.Margin(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=0
        ),  
        images= [dict(source= '/assets/img/murdroit.jpg',
                    opacity= 1,
                    layer= "below",
                    xref= "x",
                    yref= "y",
                    x= -0.5,
                    y= -0.5,
                    sizex= 3.5,
                    sizey= 3.5,
                    xanchor= "left",
                    yanchor= "bottom"
                )],
        xaxis=dict(
            autorange=True,
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks='',
            showticklabels=False
        ),
        yaxis=dict(
            autorange=True,
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks='',
            showticklabels=False
        ),
    width= 550,
    height = 600
    )
    fig = go.Figure(data=data,layout=layout)
    return fig

@app.callback(Output('citation', 'children'),
            [Input('citation-component', 'n_intervals')])
def update_citation(n):
      return [html.P(fc.fetch_citation())]

if __name__ == '__main__':
    app.run_server(debug=False)
