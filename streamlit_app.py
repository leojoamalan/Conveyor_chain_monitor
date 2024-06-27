import streamlit as st
import pandas as pd
import numpy as np
import time
from playsound import playsound

def play_alert_sound():
    playsound('alert.mp3')

def get_sensor_data():
    return {
        'Strain (μstrain)': np.random.normal(100, 10),
        'Load (kg)': np.random.normal(200, 20),
        'Chain Position (mm)': np.random.normal(10, 1),
        'Vibration (g)': np.random.normal(5, 0.5),
        'Temperature (°C)': np.random.normal(30, 2),
        'Chain Wear (%)': np.random.normal(3, 0.3),
        'Torque (Nm)': np.random.normal(50, 5),
        'Lubrication Level (%)': np.random.normal(70, 7),
        'Patch Length (mm)': np.random.normal(15, 1.5)
    }

LIMITS = {
    'Strain (μstrain)': 150,
    'Load (kg)': 250,
    'Chain Position (mm)': 12,
    'Vibration (g)': 7,
    'Temperature (°C)': 40,
    'Chain Wear (%)': 5,
    'Torque (Nm)': 60,
    'Lubrication Level (%)': 50,
    'Patch Length (mm)': 20
}

def check_limits(data):
    alerts = []
    for key, value in data.items():
        if value > LIMITS[key]:
            alerts.append(f"{key} exceeds limit: {value:.2f} > {LIMITS[key]}")
    return alerts

if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=['time'] + list(LIMITS.keys()))

st.title('Conveyor Chain Monitoring System')

alert_placeholder = st.empty()

for _ in range(100):
    sensor_data = get_sensor_data()
    sensor_data['time'] = pd.Timestamp.now()
    
    new_data = pd.DataFrame(sensor_data, index=[0])
    st.session_state.data = pd.concat([st.session_state.data, new_data], ignore_index=True)
    
    st.subheader('Current Sensor Data')
    st.write(new_data)

    alerts = check_limits(sensor_data)
    if alerts:
        alert_message = '\n'.join(alerts)
        alert_placeholder.error(alert_message)
        play_alert_sound()
    else:
        alert_placeholder.empty()
    
    st.subheader('Sensor Data Trends')
    st.line_chart(st.session_state.data.set_index('time'))
    
    time.sleep(5)
