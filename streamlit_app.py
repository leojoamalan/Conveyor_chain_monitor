# import streamlit as st
# import pandas as pd
# import plotly.graph_objs as go
# import random
# import datetime
# import time

# # Sample data generation function
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

# # Sample initial data
# data = pd.DataFrame([generate_sample_data() for _ in range(10)])

# # Streamlit app
# st.set_page_config(page_title="Machine Monitoring Dashboard", layout="wide")
# st.title("Machine Monitoring Dashboard")

# # Layout for stats cards
# cols = st.columns(4)
# stats = [
#     {"id": "strain", "title": "Strain (μstrain)"},
#     {"id": "load", "title": "Load (kg)"},
#     {"id": "chain_position", "title": "Chain Position (mm)"},
#     {"id": "vibration", "title": "Vibration (g)"},
#     {"id": "temperature", "title": "Temperature (°C)"},
#     {"id": "chain_wear", "title": "Chain Wear (%)"},
#     {"id": "torque", "title": "Torque (Nm)"},
#     {"id": "lubrication_level", "title": "Lubrication Level (%)"},
#     {"id": "patch_length", "title": "Patch Length (mm)"}
# ]

# # Function to display a stat card
# def display_stat_card(col, stat, value, percentage):
#     col.metric(stat["title"], f"{value:.2f}", f"{percentage:.2f}%")
#     col.image(stat["icon"], width=50)

# # Function to generate traces for plotting
# def generate_trace(data, y, name):
#     return go.Scatter(x=data['time'], y=data[y], mode='lines+markers', name=name)

# # Function to plot graphs
# def plot_graph(data, y, title):
#     trace = generate_trace(data, y, title)
#     layout = go.Layout(title=title)
#     fig = go.Figure(data=[trace], layout=layout)
#     st.plotly_chart(fig, use_container_width=True)

# while True:
#     new_data = generate_sample_data()
#     data.loc[len(data)] = new_data
#     if len(data) > 100:
#         data.drop(data.index[0], inplace=True)  # Keep data within a limit

#     strain_percentage = ((new_data['strain'] - data.iloc[-2]['strain']) / data.iloc[-2]['strain']) * 100 if len(data) > 1 else 0
#     load_percentage = ((new_data['load'] - data.iloc[-2]['load']) / data.iloc[-2]['load']) * 100 if len(data) > 1 else 0
#     chain_position_percentage = ((new_data['chain_position'] - data.iloc[-2]['chain_position']) / data.iloc[-2]['chain_position']) * 100 if len(data) > 1 else 0
#     vibration_percentage = ((new_data['vibration'] - data.iloc[-2]['vibration']) / data.iloc[-2]['vibration']) * 100 if len(data) > 1 else 0
#     temperature_percentage = ((new_data['temperature'] - data.iloc[-2]['temperature']) / data.iloc[-2]['temperature']) * 100 if len(data) > 1 else 0
#     chain_wear_percentage = ((new_data['chain_wear'] - data.iloc[-2]['chain_wear']) / data.iloc[-2]['chain_wear']) * 100 if len(data) > 1 else 0
#     torque_percentage = ((new_data['torque'] - data.iloc[-2]['torque']) / data.iloc[-2]['torque']) * 100 if len(data) > 1 else 0
#     lubrication_level_percentage = ((new_data['lubrication_level'] - data.iloc[-2]['lubrication_level']) / data.iloc[-2]['lubrication_level']) * 100 if len(data) > 1 else 0
#     patch_length_percentage = ((new_data['patch_length'] - data.iloc[-2]['patch_length']) / data.iloc[-2]['patch_length']) * 100 if len(data) > 1 else 0

#     with st.container():
#         cols = st.columns(4)
#         for i, stat in enumerate(stats[:4]):
#             display_stat_card(cols[i], stat, new_data[stat["id"]], eval(f"{stat['id']}_percentage"))

#         plot_graph(data, 'strain', 'Strain (μstrain)')
#         plot_graph(data, 'load', 'Load (kg)')

#         cols = st.columns(4)
#         for i, stat in enumerate(stats[4:8]):
#             display_stat_card(cols[i], stat, new_data[stat["id"]], eval(f"{stat['id']}_percentage"))

#         plot_graph(data, 'chain_position', 'Chain Position (mm)')
#         plot_graph(data, 'vibration', 'Vibration (g)')

#         cols = st.columns(4)
#         display_stat_card(cols[0], stats[8], new_data[stats[8]["id"]], patch_length_percentage)

#         plot_graph(data, 'temperature', 'Temperature (°C)')
#         plot_graph(data, 'chain_wear', 'Chain Wear (%)')
#         plot_graph(data, 'torque', 'Torque (Nm)')
#         plot_graph(data, 'lubrication_level', 'Lubrication Level (%)')
#         plot_graph(data, 'patch_length', 'Patch Length (mm)')

#     time.sleep(5)  # Update every 5 seconds
# import streamlit as st
# import pandas as pd
# import plotly.graph_objs as go
# import random
# import datetime
# import time

# # Sample data generation function
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

# # Sample initial data
# data = pd.DataFrame([generate_sample_data() for _ in range(10)])

# # Streamlit app
# st.set_page_config(page_title="Machine Monitoring Dashboard", layout="wide")
# st.title("Machine Monitoring Dashboard")

# # Layout for stats cards
# cols = st.columns(4)
# stats = [
#     {"id": "strain", "title": "Strain (μstrain)"},
#     {"id": "load", "title": "Load (kg)"},
#     {"id": "chain_position", "title": "Chain Position (mm)"},
#     {"id": "vibration", "title": "Vibration (g)"},
#     {"id": "temperature", "title": "Temperature (°C)"},
#     {"id": "chain_wear", "title": "Chain Wear (%)"},
#     {"id": "torque", "title": "Torque (Nm)"},
#     {"id": "lubrication_level", "title": "Lubrication Level (%)"},
#     {"id": "patch_length", "title": "Patch Length (mm)"}
# ]

# # Function to display a stat card
# def display_stat_card(col, stat, value, percentage):
#     col.metric(stat["title"], f"{value:.2f}", f"{percentage:.2f}%")

# # Function to generate traces for plotting
# def generate_trace(data, y, name):
#     return go.Scatter(x=data['time'], y=data[y], mode='lines+markers', name=name)

# # Function to plot graphs
# def plot_graph(data, y, title):
#     trace = generate_trace(data, y, title)
#     layout = go.Layout(title=title)
#     fig = go.Figure(data=[trace], layout=layout)
#     st.plotly_chart(fig, use_container_width=True)

# while True:
#     new_data = generate_sample_data()
#     data.loc[len(data)] = new_data
#     if len(data) > 100:
#         data.drop(data.index[0], inplace=True)  # Keep data within a limit

#     strain_percentage = ((new_data['strain'] - data.iloc[-2]['strain']) / data.iloc[-2]['strain']) * 100 if len(data) > 1 else 0
#     load_percentage = ((new_data['load'] - data.iloc[-2]['load']) / data.iloc[-2]['load']) * 100 if len(data) > 1 else 0
#     chain_position_percentage = ((new_data['chain_position'] - data.iloc[-2]['chain_position']) / data.iloc[-2]['chain_position']) * 100 if len(data) > 1 else 0
#     vibration_percentage = ((new_data['vibration'] - data.iloc[-2]['vibration']) / data.iloc[-2]['vibration']) * 100 if len(data) > 1 else 0
#     temperature_percentage = ((new_data['temperature'] - data.iloc[-2]['temperature']) / data.iloc[-2]['temperature']) * 100 if len(data) > 1 else 0
#     chain_wear_percentage = ((new_data['chain_wear'] - data.iloc[-2]['chain_wear']) / data.iloc[-2]['chain_wear']) * 100 if len(data) > 1 else 0
#     torque_percentage = ((new_data['torque'] - data.iloc[-2]['torque']) / data.iloc[-2]['torque']) * 100 if len(data) > 1 else 0
#     lubrication_level_percentage = ((new_data['lubrication_level'] - data.iloc[-2]['lubrication_level']) / data.iloc[-2]['lubrication_level']) * 100 if len(data) > 1 else 0
#     patch_length_percentage = ((new_data['patch_length'] - data.iloc[-2]['patch_length']) / data.iloc[-2]['patch_length']) * 100 if len(data) > 1 else 0

#     with st.container():
#         cols = st.columns(4)
#         for i, stat in enumerate(stats[:4]):
#             display_stat_card(cols[i], stat, new_data[stat["id"]], eval(f"{stat['id']}_percentage"))

#         plot_graph(data, 'strain', 'Strain (μstrain)')
#         plot_graph(data, 'load', 'Load (kg)')

#         cols = st.columns(4)
#         for i, stat in enumerate(stats[4:8]):
#             display_stat_card(cols[i], stat, new_data[stat["id"]], eval(f"{stat['id']}_percentage"))

#         plot_graph(data, 'chain_position', 'Chain Position (mm)')
#         plot_graph(data, 'vibration', 'Vibration (g)')

#         cols = st.columns(4)
#         display_stat_card(cols[0], stats[8], new_data[stats[8]["id"]], patch_length_percentage)

#         plot_graph(data, 'temperature', 'Temperature (°C)')
#         plot_graph(data, 'chain_wear', 'Chain Wear (%)')
#         plot_graph(data, 'torque', 'Torque (Nm)')
#         plot_graph(data, 'lubrication_level', 'Lubrication Level (%)')
#         plot_graph(data, 'patch_length', 'Patch Length (mm)')

#     time.sleep(5)  # Update every 5 seconds
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
import random
import datetime
from sklearn.linear_model import LinearRegression
import numpy as np

# Sample data generation function
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
        ),
        dcc.Store(id='failure-detected', data=False)
    ], fluid=True),
], id="main-container")

# Callback to update data and graphs
@app.callback(
    [Output('main-graph', 'figure'),
     Output('summary-card', 'children'),
     Output('graph-update', 'interval'),
     Output('failure-detected', 'data')],
    [Input('graph-update', 'n_intervals'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('dark-mode-switch', 'value'),
     Input('parameter-dropdown', 'value'),
     Input('update-interval-slider', 'value')],
    [State('failure-detected', 'data')]
)
def update_graphs(n_intervals, start_date, end_date, dark_mode, selected_params, update_interval, failure_detected):
    if failure_detected:
        raise dash.exceptions.PreventUpdate

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
    
    failure_time = None
    failure_param = None

    for param in selected_params:
        main_fig.add_trace(go.Scatter(x=filtered_data['time'], y=filtered_data[param],
                                      mode='lines+markers', name=param.replace('_', ' ').title()))

        # Forecast failure points using a simple linear regression model
        X = np.array(range(len(filtered_data))).reshape(-1, 1)
        y = filtered_data[param].values
        if len(X) > 1:
            model = LinearRegression().fit(X, y)
            X_pred = np.array(range(len(filtered_data), len(filtered_data) + 100)).reshape(-1, 1)
            y_pred = model.predict(X_pred)
            failure_index = np.argmax(y_pred >= thresholds[param][1]) if np.any(y_pred >= thresholds[param][1]) else None
            if failure_index is not None:
                param_failure_time = filtered_data['time'].iloc[-1] + pd.Timedelta(seconds=failure_index)
                if failure_time is None or param_failure_time < failure_time:
                    failure_time = param_failure_time
                    failure_param = param
                
                # Add the forecasted line to the main graph
                forecast_times = [filtered_data['time'].iloc[-1] + pd.Timedelta(seconds=i) for i in range(len(y_pred))]
                main_fig.add_trace(go.Scatter(x=forecast_times, y=y_pred, mode='lines', name=f'{param} Forecast',
                                              line=dict(dash='dot')))

    if failure_time:
        main_fig.add_trace(go.Scatter(x=[failure_time], y=[thresholds[failure_param][1]],
                                      mode='markers', name='Predicted Failure',
                                      marker=dict(color='red', size=12, symbol='x')))

    main_fig.update_layout(
        title='Parameters Over Time with Forecasts',
        xaxis_title='Time',
        yaxis_title='Value',
        paper_bgcolor=bg_color,
        plot_bgcolor=plot_bg_color,
        font={'color': text_color},
        legend_title_text='Parameters'
    )

    # Create summary card
    summary_card = dbc.Card([
        dbc.CardHeader("Latest Values"),
        dbc.CardBody([
            html.P(f"{param.replace('_', ' ').title()}: {new_data[param]:.2f} - Status: {determine_status(new_data[param], thresholds[param])}")
            for param in selected_params
        ] + ([html.P(f"Predicted Failure: {failure_time.strftime('%Y-%m-%d %H:%M:%S')} due to {failure_param}", style={'color': 'red', 'font-weight': 'bold'})] if failure_time else []))
    ])

    return main_fig, summary_card, update_interval * 1000, failure_time is not None

# Callback to pause/resume updates
@app.callback(
    Output('graph-update', 'disabled'),
    [Input('pause-button', 'n_clicks'),
     Input('failure-detected', 'data')],
    [State('graph-update', 'disabled')]
)
def toggle_interval(n_clicks, failure_detected, current_state):
    if failure_detected:
        return True
    if n_clicks:
        return not current_state
    return current_state

# Callback to download data
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
