# from dash import Dash, html, dcc, Input, Output, callback, State
# import dash_bootstrap_components as dbc
# import pandas as pd
# import plotly.graph_objs as go
# import plotly.express as px
# import random
# import datetime

# # Sample data generation function (unchanged)
# def generate_sample_data():
#     return {
#         'time': datetime.datetime.now(),
#         'strain': random.uniform(0, 100),
#         'load': random.uniform(0, 100),
#         'chain_position': random.uniform(0, 1000),
#         'vibration': random.uniform(0, 10),
#         'temperature': random.uniform(10, 50),
#         'chain_wear': random.uniform(0, 100),
#         'torque': random.uniform(0, 50),
#         'lubrication_level': random.uniform(0, 100),
#         'patch_length': random.uniform(0, 100)
#     }

# # Initialize the app
# app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# server = app.server

# # Sample initial data
# data = pd.DataFrame(columns=['time', 'strain', 'load', 'chain_position', 'vibration', 
#                              'temperature', 'chain_wear', 'torque', 'lubrication_level', 'patch_length'])

# # Define thresholds for each parameter (unchanged)
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

# # Define function to generate gauge chart
# def generate_gauge_chart(value, title, threshold):
#     return go.Figure(go.Indicator(
#         mode = "gauge+number",
#         value = value,
#         title = {'text': title},
#         gauge = {
#             'axis': {'range': [None, threshold[1]*1.2]},
#             'bar': {'color': "darkblue"},
#             'steps': [
#                 {'range': [0, threshold[0]], 'color': "lightgreen"},
#                 {'range': [threshold[0], threshold[1]], 'color': "yellow"},
#                 {'range': [threshold[1], threshold[1]*1.2], 'color': "red"}
#             ],
#             'threshold': {
#                 'line': {'color': "red", 'width': 4},
#                 'thickness': 0.75,
#                 'value': threshold[1]
#             }
#         }
#     ))

# # Update the layout
# app.layout = html.Div([
#     dbc.Container([
#         html.H1("Machine Monitoring Dashboard", className="header-title"),
#         dbc.Row([
#             dbc.Col(dcc.DatePickerRange(
#                 id='date-picker-range',
#                 start_date=datetime.datetime.now().date(),
#                 end_date=datetime.datetime.now().date(),
#                 display_format='YYYY-MM-DD'
#             ), width=6),
#             dbc.Col(dbc.Switch(
#                 id='dark-mode-switch',
#                 label="Dark Mode",
#                 value=False
#             ), width=6, className="text-right")
#         ], className="mb-4"),
#         dbc.Row([
#             dbc.Col(dcc.Graph(id='strain-gauge'), width=4),
#             dbc.Col(dcc.Graph(id='load-gauge'), width=4),
#             dbc.Col(dcc.Graph(id='temperature-gauge'), width=4),
#         ], className="mb-4"),
#         dbc.Row([
#             dbc.Col(dcc.Graph(id='strain-graph'), width=6),
#             dbc.Col(dcc.Graph(id='load-graph'), width=6),
#         ], className="mb-4"),
#         dbc.Row([
#             dbc.Col(dcc.Graph(id='chain-position-graph'), width=6),
#             dbc.Col(dcc.Graph(id='vibration-graph'), width=6),
#         ], className="mb-4"),
#         dbc.Row([
#             dbc.Col(dcc.Graph(id='temperature-graph'), width=6),
#             dbc.Col(dcc.Graph(id='chain-wear-graph'), width=6),
#         ], className="mb-4"),
#         dbc.Row([
#             dbc.Col(dcc.Graph(id='torque-graph'), width=6),
#             dbc.Col(dcc.Graph(id='lubrication-level-graph'), width=6),
#         ], className="mb-4"),
#         dbc.Row([
#             dbc.Col(dcc.Graph(id='patch-length-graph'), width=6),
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
#             interval=5*1000,  # Update every 5 seconds
#             n_intervals=0,
#             disabled=False
#         )
#     ], fluid=True),
# ], id="main-container")

# # Callback to update data and graphs
# @app.callback(
#     [Output('strain-gauge', 'figure'),
#      Output('load-gauge', 'figure'),
#      Output('temperature-gauge', 'figure'),
#      Output('strain-graph', 'figure'),
#      Output('load-graph', 'figure'),
#      Output('chain-position-graph', 'figure'),
#      Output('vibration-graph', 'figure'),
#      Output('temperature-graph', 'figure'),
#      Output('chain-wear-graph', 'figure'),
#      Output('torque-graph', 'figure'),
#      Output('lubrication-level-graph', 'figure'),
#      Output('patch-length-graph', 'figure')],
#     [Input('graph-update', 'n_intervals'),
#      Input('date-picker-range', 'start_date'),
#      Input('date-picker-range', 'end_date'),
#      Input('dark-mode-switch', 'value')]
# )
# def update_graphs(n_intervals, start_date, end_date, dark_mode):
#     new_data = generate_sample_data()
#     data.loc[len(data)] = new_data

#     # Filter data based on date range
#     mask = (data['time'].dt.date >= pd.to_datetime(start_date).date()) & (data['time'].dt.date <= pd.to_datetime(end_date).date())
#     filtered_data = data.loc[mask]

#     # Set color scheme based on dark mode
#     bg_color = 'rgb(50, 50, 50)' if dark_mode else 'white'
#     text_color = 'white' if dark_mode else 'black'
#     plot_bg_color = 'rgb(30, 30, 30)' if dark_mode else 'rgb(240, 240, 240)'

#     # Create gauge charts
#     strain_gauge = generate_gauge_chart(new_data['strain'], 'Strain (μstrain)', thresholds['strain'])
#     load_gauge = generate_gauge_chart(new_data['load'], 'Load (kg)', thresholds['load'])
#     temp_gauge = generate_gauge_chart(new_data['temperature'], 'Temperature (°C)', thresholds['temperature'])

#     # Update layout for dark mode
#     for gauge in [strain_gauge, load_gauge, temp_gauge]:
#         gauge.update_layout(
#             paper_bgcolor=bg_color,
#             font={'color': text_color},
#             plot_bgcolor=plot_bg_color
#         )

#     # Create line graphs
#     graphs = []
#     for column in ['strain', 'load', 'chain_position', 'vibration', 'temperature', 'chain_wear', 'torque', 'lubrication_level', 'patch_length']:
#         fig = px.line(filtered_data, x='time', y=column, title=f'{column.replace("_", " ").title()}')
#         fig.update_traces(mode='lines+markers')
#         fig.update_layout(
#             paper_bgcolor=bg_color,
#             plot_bgcolor=plot_bg_color,
#             font={'color': text_color},
#             xaxis=dict(showgrid=True, gridcolor='gray'),
#             yaxis=dict(showgrid=True, gridcolor='gray')
#         )
#         graphs.append(fig)

#     return [strain_gauge, load_gauge, temp_gauge] + graphs

# # Callback to download data (unchanged)
# @app.callback(
#     Output("download-data", "data"),
#     [Input("btn-download", "n_clicks")],
#     prevent_initial_call=True,
# )
# def download_data(n_clicks):
#     data_export = data.copy()
#     data_export['time'] = pd.to_datetime(data_export['time']).dt.strftime('%Y-%m-%d %H:%M:%S')
#     return dcc.send_data_frame(data_export.to_csv, "machine_data.csv", index=False)

# if __name__ == '__main__':
#     app.run_server(debug=True)

from dash import Dash, html, dcc, Input, Output, callback, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import random
import datetime

# Sample data generation function (unchanged)
def generate_sample_data():
    return {
        'time': datetime.datetime.now(),
        'strain': random.uniform(0, 100),
        'load': random.uniform(0, 100),
        'chain_position': random.uniform(0, 1000),
        'vibration': random.uniform(0, 10),
        'temperature': random.uniform(10, 50),
        'chain_wear': random.uniform(0, 100),
        'torque': random.uniform(0, 50),
        'lubrication_level': random.uniform(0, 100),
        'patch_length': random.uniform(0, 100)
    }

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Sample initial data
data = pd.DataFrame(columns=['time', 'strain', 'load', 'chain_position', 'vibration', 
                             'temperature', 'chain_wear', 'torque', 'lubrication_level', 'patch_length'])

# Define thresholds for each parameter (unchanged)
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

# Define function to generate gauge chart
def generate_gauge_chart(value, title, threshold):
    return go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        title = {'text': title},
        gauge = {
            'axis': {'range': [None, threshold[1]*1.2]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, threshold[0]], 'color': "lightgreen"},
                {'range': [threshold[0], threshold[1]], 'color': "yellow"},
                {'range': [threshold[1], threshold[1]*1.2], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': threshold[1]
            }
        }
    ))

# Define function to determine status
def determine_status(value, threshold):
    if value < threshold[0]:
        return 'Normal'
    elif value < threshold[1]:
        return 'Warning'
    else:
        return 'Critical'

# Update the layout
app.layout = html.Div([
    dbc.Container([
        html.H1("Machine Monitoring Dashboard", className="header-title"),
        dbc.Row([
            dbc.Col(dcc.DatePickerRange(
                id='date-picker-range',
                start_date=datetime.datetime.now().date(),
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
            dbc.Col(dcc.Graph(id='strain-gauge'), width=4),
            dbc.Col(dcc.Graph(id='load-gauge'), width=4),
            dbc.Col(dcc.Graph(id='temperature-gauge'), width=4),
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
        dbc.Row(
            dbc.Col(
                dbc.Button("Download Data", id="btn-download", color="primary", className="mr-2"),
                width={"size": 2, "offset": 5},
            ),
        ),
        dcc.Download(id="download-data"),
        dcc.Interval(
            id='graph-update',
            interval=5*1000,  # Update every 5 seconds initially
            n_intervals=0,
            disabled=False
        )
    ], fluid=True),
], id="main-container")

# Callback to update data and graphs
@app.callback(
    [Output('main-graph', 'figure'),
     Output('strain-gauge', 'figure'),
     Output('load-gauge', 'figure'),
     Output('temperature-gauge', 'figure'),
     Output('summary-card', 'children'),
     Output('graph-update', 'interval')],
    [Input('graph-update', 'n_intervals'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('dark-mode-switch', 'value'),
     Input('parameter-dropdown', 'value'),
     Input('update-interval-slider', 'value')]
)
def update_graphs(n_intervals, start_date, end_date, dark_mode, selected_params, update_interval):
    new_data = generate_sample_data()
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
        title='Selected Parameters Over Time',
        xaxis_title='Time',
        yaxis_title='Value',
        paper_bgcolor=bg_color,
        plot_bgcolor=plot_bg_color,
        font={'color': text_color},
        legend_title_text='Parameters'
    )

    # Create gauge charts
    strain_gauge = generate_gauge_chart(new_data['strain'], 'Strain (μstrain)', thresholds['strain'])
    load_gauge = generate_gauge_chart(new_data['load'], 'Load (kg)', thresholds['load'])
    temp_gauge = generate_gauge_chart(new_data['temperature'], 'Temperature (°C)', thresholds['temperature'])

    # Update layout for dark mode
    for gauge in [strain_gauge, load_gauge, temp_gauge]:
        gauge.update_layout(
            paper_bgcolor=bg_color,
            font={'color': text_color},
            plot_bgcolor=plot_bg_color
        )

    # Create summary card
    summary_card = dbc.Card([
        dbc.CardHeader("Latest Values"),
        dbc.CardBody([
            html.P(f"{param.replace('_', ' ').title()}: {new_data[param]:.2f} - Status: {determine_status(new_data[param], thresholds[param])}")
            for param in selected_params
        ])
    ])

    return main_fig, strain_gauge, load_gauge, temp_gauge, summary_card, update_interval * 1000

# Callback to pause/resume updates
@app.callback(
    Output('graph-update', 'disabled'),
    Input('pause-button', 'n_clicks'),
    State('graph-update', 'disabled')
)
def toggle_interval(n_clicks, current_state):
    if n_clicks:
        return not current_state
    return current_state

# Callback to download data (unchanged)
@app.callback(
    Output("download-data", "data"),
    Input("btn-download", "n_clicks"),
    prevent_initial_call=True,
)
def download_data(n_clicks):
    data_export = data.copy()
    data_export['time'] = pd.to_datetime(data_export['time']).dt.strftime('%Y-%m-%d %H:%M:%S')
    return dcc.send_data_frame(data_export.to_csv, "machine_data.csv", index=False)

if __name__ == '__main__':
    app.run_server(debug=True)