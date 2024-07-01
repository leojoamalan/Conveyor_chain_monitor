import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import random
import datetime
import time

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

# Sample initial data
data = pd.DataFrame([generate_sample_data() for _ in range(10)])

# Streamlit app
st.set_page_config(page_title="Machine Monitoring Dashboard", layout="wide")
st.title("Machine Monitoring Dashboard")

# Layout for stats cards
cols = st.columns(4)
stats = [
    {"id": "strain", "title": "Strain (μstrain)"},
    {"id": "load", "title": "Load (kg)"},
    {"id": "chain_position", "title": "Chain Position (mm)"},
    {"id": "vibration", "title": "Vibration (g)"},
    {"id": "temperature", "title": "Temperature (°C)"},
    {"id": "chain_wear", "title": "Chain Wear (%)"},
    {"id": "torque", "title": "Torque (Nm)"},
    {"id": "lubrication_level", "title": "Lubrication Level (%)"},
    {"id": "patch_length", "title": "Patch Length (mm)"}
]

# Function to display a stat card
def display_stat_card(col, stat, value, percentage):
    col.metric(stat["title"], f"{value:.2f}", f"{percentage:.2f}%")
    col.image(stat["icon"], width=50)

# Function to generate traces for plotting
def generate_trace(data, y, name):
    return go.Scatter(x=data['time'], y=data[y], mode='lines+markers', name=name)

# Function to plot graphs
def plot_graph(data, y, title):
    trace = generate_trace(data, y, title)
    layout = go.Layout(title=title)
    fig = go.Figure(data=[trace], layout=layout)
    st.plotly_chart(fig, use_container_width=True)

while True:
    new_data = generate_sample_data()
    data.loc[len(data)] = new_data
    if len(data) > 100:
        data.drop(data.index[0], inplace=True)  # Keep data within a limit

    strain_percentage = ((new_data['strain'] - data.iloc[-2]['strain']) / data.iloc[-2]['strain']) * 100 if len(data) > 1 else 0
    load_percentage = ((new_data['load'] - data.iloc[-2]['load']) / data.iloc[-2]['load']) * 100 if len(data) > 1 else 0
    chain_position_percentage = ((new_data['chain_position'] - data.iloc[-2]['chain_position']) / data.iloc[-2]['chain_position']) * 100 if len(data) > 1 else 0
    vibration_percentage = ((new_data['vibration'] - data.iloc[-2]['vibration']) / data.iloc[-2]['vibration']) * 100 if len(data) > 1 else 0
    temperature_percentage = ((new_data['temperature'] - data.iloc[-2]['temperature']) / data.iloc[-2]['temperature']) * 100 if len(data) > 1 else 0
    chain_wear_percentage = ((new_data['chain_wear'] - data.iloc[-2]['chain_wear']) / data.iloc[-2]['chain_wear']) * 100 if len(data) > 1 else 0
    torque_percentage = ((new_data['torque'] - data.iloc[-2]['torque']) / data.iloc[-2]['torque']) * 100 if len(data) > 1 else 0
    lubrication_level_percentage = ((new_data['lubrication_level'] - data.iloc[-2]['lubrication_level']) / data.iloc[-2]['lubrication_level']) * 100 if len(data) > 1 else 0
    patch_length_percentage = ((new_data['patch_length'] - data.iloc[-2]['patch_length']) / data.iloc[-2]['patch_length']) * 100 if len(data) > 1 else 0

    with st.container():
        cols = st.columns(4)
        for i, stat in enumerate(stats[:4]):
            display_stat_card(cols[i], stat, new_data[stat["id"]], eval(f"{stat['id']}_percentage"))

        plot_graph(data, 'strain', 'Strain (μstrain)')
        plot_graph(data, 'load', 'Load (kg)')

        cols = st.columns(4)
        for i, stat in enumerate(stats[4:8]):
            display_stat_card(cols[i], stat, new_data[stat["id"]], eval(f"{stat['id']}_percentage"))

        plot_graph(data, 'chain_position', 'Chain Position (mm)')
        plot_graph(data, 'vibration', 'Vibration (g)')

        cols = st.columns(4)
        display_stat_card(cols[0], stats[8], new_data[stats[8]["id"]], patch_length_percentage)

        plot_graph(data, 'temperature', 'Temperature (°C)')
        plot_graph(data, 'chain_wear', 'Chain Wear (%)')
        plot_graph(data, 'torque', 'Torque (Nm)')
        plot_graph(data, 'lubrication_level', 'Lubrication Level (%)')
        plot_graph(data, 'patch_length', 'Patch Length (mm)')

    time.sleep(5)  # Update every 5 seconds
