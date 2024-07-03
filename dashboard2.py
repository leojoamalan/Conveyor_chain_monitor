# from dash import Dash, html, dcc, Input, Output, callback, State
# import dash_bootstrap_components as dbc
# from dash.exceptions import PreventUpdate
# import pandas as pd
# import plotly.graph_objs as go
# import plotly.express as px
# import numpy as np
# import random
# import datetime

# # Sample data generation function (enhanced)
# def generate_sample_data(num_samples=100):
#     end_time = datetime.datetime.now()
#     start_time = end_time - datetime.timedelta(hours=num_samples)
#     times = [start_time + datetime.timedelta(hours=i) for i in range(num_samples)]
    
#     data = {
#         'time': times,
#         'strain': [random.uniform(0, 100) for _ in range(num_samples)],
#         'load': [random.uniform(0, 100) for _ in range(num_samples)],
#         'chain_position': [random.uniform(0, 1000) for _ in range(num_samples)],
#         'vibration': [random.uniform(0, 10) for _ in range(num_samples)],
#         'temperature': [random.uniform(10, 50) for _ in range(num_samples)],
#         'chain_wear': [random.uniform(0, 100) for _ in range(num_samples)],
#         'torque': [random.uniform(0, 50) for _ in range(num_samples)],
#         'lubrication_level': [random.uniform(0, 100) for _ in range(num_samples)],
#         'patch_length': [random.uniform(0, 100) for _ in range(num_samples)]
#     }
    
#     # Add OHLC data for strain
#     data['strain_open'] = data['strain']
#     data['strain_high'] = [x + random.uniform(0, 5) for x in data['strain']]
#     data['strain_low'] = [x - random.uniform(0, 5) for x in data['strain']]
#     data['strain_close'] = [x + random.uniform(-2, 2) for x in data['strain']]
    
#     return pd.DataFrame(data)

# # Initialize the app
# app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# server = app.server

# # Generate initial data
# data = generate_sample_data()

# # Define thresholds for each parameter (customizable)
# thresholds = {
#     'strain': (20, 50),
#     'load': (30, 70),
#     'chain_position': (200, 800),
#     'vibration': (5, 8),
#     'temperature': (20, 40),
#     'chain_wear': (30, 70),
#     'torque': (10, 30),
#     'lubrication_level': (40, 80),
#     'patch_length': (10, 30)
# }

# # Define function to determine status
# def determine_status(value, threshold):
#     if value < threshold[0]:
#         return 'Normal'
#     elif value < threshold[1]:
#         return 'Warning'
#     else:
#         return 'Critical'

# # App layout
# app.layout = html.Div([
#     dbc.Container([
#         html.H1("Machine Monitoring Dashboard", className="my-4"),
#         dbc.Tabs([
#             dbc.Tab([
#                 dbc.Row([
#                     dbc.Col(dcc.Graph(id='live-update-graph'), width=8),
#                     dbc.Col([
#                         dcc.Graph(id='pie-chart'),
#                         html.Div(id='alerts', className="mt-3")
#                     ], width=4)
#                 ]),
#                 dbc.Row([
#                     dbc.Col(dcc.Graph(id='moving-average-plot'), width=6),
#                     dbc.Col(dcc.Graph(id='radar-plot'), width=6)
#                 ]),
#                 dcc.Interval(id='interval-component', interval=5*1000, n_intervals=0)
#             ], label="Real-time Monitoring"),
#             dbc.Tab([
#                 dbc.Row([
#                     dbc.Col(dcc.Graph(id='scatter-plot'), width=6),
#                     dbc.Col(dcc.Graph(id='heatmap'), width=6)
#                 ]),
#                 dbc.Row([
#                     dbc.Col(dcc.Graph(id='candle-chart'), width=12)
#                 ]),
#                 dbc.Row([
#                     dbc.Col(dcc.Slider(
#                         id='time-slider',
#                         min=0,
#                         max=len(data) - 1,
#                         value=len(data) - 1,
#                         marks={i: str(data['time'][i].strftime('%H:%M')) for i in range(0, len(data), max(1, len(data)//10))},
#                         step=1
#                     ), width=12)
#                 ], className="my-4"),
#                 dbc.Row([
#                     dbc.Col(html.Div(id='selected-time'))
#                 ])
#             ], label="Historical Analysis")
#         ]),
#         dbc.Row([
#             dbc.Col(dcc.Dropdown(
#                 id='parameter-dropdown',
#                 options=[{'label': param.replace('_', ' ').title(), 'value': param} 
#                          for param in data.columns if param != 'time' and not param.startswith('strain_')],
#                 value=['strain', 'load', 'temperature'],
#                 multi=True
#             ), width=6),
#             dbc.Col(dbc.Button("Pause/Resume", id="pause-button", color="primary"), width=3),
#             dbc.Col(dbc.Switch(id='dark-mode-switch', label="Dark Mode", value=False), width=3)
#         ], className="my-4"),
#         dbc.Row([
#             dbc.Col(html.H4("Customize Thresholds"), width=12),
#             *[dbc.Col(dcc.RangeSlider(
#                 id=f'{param}-threshold',
#                 min=0,
#                 max=100,
#                 step=1,
#                 marks={0: '0', 50: '50', 100: '100'},
#                 value=list(thresholds[param])
#             ), width=4) for param in thresholds]
#         ], className="my-4"),
#         dcc.Store(id='threshold-store'),
#     ], fluid=True)
# ])

# @app.callback(
#     [Output('live-update-graph', 'figure'),
#      Output('pie-chart', 'figure'),
#      Output('moving-average-plot', 'figure'),
#      Output('radar-plot', 'figure'),
#      Output('alerts', 'children'),
#      Output('threshold-store', 'data')],
#     [Input('interval-component', 'n_intervals'),
#      Input('parameter-dropdown', 'value'),
#      Input('dark-mode-switch', 'value')] +
#     [Input(f'{param}-threshold', 'value') for param in thresholds]
# )
# def update_graphs(n, selected_params, dark_mode, *threshold_values):
#     global data, thresholds
    
#     if not selected_params:
#         raise PreventUpdate

#     # Update thresholds
#     for i, param in enumerate(thresholds):
#         thresholds[param] = threshold_values[i]
    
#     # Generate new data point
#     new_data = generate_sample_data(1).iloc[0]
#     data = pd.concat([data, pd.DataFrame([new_data])], ignore_index=True)
    
#     # Set color scheme based on dark mode
#     bg_color = 'rgb(50, 50, 50)' if dark_mode else 'white'
#     text_color = 'white' if dark_mode else 'black'
#     plot_bg_color = 'rgb(30, 30, 30)' if dark_mode else 'rgb(240, 240, 240)'
    
#     # Create line graph
#     fig_line = go.Figure()
#     for param in selected_params:
#         fig_line.add_trace(go.Scatter(x=data['time'], y=data[param], mode='lines+markers', name=param))
#     fig_line.update_layout(title='Selected Parameters Over Time', xaxis_title='Time', yaxis_title='Value',
#                            paper_bgcolor=bg_color, plot_bgcolor=plot_bg_color, font={'color': text_color})
    
#     # Create pie chart
#     latest_data = data.iloc[-1]
#     fig_pie = px.pie(values=[latest_data[param] for param in selected_params],
#                      names=selected_params, title='Current Parameter Distribution')
#     fig_pie.update_layout(paper_bgcolor=bg_color, plot_bgcolor=plot_bg_color, font={'color': text_color})
    
#     # Create moving average plot
#     fig_ma = go.Figure()
#     for param in selected_params:
#         ma = data[param].rolling(window=10).mean()
#         fig_ma.add_trace(go.Scatter(x=data['time'], y=ma, mode='lines', name=f'{param} MA'))
#     fig_ma.update_layout(title='10-point Moving Average of Selected Parameters',
#                          xaxis_title='Time', yaxis_title='Value',
#                          paper_bgcolor=bg_color, plot_bgcolor=plot_bg_color, font={'color': text_color})
    
#     # Create radar plot
#     fig_radar = go.Figure()
#     fig_radar.add_trace(go.Scatterpolar(
#         r=[latest_data[param] for param in selected_params],
#         theta=selected_params,
#         fill='toself',
#         name='Current Values'
#     ))
#     fig_radar.update_layout(
#         polar=dict(
#             radialaxis=dict(visible=True, range=[0, max([latest_data[param] for param in selected_params])])
#         ),
#         title='Radar Plot of Current Parameter Values',
#         paper_bgcolor=bg_color,
#         plot_bgcolor=plot_bg_color,
#         font={'color': text_color}
#     )
    
#     # Generate alerts
#     alerts = []
#     for param in selected_params:
#         status = determine_status(latest_data[param], thresholds[param])
#         if status != 'Normal':
#             alerts.append(html.Div(f"ALERT: {param} is in {status} state!", 
#                                    style={'color': 'yellow' if status == 'Warning' else 'red'}))
    
#     return fig_line, fig_pie, fig_ma, fig_radar, alerts, thresholds

# @app.callback(
#     Output('scatter-plot', 'figure'),
#     [Input('time-slider', 'value'),
#      Input('dark-mode-switch', 'value'),
#      Input('parameter-dropdown', 'value')]
# )
# def update_scatter_plot(selected_time, dark_mode, selected_params):
#     bg_color = 'rgb(50, 50, 50)' if dark_mode else 'white'
#     text_color = 'white' if dark_mode else 'black'
#     plot_bg_color = 'rgb(30, 30, 30)' if dark_mode else 'rgb(240, 240, 240)'
    
#     if len(selected_params) < 2:
#         return go.Figure()  # Return an empty figure if less than 2 parameters are selected

#     # Select the last 50 data points up to the selected time
#     start_index = max(0, selected_time - 49)
#     df_selected = data.iloc[start_index:selected_time+1]

#     fig = go.Figure()
#     for param in selected_params[:2]:  # Use the first two selected parameters
#         fig.add_trace(go.Scatter(
#             x=df_selected['time'],
#             y=df_selected[param],
#             mode='markers',
#             name=param
#         ))
    
#     fig.update_layout(
#         title='Scatter Plot of Selected Parameters',
#         xaxis_title='Time',
#         yaxis_title='Values',
#         paper_bgcolor=bg_color,
#         plot_bgcolor=plot_bg_color,
#         font={'color': text_color},
#         height=400
#     )
#     return fig

# @app.callback(
#     Output('heatmap', 'figure'),
#     [Input('time-slider', 'value'),
#      Input('dark-mode-switch', 'value'),
#      Input('parameter-dropdown', 'value')]
# )
# def update_heatmap(selected_time, dark_mode, selected_params):
#     bg_color = 'rgb(50, 50, 50)' if dark_mode else 'white'
#     text_color = 'white' if dark_mode else 'black'
#     plot_bg_color = 'rgb(30, 30, 30)' if dark_mode else 'rgb(240, 240, 240)'
    
#     if not selected_params:
#         return go.Figure()  # Return an empty figure if no parameters are selected

#     # Select the last 20 data points up to the selected time
#     start_index = max(0, selected_time - 19)
#     df_selected = data.iloc[start_index:selected_time+1]

#     fig = go.Figure(data=go.Heatmap(
#         z=df_selected[selected_params].values.T,
#         x=df_selected['time'],
#         y=selected_params,
#         colorscale='Viridis'
#     ))
    
#     fig.update_layout(
#         title='Heatmap of Selected Parameters',
#         xaxis_title='Time',
#         yaxis_title='Parameters',
#         paper_bgcolor=bg_color,
#         plot_bgcolor=plot_bg_color,
#         font={'color': text_color},
#         height=400
#     )
#     return fig

# @app.callback(
#     Output('candle-chart', 'figure'),
#     [Input('time-slider', 'value'),
#      Input('dark-mode-switch', 'value'),
#      Input('parameter-dropdown', 'value')]
# )
# def update_candlechart(selected_time, dark_mode, selected_params):
#     bg_color = 'rgb(50, 50, 50)' if dark_mode else 'white'
#     text_color = 'white' if dark_mode else 'black'
#     plot_bg_color = 'rgb(30, 30, 30)' if dark_mode else 'rgb(240, 240, 240)'
    
#     if not selected_params or 'strain' not in selected_params:
#         return go.Figure()  # Return an empty figure if 'strain' is not selected

#     # Select the last 20 data points up to the selected time
#     start_index = max(0, selected_time - 19)
#     df_selected = data.iloc[start_index:selected_time+1]

#     fig = go.Figure(data=[go.Candlestick(
#         x=df_selected['time'],
#         open=df_selected['strain_open'],
#         high=df_selected['strain_high'],
#         low=df_selected['strain_low'],
#         close=df_selected['strain_close']
#     )])
    
#     fig.update_layout(
#         title='Strain Candle Chart',
#         xaxis_title='Time',
#         yaxis_title='Strain Values',
#         paper_bgcolor=bg_color,
#         plot_bgcolor=plot_bg_color,
#         font={'color': text_color},
#         height=400
#     )
#     return fig

# @app.callback(
#     Output('selected-time', 'children'),
#     [Input('time-slider', 'value')]
# )
# def update_selected_time(selected_time):
#     return f"Selected Time: {data['time'].iloc[selected_time]}"

# @app.callback(
#     Output('interval-component', 'disabled'),
#     [Input('pause-button', 'n_clicks')],
#     [State('interval-component', 'disabled')]
# )
# def toggle_interval(n_clicks, current_state):
#     if n_clicks is None:
#         raise PreventUpdate
#     return not current_state

# if __name__ == '__main__':
#     app.run_server(debug=True)
# from dash import Dash, html, dcc, Input, Output, callback, State
# import dash_bootstrap_components as dbc
# from dash.exceptions import PreventUpdate
# import pandas as pd
# import plotly.graph_objs as go
# import plotly.express as px
# import numpy as np
# import random
# import datetime

# # Sample data generation function (enhanced)
# def generate_sample_data(num_samples=100):
#     end_time = datetime.datetime.now()
#     start_time = end_time - datetime.timedelta(hours=num_samples)
#     times = [start_time + datetime.timedelta(hours=i) for i in range(num_samples)]
    
#     data = {
#         'time': times,
#         'strain': [random.uniform(0, 100) for _ in range(num_samples)],
#         'load': [random.uniform(0, 100) for _ in range(num_samples)],
#         'chain_position': [random.uniform(0, 1000) for _ in range(num_samples)],
#         'vibration': [random.uniform(0, 10) for _ in range(num_samples)],
#         'temperature': [random.uniform(10, 50) for _ in range(num_samples)],
#         'chain_wear': [random.uniform(0, 100) for _ in range(num_samples)],
#         'torque': [random.uniform(0, 50) for _ in range(num_samples)],
#         'lubrication_level': [random.uniform(0, 100) for _ in range(num_samples)],
#         'patch_length': [random.uniform(0, 100) for _ in range(num_samples)]
#     }
    
#     # Add OHLC data for strain
#     data['strain_open'] = data['strain']
#     data['strain_high'] = [x + random.uniform(0, 5) for x in data['strain']]
#     data['strain_low'] = [x - random.uniform(0, 5) for x in data['strain']]
#     data['strain_close'] = [x + random.uniform(-2, 2) for x in data['strain']]
    
#     return pd.DataFrame(data)

# # Initialize the app
# app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# server = app.server

# # Generate initial data
# data = generate_sample_data()

# # Define thresholds for each parameter (customizable)
# thresholds = {
#     'strain': (20, 50),
#     'load': (30, 70),
#     'chain_position': (200, 800),
#     'vibration': (5, 8),
#     'temperature': (20, 40),
#     'chain_wear': (30, 70),
#     'torque': (10, 30),
#     'lubrication_level': (40, 80),
#     'patch_length': (10, 30)
# }

# # Define function to determine status
# def determine_status(value, threshold):
#     if value < threshold[0]:
#         return 'Normal'
#     elif value < threshold[1]:
#         return 'Warning'
#     else:
#         return 'Critical'

# # App layout
# app.layout = html.Div([
#     dbc.Container([
#         html.H1("Machine Monitoring Dashboard", className="my-4"),
#         dbc.Tabs([
#             dbc.Tab([
#                 dbc.Row([
#                     dbc.Col(dcc.Graph(id='live-update-graph'), width=8),
#                     dbc.Col([
#                         dcc.Graph(id='pie-chart'),
#                         html.Div(id='alerts', className="mt-3")
#                     ], width=4)
#                 ]),
#                 dbc.Row([
#                     dbc.Col(dcc.Graph(id='moving-average-plot'), width=6),
#                     dbc.Col(dcc.Graph(id='radar-plot'), width=6)
#                 ]),
#                 dcc.Interval(id='interval-component', interval=5*1000, n_intervals=0)
#             ], label="Real-time Monitoring"),
#             dbc.Tab([
#                 dbc.Row([
#                     dbc.Col(dcc.Graph(id='scatter-plot'), width=6),
#                     dbc.Col(dcc.Graph(id='facet-grid'), width=6)
#                 ]),
#                 dbc.Row([
#                     dbc.Col(dcc.Graph(id='candle-chart'), width=12)
#                 ]),
#                 dbc.Row([
#                     dbc.Col(dcc.Slider(
#                         id='time-slider',
#                         min=0,
#                         max=len(data) - 1,
#                         value=len(data) - 1,
#                         marks={i: str(data['time'][i].strftime('%H:%M')) for i in range(0, len(data), max(1, len(data)//10))},
#                         step=1
#                     ), width=12)
#                 ], className="my-4"),
#                 dbc.Row([
#                     dbc.Col(html.Div(id='selected-time'))
#                 ])
#             ], label="Historical Analysis")
#         ]),
#         dbc.Row([
#             dbc.Col(dcc.Dropdown(
#                 id='parameter-dropdown',
#                 options=[{'label': param.replace('_', ' ').title(), 'value': param} 
#                          for param in data.columns if param != 'time' and not param.startswith('strain_')],
#                 value=['strain', 'load', 'temperature'],
#                 multi=True
#             ), width=6),
#             dbc.Col(dbc.Button("Pause/Resume", id="pause-button", color="primary"), width=3),
#             dbc.Col(dbc.Switch(id='dark-mode-switch', label="Dark Mode", value=False), width=3)
#         ], className="my-4"),
#         dbc.Row([
#             dbc.Col(html.H4("Customize Thresholds"), width=12),
#             *[dbc.Col(dcc.RangeSlider(
#                 id=f'{param}-threshold',
#                 min=0,
#                 max=100,
#                 step=1,
#                 marks={0: '0', 50: '50', 100: '100'},
#                 value=list(thresholds[param])
#             ), width=4) for param in thresholds]
#         ], className="my-4"),
#         dcc.Store(id='threshold-store'),
#     ], fluid=True)
# ])

# @app.callback(
#     [Output('live-update-graph', 'figure'),
#      Output('pie-chart', 'figure'),
#      Output('moving-average-plot', 'figure'),
#      Output('radar-plot', 'figure'),
#      Output('alerts', 'children'),
#      Output('threshold-store', 'data')],
#     [Input('interval-component', 'n_intervals'),
#      Input('parameter-dropdown', 'value'),
#      Input('dark-mode-switch', 'value')] +
#     [Input(f'{param}-threshold', 'value') for param in thresholds]
# )
# def update_graphs(n, selected_params, dark_mode, *threshold_values):
#     global data, thresholds
    
#     if not selected_params:
#         raise PreventUpdate

#     # Update thresholds
#     for i, param in enumerate(thresholds):
#         thresholds[param] = threshold_values[i]
    
#     # Generate new data point
#     new_data = generate_sample_data(1).iloc[0]
#     data = pd.concat([data, pd.DataFrame([new_data])], ignore_index=True)
    
#     # Set color scheme based on dark mode
#     bg_color = 'rgb(50, 50, 50)' if dark_mode else 'white'
#     text_color = 'white' if dark_mode else 'black'
#     plot_bg_color = 'rgb(30, 30, 30)' if dark_mode else 'rgb(240, 240, 240)'
    
#     # Create line graph
#     fig_line = go.Figure()
#     for param in selected_params:
#         fig_line.add_trace(go.Scatter(x=data['time'], y=data[param], mode='lines+markers', name=param))
#     fig_line.update_layout(title='Selected Parameters Over Time', xaxis_title='Time', yaxis_title='Value',
#                            paper_bgcolor=bg_color, plot_bgcolor=plot_bg_color, font={'color': text_color})
    
#     # Create pie chart
#     latest_data = data.iloc[-1]
#     fig_pie = px.pie(values=[latest_data[param] for param in selected_params],
#                      names=selected_params, title='Current Parameter Distribution')
#     fig_pie.update_layout(paper_bgcolor=bg_color, plot_bgcolor=plot_bg_color, font={'color': text_color})
    
#     # Create moving average plot
#     fig_ma = go.Figure()
#     for param in selected_params:
#         ma = data[param].rolling(window=10).mean()
#         fig_ma.add_trace(go.Scatter(x=data['time'], y=ma, mode='lines', name=f'{param} MA'))
#     fig_ma.update_layout(title='10-point Moving Average of Selected Parameters',
#                          xaxis_title='Time', yaxis_title='Value',
#                          paper_bgcolor=bg_color, plot_bgcolor=plot_bg_color, font={'color': text_color})
    
#     # Create radar plot
#     fig_radar = go.Figure()
#     fig_radar.add_trace(go.Scatterpolar(
#         r=[latest_data[param] for param in selected_params],
#         theta=selected_params,
#         fill='toself',
#         name='Current Values'
#     ))
#     fig_radar.update_layout(
#         polar=dict(
#             radialaxis=dict(visible=True, range=[0, max([latest_data[param] for param in selected_params])])
#         ),
#         title='Radar Plot of Current Parameter Values',
#         paper_bgcolor=bg_color,
#         plot_bgcolor=plot_bg_color,
#         font={'color': text_color}
#     )
    
#     # Generate alerts
#     alerts = []
#     for param in selected_params:
#         status = determine_status(latest_data[param], thresholds[param])
#         if status != 'Normal':
#             alerts.append(html.Div(f"ALERT: {param} is in {status} state!", 
#                                    style={'color': 'yellow' if status == 'Warning' else 'red'}))
    
#     return fig_line, fig_pie, fig_ma, fig_radar, alerts, thresholds

# @app.callback(
#     Output('scatter-plot', 'figure'),
#     [Input('time-slider', 'value'),
#      Input('dark-mode-switch', 'value'),
#      Input('parameter-dropdown', 'value')]
# )
# def update_scatter_plot(selected_time, dark_mode, selected_params):
#     bg_color = 'rgb(50, 50, 50)' if dark_mode else 'white'
#     text_color = 'white' if dark_mode else 'black'
#     plot_bg_color = 'rgb(30, 30, 30)' if dark_mode else 'rgb(240, 240, 240)'
    
#     if len(selected_params) < 2:
#         return go.Figure()  # Return an empty figure if less than 2 parameters are selected

#     # Select the last 50 data points up to the selected time
#     start_index = max(0, selected_time - 49)
#     df_selected = data.iloc[start_index:selected_time+1]

#     fig = go.Figure()
#     for param in selected_params[:2]:  # Use the first two selected parameters
#         fig.add_trace(go.Scatter(
#             x=df_selected['time'],
#             y=df_selected[param],
#             mode='markers',
#             name=param
#         ))
    
#     fig.update_layout(
#         title='Scatter Plot of Selected Parameters',
#         xaxis_title='Time',
#         yaxis_title='Values',
#         paper_bgcolor=bg_color,
#         plot_bgcolor=plot_bg_color,
#         font={'color': text_color},
#         height=400
#     )
#     return fig

# @app.callback(
#     Output('facet-grid', 'figure'),
#     [Input('time-slider', 'value'),
#      Input('dark-mode-switch', 'value'),
#      Input('parameter-dropdown', 'value')]
# )
# def update_facet_grid(selected_time, dark_mode, selected_params):
#     bg_color = 'rgb(50, 50, 50)' if dark_mode else 'white'
#     text_color = 'white' if dark_mode else 'black'
#     plot_bg_color = 'rgb(30, 30, 30)' if dark_mode else 'rgb(240, 240, 240)'
    
#     if not selected_params:
#         return go.Figure()  # Return an empty figure if no parameters are selected

#     # Select the last 20 data points up to the selected time
#     start_index = max(0, selected_time - 19)
#     df_selected = data.iloc[start_index:selected_time+1]

#     # Create facet grid plot using Plotly Express
#     fig = px.line(df_selected.melt(id_vars=['time'], value_vars=selected_params), x='time', y='value', color='variable', facet_col='variable', facet_col_wrap=2)
    
#     fig.update_layout(
#         title='Facet Grid of Selected Parameters Over Time',
#         xaxis_title='Time',
#         yaxis_title='Values',
#         paper_bgcolor=bg_color,
#         plot_bgcolor=plot_bg_color,
#         font={'color': text_color},
#         height=800
#     )
#     return fig

# @app.callback(
#     Output('candle-chart', 'figure'),
#     [Input('time-slider', 'value'),
#      Input('dark-mode-switch', 'value'),
#      Input('parameter-dropdown', 'value')]
# )
# def update_candlechart(selected_time, dark_mode, selected_params):
#     bg_color = 'rgb(50, 50, 50)' if dark_mode else 'white'
#     text_color = 'white' if dark_mode else 'black'
#     plot_bg_color = 'rgb(30, 30, 30)' if dark_mode else 'rgb(240, 240, 240)'
    
#     if not selected_params or 'strain' not in selected_params:
#         return go.Figure()  # Return an empty figure if 'strain' is not selected

#     # Select the last 20 data points up to the selected time
#     start_index = max(0, selected_time - 19)
#     df_selected = data.iloc[start_index:selected_time+1]

#     fig = go.Figure(data=[go.Candlestick(
#         x=df_selected['time'],
#         open=df_selected['strain_open'],
#         high=df_selected['strain_high'],
#         low=df_selected['strain_low'],
#         close=df_selected['strain_close']
#     )])
    
#     fig.update_layout(
#         title='Strain Candle Chart',
#         xaxis_title='Time',
#         yaxis_title='Strain Values',
#         paper_bgcolor=bg_color,
#         plot_bgcolor=plot_bg_color,
#         font={'color': text_color},
#         height=400
#     )
#     return fig

# @app.callback(
#     Output('selected-time', 'children'),
#     [Input('time-slider', 'value')]
# )
# def update_selected_time(selected_time):
#     return f"Selected Time: {data['time'].iloc[selected_time]}"

# @app.callback(
#     Output('interval-component', 'disabled'),
#     [Input('pause-button', 'n_clicks')],
#     [State('interval-component', 'disabled')]
# )
# def toggle_interval(n_clicks, current_state):
#     if n_clicks is None:
#         raise PreventUpdate
#     return not current_state

# if __name__ == '__main__':
#     app.run_server(debug=True)
from dash import Dash, html, dcc, Input, Output, callback, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import numpy as np
import random
import datetime

# Sample data generation function (enhanced) with random decreasing order
def generate_sample_data(num_samples=100):
    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(hours=num_samples)
    times = [start_time + datetime.timedelta(hours=i) for i in range(num_samples)]
    
    data = {
        'time': times,
        'strain': sorted([random.uniform(0, 100) for _ in range(num_samples)], reverse=True),
        'load': sorted([random.uniform(0, 100) for _ in range(num_samples)], reverse=True),
        'chain_position': sorted([random.uniform(0, 1000) for _ in range(num_samples)], reverse=True),
        'vibration': sorted([random.uniform(0, 10) for _ in range(num_samples)], reverse=True),
        'temperature': sorted([random.uniform(10, 50) for _ in range(num_samples)], reverse=True),
        'chain_wear': sorted([random.uniform(0, 100) for _ in range(num_samples)], reverse=True),
        'torque': sorted([random.uniform(0, 50) for _ in range(num_samples)], reverse=True),
        'lubrication_level': sorted([random.uniform(0, 100) for _ in range(num_samples)], reverse=True),
        'patch_length': sorted([random.uniform(0, 100) for _ in range(num_samples)], reverse=True)
    }
    
    return pd.DataFrame(data)

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Generate initial data
data = generate_sample_data()

# Define thresholds for each parameter (customizable)
thresholds = {
    'strain': (20, 50),
    'load': (30, 70),
    'chain_position': (200, 800),
    'vibration': (5, 8),
    'temperature': (20, 40),
    'chain_wear': (30, 70),
    'torque': (10, 30),
    'lubrication_level': (40, 80),
    'patch_length': (10, 30)
}

# Define function to determine status
def determine_status(value, threshold):
    if value < threshold[0]:
        return 'Normal'
    elif value < threshold[1]:
        return 'Warning'
    else:
        return 'Critical'

# App layout
app.layout = html.Div([
    dbc.Container([
        html.H1("Machine Monitoring Dashboard", className="my-4"),
        dbc.Tabs([
            dbc.Tab([
                dbc.Row([
                    dbc.Col(dcc.Graph(id='live-update-graph'), width=8),
                    dbc.Col([
                        dcc.Graph(id='pie-chart'),
                        html.Div(id='alerts', className="mt-3")
                    ], width=4)
                ]),
                dbc.Row([
                    dbc.Col(dcc.Graph(id='moving-average-plot'), width=6),
                    dbc.Col(dcc.Graph(id='radar-plot'), width=6)
                ]),
                dcc.Interval(id='interval-component', interval=5*1000, n_intervals=0)
            ], label="Real-time Monitoring"),
            dbc.Tab([
                dbc.Row([
                    dbc.Col(dcc.Graph(id='scatter-plot'), width=6),
                    dbc.Col(dcc.Graph(id='facet-grid'), width=6)
                ]),
                dbc.Row([
                    dbc.Col(dcc.Graph(id='dumbbell-chart'), width=12)
                ]),
                dbc.Row([
                    dbc.Col(dcc.Slider(
                        id='time-slider',
                        min=0,
                        max=len(data) - 1,
                        value=len(data) - 1,
                        marks={i: str(data['time'][i].strftime('%H:%M')) for i in range(0, len(data), max(1, len(data)//10))},
                        step=1
                    ), width=12)
                ], className="my-4"),
                dbc.Row([
                    dbc.Col(html.Div(id='selected-time'))
                ])
            ], label="Historical Analysis")
        ]),
        dbc.Row([
            dbc.Col(dcc.Dropdown(
                id='parameter-dropdown',
                options=[{'label': param.replace('_', ' ').title(), 'value': param} 
                         for param in data.columns if param != 'time'],
                value=['strain', 'load', 'temperature'],
                multi=True
            ), width=6),
            dbc.Col(dbc.Button("Pause/Resume", id="pause-button", color="primary"), width=3),
            dbc.Col(dbc.Switch(id='dark-mode-switch', label="Dark Mode", value=False), width=3)
        ], className="my-4"),
        dbc.Row([
            dbc.Col(html.H4("Customize Thresholds"), width=12),
            *[dbc.Col(dcc.RangeSlider(
                id=f'{param}-threshold',
                min=0,
                max=100,
                step=1,
                marks={0: '0', 50: '50', 100: '100'},
                value=list(thresholds[param])
            ), width=4) for param in thresholds]
        ], className="my-4"),
        dcc.Store(id='threshold-store'),
    ], fluid=True)
])

@app.callback(
    [Output('live-update-graph', 'figure'),
     Output('pie-chart', 'figure'),
     Output('moving-average-plot', 'figure'),
     Output('radar-plot', 'figure'),
     Output('alerts', 'children'),
     Output('threshold-store', 'data')],
    [Input('interval-component', 'n_intervals'),
     Input('parameter-dropdown', 'value'),
     Input('dark-mode-switch', 'value')] +
    [Input(f'{param}-threshold', 'value') for param in thresholds]
)
def update_graphs(n, selected_params, dark_mode, *threshold_values):
    global data, thresholds
    
    if not selected_params:
        raise PreventUpdate

    # Update thresholds
    for i, param in enumerate(thresholds):
        thresholds[param] = threshold_values[i]
    
    # Generate new data point
    new_data = generate_sample_data(1).iloc[0]
    data = pd.concat([data, pd.DataFrame([new_data])], ignore_index=True)
    
    # Set color scheme based on dark mode
    bg_color = 'rgb(50, 50, 50)' if dark_mode else 'white'
    text_color = 'white' if dark_mode else 'black'
    plot_bg_color = 'rgb(30, 30, 30)' if dark_mode else 'rgb(240, 240, 240)'
    
    # Create line graph
    fig_line = go.Figure()
    for param in selected_params:
        fig_line.add_trace(go.Scatter(x=data['time'], y=data[param], mode='lines+markers', name=param))
    fig_line.update_layout(title='Selected Parameters Over Time', xaxis_title='Time', yaxis_title='Value',
                           paper_bgcolor=bg_color, plot_bgcolor=plot_bg_color, font={'color': text_color})
    
    # Create pie chart
    latest_data = data.iloc[-1]
    fig_pie = px.pie(values=[latest_data[param] for param in selected_params],
                     names=selected_params, title='Current Parameter Distribution')
    fig_pie.update_layout(paper_bgcolor=bg_color, plot_bgcolor=plot_bg_color, font={'color': text_color})
    
    # Create moving average plot
    fig_ma = go.Figure()
    for param in selected_params:
        ma = data[param].rolling(window=10).mean()
        fig_ma.add_trace(go.Scatter(x=data['time'], y=ma, mode='lines', name=f'{param} MA'))
    fig_ma.update_layout(title='10-point Moving Average of Selected Parameters',
                         xaxis_title='Time', yaxis_title='Value',
                         paper_bgcolor=bg_color, plot_bgcolor=plot_bg_color, font={'color': text_color})
    
    # Create radar plot
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=[latest_data[param] for param in selected_params],
        theta=selected_params,
        fill='toself',
        name='Current Values'
    ))
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, max([latest_data[param] for param in selected_params])])
        ),
        title='Radar Plot of Current Parameter Values',
        paper_bgcolor=bg_color,
        plot_bgcolor=plot_bg_color,
        font={'color': text_color}
    )
    
    # Generate alerts
    alerts = []
    for param in selected_params:
        status = determine_status(latest_data[param], thresholds[param])
        if status != 'Normal':
            alerts.append(html.Div(f"ALERT: {param} is in {status} state!", 
                                   style={'color': 'yellow' if status == 'Warning' else 'red'}))
    
    return fig_line, fig_pie, fig_ma, fig_radar, alerts, thresholds

@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('time-slider', 'value'),
     Input('dark-mode-switch', 'value'),
     Input('parameter-dropdown', 'value')]
)
def update_scatter_plot(selected_time, dark_mode, selected_params):
    bg_color = 'rgb(50, 50, 50)' if dark_mode else 'white'
    text_color = 'white' if dark_mode else 'black'
    plot_bg_color = 'rgb(30, 30, 30)' if dark_mode else 'rgb(240, 240, 240)'
    
    if len(selected_params) < 2:
        return go.Figure()  # Return an empty figure if less than 2 parameters are selected

    # Select the last 50 data points up to the selected time
    start_index = max(0, selected_time - 49)
    df_selected = data.iloc[start_index:selected_time+1]

    fig = go.Figure()
    for param in selected_params[:2]:  # Use the first two selected parameters
        fig.add_trace(go.Scatter(
            x=df_selected['time'],
            y=df_selected[param],
            mode='markers',
            name=param
        ))
    
    fig.update_layout(
        title='Scatter Plot of Selected Parameters',
        xaxis_title='Time',
        yaxis_title='Values',
        paper_bgcolor=bg_color,
        plot_bgcolor=plot_bg_color,
        font={'color': text_color},
        height=400
    )
    return fig

@app.callback(
    Output('facet-grid', 'figure'),
    [Input('time-slider', 'value'),
     Input('dark-mode-switch', 'value'),
     Input('parameter-dropdown', 'value')]
)
def update_facet_grid(selected_time, dark_mode, selected_params):
    bg_color = 'rgb(50, 50, 50)' if dark_mode else 'white'
    text_color = 'white' if dark_mode else 'black'
    plot_bg_color = 'rgb(30, 30, 30)' if dark_mode else 'rgb(240, 240, 240)'
    
    if not selected_params:
        return go.Figure()  # Return an empty figure if no parameters are selected

    # Select the last 20 data points up to the selected time
    start_index = max(0, selected_time - 19)
    df_selected = data.iloc[start_index:selected_time+1]

    # Create facet grid plot using Plotly Express
    fig = px.line(df_selected.melt(id_vars=['time'], value_vars=selected_params), x='time', y='value', color='variable', facet_col='variable', facet_col_wrap=2)
    
    fig.update_layout(
        title='Facet Grid of Selected Parameters Over Time',
        xaxis_title='Time',
        yaxis_title='Values',
        paper_bgcolor=bg_color,
        plot_bgcolor=plot_bg_color,
        font={'color': text_color},
        height=800
    )
    return fig

@app.callback(
    Output('dumbbell-chart', 'figure'),
    [Input('time-slider', 'value'),
     Input('dark-mode-switch', 'value'),
     Input('parameter-dropdown', 'value')]
)
def update_dumbbell_chart(selected_time, dark_mode, selected_params):
    bg_color = 'rgb(50, 50, 50)' if dark_mode else 'white'
    text_color = 'white' if dark_mode else 'black'
    plot_bg_color = 'rgb(30, 30, 30)' if dark_mode else 'rgb(240, 240, 240)'
    
    if not selected_params or len(selected_params) < 2:
        return go.Figure()  # Return an empty figure if less than 2 parameters are selected

    # Select the last 20 data points up to the selected time
    start_index = max(0, selected_time - 19)
    df_selected = data.iloc[start_index:selected_time+1]

    fig = go.Figure()

    # Create the dumbbell chart
    for param in selected_params:
        fig.add_trace(go.Scatter(
            x=df_selected['time'],
            y=df_selected[param],
            mode='lines+markers',
            name=param
        ))
    
    fig.update_layout(
        title='Dumbbell Chart of Selected Parameters Over Time',
        xaxis_title='Time',
        yaxis_title='Values',
        paper_bgcolor=bg_color,
        plot_bgcolor=plot_bg_color,
        font={'color': text_color},
        height=400
    )
    return fig

@app.callback(
    Output('selected-time', 'children'),
    [Input('time-slider', 'value')]
)
def update_selected_time(selected_time):
    return f"Selected Time: {data['time'].iloc[selected_time]}"

@app.callback(
    Output('interval-component', 'disabled'),
    [Input('pause-button', 'n_clicks')],
    [State('interval-component', 'disabled')]
)
def toggle_interval(n_clicks, current_state):
    if n_clicks is None:
        raise PreventUpdate
    return not current_state

if __name__ == '__main__':
    app.run_server(debug=True)
