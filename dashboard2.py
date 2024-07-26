# from dash import Dash, html, dcc, Input, Output, State
# import dash_bootstrap_components as dbc
# import pandas as pd
# import plotly.graph_objs as go
# import datetime
# import numpy as np
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import os

# # Sample data generation function with a trend
# def generate_sample_data(start_date, days=30, trend='increasing'):
#     date_range = pd.date_range(start=start_date, periods=days, freq='D')
#     data = {
#         'time': date_range,
#         'strain': [],
#         'load': [],
#         'chain_position': [],
#         'vibration': [],
#         'temperature': [],
#         'chain_wear': [],
#         'torque': [],
#         'lubrication_level': [],
#         'patch_length': []
#     }

#     for date in date_range:
#         is_weekend = date.weekday() >= 5
#         base_multiplier = 0.7 if is_weekend else 1.0  # Lower the base value for weekends
#         if trend == 'increasing':
#             base = base_multiplier * np.linspace(0, 100, days)[len(data['strain'])]
#             variance = 5
#         else:
#             base = base_multiplier * np.linspace(100, 0, days)[len(data['strain'])]
#             variance = 5

#         data['strain'].append(base + np.random.uniform(-variance, variance))
#         data['load'].append(base + np.random.uniform(-variance, variance))
#         data['chain_position'].append(base * 10 + np.random.uniform(-variance * 10, variance * 10))
#         data['vibration'].append(base / 10 + np.random.uniform(-variance / 10, variance / 10))
#         data['temperature'].append(base / 2 + np.random.uniform(-variance / 2, variance / 2))
#         data['chain_wear'].append(base + np.random.uniform(-variance, variance))
#         data['torque'].append(base / 2 + np.random.uniform(-variance / 2, variance / 2))
#         data['lubrication_level'].append(base + np.random.uniform(-variance, variance))
#         data['patch_length'].append(base + np.random.uniform(-variance, variance))

#     return pd.DataFrame(data)

# # Function to send email notification
# def send_email(subject, body):
#     try:
#         sender_email = os.getenv("leojoamalan6@gmail.com")
#         receiver_email = os.getenv("leojoamalan@gmail.com")
#         password = os.getenv("fjnpgiukmlninvch")

#         msg = MIMEMultipart()
#         msg['From'] = sender_email
#         msg['To'] = receiver_email
#         msg['Subject'] = subject

#         msg.attach(MIMEText(body, 'plain'))

#         with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
#             server.login(sender_email, password)
#             server.sendmail(sender_email, receiver_email, msg.as_string())
#         print("Email sent successfully!")
#     except Exception as e:
#         print(f"Failed to send email: {e}")

# # Initialize the app
# app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# server = app.server

# # Generate initial data
# data = generate_sample_data(start_date=datetime.datetime.now() - datetime.timedelta(days=30), days=30, trend='increasing')

# # Define thresholds for each parameter
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

# # Update the layout
# app.layout = html.Div([
#     dbc.Container([
#         html.H1("Machine Monitoring Dashboard", className="header-title"),
#         dbc.Row([
#             dbc.Col(dcc.DatePickerRange(
#                 id='date-picker-range',
#                 start_date=(datetime.datetime.now() - datetime.timedelta(days=30)).date(),
#                 end_date=datetime.datetime.now().date(),
#                 display_format='YYYY-MM-DD'
#             ), width=4),
#             dbc.Col(dcc.Dropdown(
#                 id='parameter-dropdown',
#                 options=[{'label': param.replace('_', ' ').title(), 'value': param} 
#                          for param in ['strain', 'load', 'chain_position', 'vibration', 'temperature', 
#                                        'chain_wear', 'torque', 'lubrication_level', 'patch_length']],
#                 value=['strain', 'load', 'temperature'],
#                 multi=True
#             ), width=4),
#             dbc.Col(dbc.Switch(
#                 id='dark-mode-switch',
#                 label="Dark Mode",
#                 value=False
#             ), width=2),
#             dbc.Col(dbc.Button("Pause/Resume", id="pause-button", color="primary"), width=2)
#         ], className="mb-4"),
#         dbc.Row([
#             dbc.Col(dcc.Graph(id='main-graph'), width=12),
#         ], className="mb-4"),
#         dbc.Row([
#             dbc.Col(dcc.Graph(id='history-graph'), width=12),
#         ], className="mb-4"),
#         dbc.Row([
#             dbc.Col(dcc.Graph(id='performance-analysis-graph'), width=12),
#         ], className="mb-4"),
#         dbc.Row([
#             dbc.Col(dcc.Graph(id='failure-graph'), width=12),
#         ], className="mb-4"),
#         dbc.Row([
#             dbc.Col(dbc.Card(id="summary-card", body=True), width=12)
#         ], className="mb-4"),
#         dbc.Row([
#             dbc.Col(dcc.Slider(
#                 id='update-interval-slider',
#                 min=1,
#                 max=60,
#                 step=1,
#                 value=5,
#                 marks={i: f'{i}s' for i in range(0, 61, 10)},
#                 tooltip={"placement": "bottom", "always_visible": True}
#             ), width=12)
#         ], className="mb-4"),
#         dbc.Row(
#             dbc.Col(
#                 dbc.Button("Download Data", id="btn-download", color="primary", className="mr-2"),
#                 width={"size": 2, "offset": 5},
#             ),
#         ),
#         dcc.Download(id="download-data"),
#         dcc.Interval(
#             id='graph-update',
#             interval=5*1000,  # Update every 5 seconds initially
#             n_intervals=0,
#             disabled=False
#         ),
#         dcc.Store(id='failure-detected', data={param: False for param in thresholds.keys()}),
#         dcc.Store(id='failure-periods', data={param: [] for param in thresholds.keys()})
#     ], fluid=True),
# ], id="main-container")

# # Callback to update data and graphs
# @app.callback(
#     [Output('main-graph', 'figure'),
#      Output('history-graph', 'figure'),
#      Output('performance-analysis-graph', 'figure'),
#      Output('failure-graph', 'figure'),
#      Output('summary-card', 'children'),
#      Output('graph-update', 'interval'),
#      Output('failure-detected', 'data'),
#      Output('failure-periods', 'data')],
#     [Input('graph-update', 'n_intervals'),
#      Input('date-picker-range', 'start_date'),
#      Input('date-picker-range', 'end_date'),
#      Input('dark-mode-switch', 'value'),
#      Input('parameter-dropdown', 'value'),
#      Input('update-interval-slider', 'value')],
#     [State('failure-detected', 'data'),
#      State('failure-periods', 'data')]
# )
# def update_graphs(n_intervals, start_date, end_date, dark_mode, selected_params, update_interval, failure_detected, failure_periods):
#     new_data = generate_sample_data(start_date=data['time'].iloc[-1] + datetime.timedelta(days=1), days=1).iloc[0]
#     data.loc[len(data)] = new_data

#     # Filter data based on date range
#     mask = (data['time'].dt.date >= pd.to_datetime(start_date).date()) & (data['time'].dt.date <= pd.to_datetime(end_date).date())
#     filtered_data = data.loc[mask]

#     # Set color scheme based on dark mode
#     bg_color = 'rgb(50, 50, 50)' if dark_mode else 'white'
#     text_color = 'white' if dark_mode else 'black'
#     plot_bg_color = 'rgb(30, 30, 30)' if dark_mode else 'rgb(240, 240, 240)'

#     # Create main graph
#     main_fig = go.Figure()

#     for param in selected_params:
#         main_fig.add_trace(go.Scatter(x=filtered_data['time'], y=filtered_data[param],
#                                       mode='lines+markers', name=param.replace('_', ' ').title()))

#     main_fig.update_layout(
#         title='Parameters Over Time',
#         xaxis_title='Time',
#         yaxis_title='Value',
#         paper_bgcolor=bg_color,
#         plot_bgcolor=plot_bg_color,
#         font={'color': text_color},
#         legend_title_text='Parameters'
#     )

#     # Create history graph
#     history_fig = go.Figure()

#     for param in selected_params:
#         history_fig.add_trace(go.Scatter(x=data['time'], y=data[param],
#                                          mode='lines', name=param.replace('_', ' ').title()))

#     history_fig.update_layout(
#         title='Historical Data',
#         xaxis_title='Time',
#         yaxis_title='Value',
#         paper_bgcolor=bg_color,
#         plot_bgcolor=plot_bg_color,
#         font={'color': text_color},
#         legend_title_text='Parameters'
#     )

#     # Create performance analysis graph
#     performance_data = data[selected_params].mean(axis=1)
#     performance_fig = go.Figure()
#     performance_fig.add_trace(go.Scatter(x=data['time'], y=performance_data, mode='lines+markers', name='Performance'))

#     performance_fig.update_layout(
#         title='Performance Analysis',
#         xaxis_title='Time',
#         yaxis_title='Performance Metric',
#         paper_bgcolor=bg_color,
#         plot_bgcolor=plot_bg_color,
#         font={'color': text_color}
#     )

#     # Update failure detection and failure periods
#     critical_points = []
#     for param in selected_params:
#         current_value = new_data[param]
#         threshold = thresholds[param]
#         status = determine_status(current_value, threshold)

#         if status == 'Critical':
#             failure_detected[param] = True
#             critical_points.append((param, data['time'].iloc[-1], current_value))
#             if not failure_periods[param] or failure_periods[param][-1][1] != data['time'].iloc[-1]:
#                 failure_periods[param].append((data['time'].iloc[-1], data['time'].iloc[-1]))
#         elif failure_detected[param]:
#             failure_periods[param][-1] = (failure_periods[param][-1][0], data['time'].iloc[-1])
#             failure_detected[param] = False

#     # Create failure graph
#     failure_fig = go.Figure()
#     for param in selected_params:
#         failure_fig.add_trace(go.Scatter(x=data['time'], y=data[param],
#                                          mode='lines', name=param.replace('_', ' ').title()))
#         for start, end in failure_periods[param]:
#             failure_fig.add_shape(
#                 type="rect",
#                 xref="x",
#                 yref="y",
#                 x0=start,
#                 x1=end,
#                 y0=0,
#                 y1=max(data[param]),
#                 fillcolor="red",
#                 opacity=0.3,
#                 line_width=0,
#             )

#     failure_fig.update_layout(
#         title='Potential Failure Points',
#         xaxis_title='Time',
#         yaxis_title='Value',
#         paper_bgcolor=bg_color,
#         plot_bgcolor=plot_bg_color,
#         font={'color': text_color}
#     )

#     # Create summary card
#     summary_card_content = []
#     for param in selected_params:
#         current_value = new_data[param]
#         threshold = thresholds[param]
#         status = determine_status(current_value, threshold)
#         color = 'green' if status == 'Normal' else 'orange' if status == 'Warning' else 'red'
#         summary_card_content.append(html.P(f"{param.replace('_', ' ').title()}: {current_value:.2f} ({status})", style={'color': color}))

#     summary_card = [
#         html.H4("Current Status", className="card-title"),
#         html.Div(summary_card_content)
#     ]

#     # Send email notification if there are critical points
#     if critical_points:
#         subject = "Machine Failure Predicted"
#         body = "Critical values detected for the following parameters:\n"
#         for param, time, value in critical_points:
#             body += f"{param.replace('_', ' ').title()} at {time}: {value:.2f}\n"
#         send_email(subject, body)

#     return main_fig, history_fig, performance_fig, failure_fig, summary_card, update_interval * 1000, failure_detected, failure_periods

# # Callback to toggle interval updates
# @app.callback(
#     Output('graph-update', 'disabled'),
#     Input('pause-button', 'n_clicks'),
#     State('graph-update', 'disabled')
# )
# def toggle_pause_resume(n_clicks, currently_disabled):
#     if n_clicks is None:
#         return currently_disabled
#     return not currently_disabled

# # Callback for downloading data
# @app.callback(
#     Output("download-data", "data"),
#     Input("btn-download", "n_clicks"),
#     prevent_initial_call=True,
# )
# def func(n_clicks):
#     return dcc.send_data_frame(data.to_csv, "machine_data.csv")

# # Run the app
# if __name__ == '__main__':
#     app.run_server(debug=True)

# from dash import Dash, html, dcc, Input, Output, State
# import dash_bootstrap_components as dbc
# import pandas as pd
# import plotly.graph_objs as go
# import datetime
# import numpy as np
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import os
# from sklearn.linear_model import LinearRegression

# # Sample data generation function with a trend
# def generate_sample_data(start_date, days=30, trend='increasing'):
#     date_range = pd.date_range(start=start_date, periods=days, freq='D')
#     data = {
#         'time': date_range,
#         'strain': [],
#         'load': [],
#         'chain_position': [],
#         'vibration': [],
#         'temperature': [],
#         'chain_wear': [],
#         'torque': [],
#         'lubrication_level': [],
#         'patch_length': []
#     }

#     for date in date_range:
#         is_weekend = date.weekday() >= 5
#         base_multiplier = 0.7 if is_weekend else 1.0
#         if trend == 'increasing':
#             base = base_multiplier * np.linspace(0, 100, days)[len(data['strain'])]
#             variance = 5
#         else:
#             base = base_multiplier * np.linspace(100, 0, days)[len(data['strain'])]
#             variance = 5

#         data['strain'].append(base + np.random.uniform(-variance, variance))
#         data['load'].append(base + np.random.uniform(-variance, variance))
#         data['chain_position'].append(base * 10 + np.random.uniform(-variance * 10, variance * 10))
#         data['vibration'].append(base / 10 + np.random.uniform(-variance / 10, variance / 10))
#         data['temperature'].append(base / 2 + np.random.uniform(-variance / 2, variance / 2))
#         data['chain_wear'].append(base + np.random.uniform(-variance, variance))
#         data['torque'].append(base / 2 + np.random.uniform(-variance / 2, variance / 2))
#         data['lubrication_level'].append(base + np.random.uniform(-variance, variance))
#         data['patch_length'].append(base + np.random.uniform(-variance, variance))

#     return pd.DataFrame(data)

# # Function to send email notification
# # def send_email(subject, body):
# #     try:
# #         sender_email = os.getenv("leojoamalan6@gmail.com")
# #         receiver_email = os.getenv("leojoamalan@gmail.com")
# #         password = os.getenv("fjnpgiukmlninvch")

# #         msg = MIMEMultipart()
# #         msg['From'] = sender_email
# #         msg['To'] = receiver_email
# #         msg['Subject'] = subject

# #         msg.attach(MIMEText(body, 'plain'))

# #         with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
# #             server.login(sender_email, password)
# #             server.sendmail(sender_email, receiver_email, msg.as_string())
# #         print("Email sent successfully!")
# #     except Exception as e:
# #         print(f"Failed to send email: {e}")

# # Initialize the app
# app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# server = app.server

# # Generate initial data
# data = generate_sample_data(start_date=datetime.datetime.now() - datetime.timedelta(days=30), days=30, trend='increasing')

# # Define thresholds for each parameter
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

# # Function to predict future values using Linear Regression
# def predict_future_values(data, param, future_days=7):
#     X = np.arange(len(data)).reshape(-1, 1)  # Days as numerical values
#     y = data[param].values
#     model = LinearRegression()
#     model.fit(X, y)

#     future_X = np.arange(len(data), len(data) + future_days).reshape(-1, 1)
#     future_predictions = model.predict(future_X)
    
#     return future_predictions

# # Update the layout
# app.layout = html.Div([
#     dbc.Container([
#         html.H1("Machine Monitoring Dashboard", className="header-title"),
#         dbc.Row([
#             dbc.Col(dcc.DatePickerRange(
#                 id='date-picker-range',
#                 start_date=(datetime.datetime.now() - datetime.timedelta(days=30)).date(),
#                 end_date=datetime.datetime.now().date(),
#                 display_format='YYYY-MM-DD'
#             ), width=4),
#             dbc.Col(dcc.Dropdown(
#                 id='parameter-dropdown',
#                 options=[{'label': param.replace('_', ' ').title(), 'value': param} 
#                          for param in ['strain', 'load', 'chain_position', 'vibration', 'temperature', 
#                                        'chain_wear', 'torque', 'lubrication_level', 'patch_length']],
#                 value=['strain', 'load', 'temperature'],
#                 multi=True
#             ), width=4),
#             dbc.Col(dbc.Switch(
#                 id='dark-mode-switch',
#                 label="Dark Mode",
#                 value=False
#             ), width=2),
#             dbc.Col(dbc.Button("Pause/Resume", id="pause-button", color="primary"), width=2)
#         ], className="mb-4"),
#         dbc.Row([
#             dbc.Col(dcc.Graph(id='main-graph'), width=12),
#         ], className="mb-4"),
#         dbc.Row([
#             dbc.Col(dcc.Graph(id='history-graph'), width=12),
#         ], className="mb-4"),
#         dbc.Row([
#             dbc.Col(dcc.Graph(id='performance-analysis-graph'), width=12),
#         ], className="mb-4"),
#         dbc.Row([
#             dbc.Col(dcc.Graph(id='failure-graph'), width=12),
#         ], className="mb-4"),
#         dbc.Row([
#             dbc.Col(dbc.Card(id="summary-card", body=True), width=12)
#         ], className="mb-4"),
#         dbc.Row([
#             dbc.Col(dcc.Slider(
#                 id='update-interval-slider',
#                 min=1,
#                 max=60,
#                 step=1,
#                 value=5,
#                 marks={i: f'{i}s' for i in range(0, 61, 10)},
#                 tooltip={"placement": "bottom", "always_visible": True}
#             ), width=12)
#         ], className="mb-4"),
#         dbc.Row(
#             dbc.Col(
#                 dbc.Button("Download Data", id="btn-download", color="primary", className="mr-2"),
#                 width={"size": 2, "offset": 5},
#             ),
#         ),
#         dcc.Download(id="download-data"),
#         dcc.Interval(
#             id='graph-update',
#             interval=5*1000,
#             n_intervals=0,
#             disabled=False
#         ),
#         dcc.Store(id='failure-detected', data={param: False for param in thresholds.keys()}),
#         dcc.Store(id='failure-periods', data={param: [] for param in thresholds.keys()})
#     ], fluid=True),
# ], id="main-container")

# # Callback to update data and graphs
# @app.callback(
#     [Output('main-graph', 'figure'),
#      Output('history-graph', 'figure'),
#      Output('performance-analysis-graph', 'figure'),
#      Output('failure-graph', 'figure'),
#      Output('summary-card', 'children'),
#      Output('graph-update', 'interval'),
#      Output('failure-detected', 'data'),
#      Output('failure-periods', 'data')],
#     [Input('graph-update', 'n_intervals'),
#      Input('date-picker-range', 'start_date'),
#      Input('date-picker-range', 'end_date'),
#      Input('dark-mode-switch', 'value'),
#      Input('parameter-dropdown', 'value'),
#      Input('update-interval-slider', 'value')],
#     [State('failure-detected', 'data'),
#      State('failure-periods', 'data')]
# )
# def update_graphs(n_intervals, start_date, end_date, dark_mode, selected_params, update_interval, failure_detected, failure_periods):
#     global data
#     new_data = generate_sample_data(start_date=data['time'].iloc[-1] + datetime.timedelta(days=1), days=1).iloc[0]
#     data.loc[len(data)] = new_data

#     # Filter data based on date range
#     mask = (data['time'].dt.date >= pd.to_datetime(start_date).date()) & (data['time'].dt.date <= pd.to_datetime(end_date).date())
#     filtered_data = data.loc[mask]

#     # Set color scheme based on dark mode
#     bg_color = 'rgb(50, 50, 50)' if dark_mode else 'white'
#     text_color = 'white' if dark_mode else 'black'
#     plot_bg_color = 'rgb(30, 30, 30)' if dark_mode else 'rgb(240, 240, 240)'

#     # Create main graph
#     main_fig = go.Figure()
#     for param in selected_params:
#         main_fig.add_trace(go.Scatter(x=filtered_data['time'], y=filtered_data[param],
#                                       mode='lines+markers', name=param.replace('_', ' ').title()))

#     main_fig.update_layout(
#         title='Parameters Over Time',
#         xaxis_title='Time',
#         yaxis_title='Value',
#         paper_bgcolor=bg_color,
#         plot_bgcolor=plot_bg_color,
#         font={'color': text_color},
#         legend_title_text='Parameters'
#     )

#     # Create history graph
#     history_fig = go.Figure()
#     for param in selected_params:
#         history_fig.add_trace(go.Scatter(x=data['time'], y=data[param],
#                                          mode='lines', name=param.replace('_', ' ').title()))

#     history_fig.update_layout(
#         title='Historical Data',
#         xaxis_title='Time',
#         yaxis_title='Value',
#         paper_bgcolor=bg_color,
#         plot_bgcolor=plot_bg_color,
#         font={'color': text_color},
#         legend_title_text='Parameters'
#     )

#     # Create performance analysis graph
#     performance_data = data[selected_params].mean(axis=1)
#     performance_fig = go.Figure()
#     performance_fig.add_trace(go.Scatter(x=data['time'], y=performance_data, mode='lines+markers', name='Performance'))

#     performance_fig.update_layout(
#         title='Performance Analysis',
#         xaxis_title='Time',
#         yaxis_title='Performance Metric',
#         paper_bgcolor=bg_color,
#         plot_bgcolor=plot_bg_color,
#         font={'color': text_color}
#     )

#     # Update failure detection and failure periods
#     critical_points = []
#     sudden_changes = []
#     future_predictions = {param: predict_future_values(data, param) for param in selected_params}

#     for param in selected_params:
#         current_value = new_data[param]
#         threshold = thresholds[param]
#         status = determine_status(current_value, threshold)

#         # Detect critical status
#         if status == 'Critical':
#             failure_detected[param] = True
#             critical_points.append((param, data['time'].iloc[-1], current_value))
#             if not failure_periods[param] or failure_periods[param][-1][1] != data['time'].iloc[-1]:
#                 failure_periods[param].append((data['time'].iloc[-1], data['time'].iloc[-1]))
#         elif failure_detected[param]:
#             failure_periods[param][-1] = (failure_periods[param][-1][0], data['time'].iloc[-1])
#             failure_detected[param] = False

#         # Detect sudden changes
#         if len(data[param]) > 1:
#             recent_values = data[param].tail(2).values
#             change = recent_values[-1] - recent_values[-2]
#             if abs(change) > thresholds[param][1] * 0.2:  # 20% threshold for sudden change
#                 sudden_changes.append((param, data['time'].iloc[-1], recent_values[-1], change))

#     # Create failure graph
#     failure_fig = go.Figure()
#     for param in selected_params:
#         failure_fig.add_trace(go.Scatter(x=data['time'], y=data[param],
#                                          mode='lines', name=param.replace('_', ' ').title()))
#         for start, end in failure_periods[param]:
#             failure_fig.add_shape(
#                 type="rect",
#                 xref="x",
#                 yref="y",
#                 x0=start,
#                 x1=end,
#                 y0=0,
#                 y1=max(data[param]),
#                 fillcolor="red",
#                 opacity=0.3,
#                 line_width=0,
#             )

#     failure_fig.update_layout(
#         title='Potential Failure Points',
#         xaxis_title='Time',
#         yaxis_title='Value',
#         paper_bgcolor=bg_color,
#         plot_bgcolor=plot_bg_color,
#         font={'color': text_color}
#     )

#     # Create summary card
#     summary_card_content = []
#     for param in selected_params:
#         current_value = new_data[param]
#         threshold = thresholds[param]
#         status = determine_status(current_value, threshold)
#         color = 'green' if status == 'Normal' else 'orange' if status == 'Warning' else 'red'
#         summary_card_content.append(html.P(f"{param.replace('_', ' ').title()}: {current_value:.2f} ({status})", style={'color': color}))

#     summary_card = [
#         html.H4("Current Status", className="card-title"),
#         html.Div(summary_card_content)
#     ]

#     # Send email notification if there are critical points or sudden changes
#     if critical_points or sudden_changes:
#         subject = "Machine Monitoring Alerts"
#         body = ""
#         if critical_points:
#             body += "Critical values detected for the following parameters:\n"
#             for param, time, value in critical_points:
#                 body += f"{param.replace('_', ' ').title()} at {time}: {value:.2f}\n"
#         if sudden_changes:
#             body += "\nSudden changes detected for the following parameters:\n"
#             for param, time, value, change in sudden_changes:
#                 body += f"{param.replace('_', ' ').title()} at {time}: {value:.2f} (Change: {change:.2f})\n"
#         # send_email(subject, body)

#     return main_fig, history_fig, performance_fig, failure_fig, summary_card, update_interval * 1000, failure_detected, failure_periods

# # Callback to handle data download
# @app.callback(
#     Output("download-data", "data"),
#     Input("btn-download", "n_clicks"),
#     prevent_initial_call=True,
# )
# def download_data(n_clicks):
#     if n_clicks is None:
#         return None
#     # Convert data to CSV format
#     csv_string = data.to_csv(index=False, header=True)
#     return dcc.send_data_frame(data.to_csv, "machine_data.csv")

# # Run the app
# if __name__ == '__main__':
#     app.run_server(debug=True)

from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
import datetime
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from sklearn.linear_model import LinearRegression

# Sample data generation function with a trend
def generate_sample_data(start_date, days=30, trend='increasing'):
    date_range = pd.date_range(start=start_date, periods=days, freq='D')
    data = {
        'time': date_range,
        'strain': [],
        'load': [],
        'chain_position': [],
        'vibration': [],
        'temperature': [],
        'chain_wear': [],
        'torque': [],
        'lubrication_level': [],
        'patch_length': []
    }

    for date in date_range:
        is_weekend = date.weekday() >= 5
        base_multiplier = 0.7 if is_weekend else 1.0
        if trend == 'increasing':
            base = base_multiplier * np.linspace(0, 100, days)[len(data['strain'])]
            variance = 5
        else:
            base = base_multiplier * np.linspace(100, 0, days)[len(data['strain'])]
            variance = 5

        data['strain'].append(base + np.random.uniform(-variance, variance))
        data['load'].append(base + np.random.uniform(-variance, variance))
        data['chain_position'].append(base * 10 + np.random.uniform(-variance * 10, variance * 10))
        data['vibration'].append(base / 10 + np.random.uniform(-variance / 10, variance / 10))
        data['temperature'].append(base / 2 + np.random.uniform(-variance / 2, variance / 2))
        data['chain_wear'].append(base + np.random.uniform(-variance, variance))
        data['torque'].append(base / 2 + np.random.uniform(-variance / 2, variance / 2))
        data['lubrication_level'].append(base + np.random.uniform(-variance, variance))
        data['patch_length'].append(base + np.random.uniform(-variance, variance))

    return pd.DataFrame(data)

# Function to send email notification
# def send_email(subject, body):
#     try:
#         sender_email = os.getenv("leojoamalan6@gmail.com")
#         receiver_email = os.getenv("leojoamalan@gmail.com")
#         password = os.getenv("fjnpgiukmlninvch")

#         msg = MIMEMultipart()
#         msg['From'] = sender_email
#         msg['To'] = receiver_email
#         msg['Subject'] = subject

#         msg.attach(MIMEText(body, 'plain'))

#         with smtplib.SMTP_SSL("smtp.gmail.com", 587) as server:
#             server.login(sender_email, password)
#             server.sendmail(sender_email, receiver_email, msg.as_string())
#         print("Email sent successfully!")
#     except Exception as e:
#         print(f"Failed to send email: {e}")
import logging
from dotenv import load_dotenv
import os

load_dotenv() 

# Configure the logger
logging.basicConfig(
    level=logging.INFO,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log message format
)

# Create a logger object
logger = logging.getLogger(__name__)

def send_email(subject, body):
    try:
        sender_email = os.getenv("leojoamalan6@gmail.com")
        receiver_email = os.getenv("leo.s@solidpro-es.com")
        password = os.getenv("ldwzeqmgubfiqnld")

        if not sender_email or not receiver_email or not password:
            logger.error("Email environment variables not set properly.")
            return

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        # Try SSL connection first
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
        except smtplib.SMTPException as e:
            logger.warning(f"SSL connection failed: {e}")
            # Fall back to TLS
            try:
                with smtplib.SMTP("smtp.gmail.com", 587) as server:
                    server.starttls()
                    server.login(sender_email, password)
                    server.sendmail(sender_email, receiver_email, msg.as_string())
            except smtplib.SMTPException as e:
                logger.error(f"Failed to send email: {e}")

        logger.info("Email sent successfully!")
    except Exception as e:
        logger.error(f"Failed to send email: {e}")

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Generate initial data
data = generate_sample_data(start_date=datetime.datetime.now() - datetime.timedelta(days=30), days=30, trend='increasing')

# Define thresholds for each parameter
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

# Function to detect sudden changes
def detect_sudden_changes(data, param, threshold=10):
    recent_values = data[param].tail(2)
    if len(recent_values) < 2:
        return False
    change = abs(recent_values.iloc[-1] - recent_values.iloc[-2])
    return change > threshold

# Function to predict future values using Linear Regression
def predict_future_values(data, param, future_days=7):
    X = np.arange(len(data)).reshape(-1, 1)  # Days as numerical values
    y = data[param].values
    model = LinearRegression()
    model.fit(X, y)

    future_X = np.arange(len(data), len(data) + future_days).reshape(-1, 1)
    future_predictions = model.predict(future_X)
    
    return future_predictions

# Update the layout
app.layout = html.Div([
    dbc.Container([
        html.H1("Machine Monitoring Dashboard", className="header-title"),
        dbc.Row([
            dbc.Col(dcc.DatePickerRange(
                id='date-picker-range',
                start_date=(datetime.datetime.now() - datetime.timedelta(days=30)).date(),
                end_date=datetime.datetime.now().date(),
                display_format='YYYY-MM-DD'
            ), width=4),
            dbc.Col(dcc.Dropdown(
                id='parameter-dropdown',
                options=[{'label': param.replace('_', ' ').title(), 'value': param} 
                         for param in ['strain', 'load', 'chain_position', 'vibration', 'temperature', 
                                       'chain_wear', 'torque', 'lubrication_level', 'patch_length']],
                value=['strain', 'load', 'temperature'],
                multi=True
            ), width=4),
            dbc.Col(dbc.Switch(
                id='dark-mode-switch',
                label="Dark Mode",
                value=False
            ), width=2),
            dbc.Col(dbc.Button("Pause/Resume", id="pause-button", color="primary"), width=2)
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(dcc.Graph(id='main-graph'), width=12),
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(dcc.Graph(id='history-graph'), width=12),
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(dcc.Graph(id='performance-analysis-graph'), width=12),
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(dcc.Graph(id='failure-graph'), width=12),
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(dbc.Card(id="summary-card", body=True), width=12)
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(dcc.Slider(
                id='update-interval-slider',
                min=1,
                max=60,
                step=1,
                value=5,
                marks={i: f'{i}s' for i in range(0, 61, 10)},
                tooltip={"placement": "bottom", "always_visible": True}
            ), width=12)
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(dbc.Button("Download Data", id="btn-download", color="primary", className="mr-2"), width={"size": 2, "offset": 5}),
            dbc.Col(dbc.Button("Send Email", id="btn-send-email", color="danger"), width={"size": 2}),
        ], className="mb-4"),
        dcc.Download(id="download-data"),
        dcc.Interval(
            id='graph-update',
            interval=5*1000,
            n_intervals=0,
            disabled=False
        ),
        dcc.Store(id='failure-detected', data={param: False for param in thresholds.keys()}),
        dcc.Store(id='failure-periods', data={param: [] for param in thresholds.keys()})
    ], fluid=True),
], id="main-container")

# Callback to update data and graphs
@app.callback(
    [Output('main-graph', 'figure'),
     Output('history-graph', 'figure'),
     Output('performance-analysis-graph', 'figure'),
     Output('failure-graph', 'figure'),
     Output('summary-card', 'children'),
     Output('graph-update', 'interval'),
     Output('failure-detected', 'data'),
     Output('failure-periods', 'data')],
    [Input('graph-update', 'n_intervals'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('dark-mode-switch', 'value'),
     Input('parameter-dropdown', 'value'),
     Input('update-interval-slider', 'value')],
    [State('failure-detected', 'data'),
     State('failure-periods', 'data')]
)
def update_graphs(n_intervals, start_date, end_date, dark_mode, selected_params, update_interval, failure_detected, failure_periods):
    global data
    new_data = generate_sample_data(start_date=data['time'].iloc[-1] + datetime.timedelta(days=1), days=1).iloc[0]
    data.loc[len(data)] = new_data

    # Filter data based on date range
    mask = (data['time'].dt.date >= pd.to_datetime(start_date).date()) & (data['time'].dt.date <= pd.to_datetime(end_date).date())
    filtered_data = data.loc[mask]

    # Set color scheme based on dark mode
    bg_color = 'rgb(50, 50, 50)' if dark_mode else 'white'
    text_color = 'white' if dark_mode else 'black'
    plot_bg_color = 'rgb(30, 30, 30)' if dark_mode else 'rgb(240, 240, 240)'

    # Create main graph
    main_fig = go.Figure()
    for param in selected_params:
        main_fig.add_trace(go.Scatter(x=filtered_data['time'], y=filtered_data[param],
                                      mode='lines+markers', name=param.replace('_', ' ').title()))

    main_fig.update_layout(
        title='Parameters Over Time',
        xaxis_title='Time',
        yaxis_title='Value',
        paper_bgcolor=bg_color,
        plot_bgcolor=plot_bg_color,
        font={'color': text_color},
        legend_title_text='Parameters'
    )

    # Create history graph
    history_fig = go.Figure()
    for param in selected_params:
        history_fig.add_trace(go.Scatter(x=data['time'], y=data[param],
                                         mode='lines', name=param.replace('_', ' ').title()))

    history_fig.update_layout(
        title='Historical Data',
        xaxis_title='Time',
        yaxis_title='Value',
        paper_bgcolor=bg_color,
        plot_bgcolor=plot_bg_color,
        font={'color': text_color},
        legend_title_text='Parameters'
    )

    # Create performance analysis graph
    performance_data = data[selected_params].mean(axis=1)
    performance_fig = go.Figure()
    performance_fig.add_trace(go.Scatter(x=data['time'], y=performance_data, mode='lines+markers', name='Performance'))

    performance_fig.update_layout(
        title='Performance Analysis',
        xaxis_title='Time',
        yaxis_title='Performance Metric',
        paper_bgcolor=bg_color,
        plot_bgcolor=plot_bg_color,
        font={'color': text_color}
    )

    # Create failure detection graph
    failure_fig = go.Figure()
    for param in selected_params:
        failure_fig.add_trace(go.Scatter(x=data['time'], y=data[param],
                                         mode='lines', name=param.replace('_', ' ').title()))
        for start, end in failure_periods[param]:
            failure_fig.add_shape(
                type="rect",
                xref="x",
                yref="y",
                x0=start,
                x1=end,
                y0=0,
                y1=max(data[param]),
                fillcolor="red",
                opacity=0.3,
                line_width=0,
            )

    failure_fig.update_layout(
        title='Potential Failure Points',
        xaxis_title='Time',
        yaxis_title='Value',
        paper_bgcolor=bg_color,
        plot_bgcolor=plot_bg_color,
        font={'color': text_color}
    )

    # Create summary card
    summary_card_content = []
    for param in selected_params:
        current_value = new_data[param]
        threshold = thresholds[param]
        status = determine_status(current_value, threshold)
        color = 'green' if status == 'Normal' else 'orange' if status == 'Warning' else 'red'
        summary_card_content.append(html.P(f"{param.replace('_', ' ').title()}: {current_value:.2f} ({status})", style={'color': color}))

    summary_card = [
        html.H4("Current Status", className="card-title"),
        html.Div(summary_card_content)
    ]

    # Update failure detection and failure periods
    critical_points = []
    sudden_changes = []
    future_predictions = {param: predict_future_values(data, param) for param in selected_params}

    for param in selected_params:
        current_value = new_data[param]
        threshold = thresholds[param]
        status = determine_status(current_value, threshold)

        # Check for critical status
        if status == 'Critical':
            failure_detected[param] = True
            critical_points.append((param, data['time'].iloc[-1], current_value))
            if not failure_periods[param] or failure_periods[param][-1][1] != data['time'].iloc[-1]:
                failure_periods[param].append((data['time'].iloc[-1], data['time'].iloc[-1]))
        elif failure_detected[param]:
            failure_periods[param][-1] = (failure_periods[param][-1][0], data['time'].iloc[-1])
            failure_detected[param] = False

        # Detect sudden changes
        if detect_sudden_changes(data, param):
            sudden_changes.append(param)

    # Send email notification if there are critical points or sudden changes
    if critical_points or sudden_changes:
        subject = "Machine Alert Notification"
        body = "The following issues have been detected:\n\n"

        if critical_points:
            body += "Critical values detected for the following parameters:\n"
            for param, time, value in critical_points:
                body += f"{param.replace('_', ' ').title()} at {time}: {value:.2f}\n"

        if sudden_changes:
            body += "\nSudden changes detected in the following parameters:\n"
            for param in sudden_changes:
                body += f"{param.replace('_', ' ').title()}\n"

        send_email(subject, body)

    return main_fig, history_fig, performance_fig, failure_fig, summary_card, update_interval * 1000, failure_detected, failure_periods

# Callback to toggle interval updates
@app.callback(
    Output('graph-update', 'disabled'),
    Input('pause-button', 'n_clicks'),
    State('graph-update', 'disabled')
)
def toggle_pause_resume(n_clicks, currently_disabled):
    if n_clicks is None:
        return currently_disabled
    return not currently_disabled

# Callback for downloading data
@app.callback(
    Output("download-data", "data"),
    Input("btn-download", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_data_frame(data.to_csv, "machine_data.csv")

# Callback for sending email manually
@app.callback(
    Output('btn-send-email', 'children'),
    Input('btn-send-email', 'n_clicks'),
    prevent_initial_call=True
)
def manual_send_email(n_clicks):
    if n_clicks:
        subject = "Manual Alert Notification"
        body = "This is a manual alert notification."
        send_email(subject, body)
        return "Email Sent"
    return "Send Email Now"

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
