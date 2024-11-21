# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
options1=[{'label': 'All Sites', 'value': 'ALL'},{'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},{'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},{'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},{'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}]

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                
                                html.Div(dcc.Dropdown(
                                            id='site-dropdown',
                                            options=options1,
                                            value='ALL',placeholder='Select a Launch Site here',
                                            searchable=True
                                            )),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                #html.Div(dcc.Graph(id='success-pie-chart'))
                                html.Div(id='success-pie-chart', className='chart-grid', style={'display': 'flex'}),
                                html.Br(),
                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                html.Div(dcc.RangeSlider(id='payload-slider',
                                          min=0, max=10000, step=1000,
                                          marks={0: '0',100: '100'},
                                          value=[min_payload, max_payload])),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                #html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                html.Div(id='success-payload-scatter-chart', className='chart-grid', style={'display': 'flex'}),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='children'),
    Input(component_id='site-dropdown', component_property='value'))


def update_output_container(input_launchsite):
    if input_launchsite == 'ALL':
        sucess_data = spacex_df[spacex_df['class'] == 1]
        data_pie=sucess_data.groupby('Launch Site')['class'].sum().reset_index() 
        R_chart1    =   dcc.Graph(figure = px.pie(data_pie,values='class',
            		        names='Launch Site',
            		        title="Total Sucess Launches By Site"))
        return  [html.Div(className='chart-item',children=[html.Div(children=R_chart1)],style={'display': 'flex'})]

    else:
            launchsite_data  = spacex_df[spacex_df['Launch Site'] == input_launchsite]
            data_pie1 = launchsite_data.groupby('class')['Launch Site'].count().reset_index()
            data_pie1_sucess = data_pie1[data_pie1['class']==1]
            data_pie1_sucess_cnt = data_pie1_sucess.iloc[0,1]
            R_chart2 = dcc.Graph(
            		        figure=px.pie(data_pie1,
            		        values='Launch Site',
            		        names='class',
            		        title=f"Total Sucess for the site {input_launchsite} {data_pie1_sucess_cnt}")) 
            return [
                    html.Div(className='chart-item', children=[html.Div(children=R_chart2)],style={'display': 'flex'})
                    ]

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='children'),
    [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])


def update_output_container1(input_launchsite,selected_range):
    if input_launchsite == 'ALL':
        
        min_value, max_value = selected_range
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= min_value) & (spacex_df['Payload Mass (kg)'] <= max_value)] 
        R_chart3 = dcc.Graph(
            		      figure=px.scatter(filtered_df,
            				         x='Payload Mass (kg)',
            		                         y='class',
                                                 color='Booster Version Category',
            		                         title="Correlation between Payload and Success for all Sites")) 
        return [html.Div(className='chart-item', children=[html.Div(children=R_chart3)],style={'display': 'flex'})]

    else: 
        
        launchsite_data  = spacex_df[spacex_df['Launch Site'] == input_launchsite] 
        min_value, max_value = selected_range 
        filtered_df = launchsite_data[(launchsite_data['Payload Mass (kg)'] >= min_value) & (launchsite_data['Payload Mass (kg)'] <= max_value)]
        R_chart4 = dcc.Graph(
            		      figure=px.scatter(filtered_df,
            		                         x='Payload Mass (kg)',
            		                         y='class',
                                                 color='Booster Version Category',
            		                         title=f"Correlation between Payload and Success for {input_launchsite}"))
        return [
                    html.Div(className='chart-item', children=[html.Div(children=R_chart4)],style={'display': 'flex'})
                    ]

# Run the app
if __name__ == '__main__':
    app.run_server()
