import streamlit as st
import plotly.graph_objects as go
import json
import numpy as np
import os
from datetime import datetime

st.set_page_config(layout="wide")

DATA_PATH = "filtered_ts_data.json"  # your time series data
LABELS_PATH = "labels.json"

# Load the data
if "data" not in st.session_state:
    with open(DATA_PATH, "r") as f:
        st.session_state.data = json.load(f)

data = st.session_state.data

if 'labels' not in st.session_state:
    if os.path.exists(LABELS_PATH):
        with open(LABELS_PATH, "r") as f:
            st.session_state.labels = json.load(f)
    else:
        st.session_state.labels = {}


untagged_pids = [pid for pid in st.session_state.labels if (st.session_state.labels[pid]['m1'] == "") or (st.session_state.labels[pid]['m2'] == "")]



if len(untagged_pids)==0:
    st.success("All plots are tagged!")
else:
    pid = untagged_pids[0]
    ts_data = data[pid]
    timestamps = ts_data["timestamp"][-360:]

    # formatted_dates = []

    # for date_str in timestamps:
        
    #     if date_str.endswith('Z'):
    #         date_str = date_str.replace('Z', '+00:00')
    #     try:
            
    #         dt = datetime.fromisoformat(date_str)
            
    #         formatted_date = dt.strftime("%B %d, %Y")
    #         formatted_dates.append(formatted_date)
    #     except ValueError as e:
    #         print(f"Error parsing date string '{date_str}': {e}")

    m1 = np.array(ts_data["m1"][-360:], dtype=np.float32)
    m2 = np.array(ts_data["m2"][-360:], dtype=np.float32)

    # Plot the time series
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=timestamps, y=m1, mode='lines', name='m1'))
    fig.add_trace(go.Scatter(x=timestamps, y=m2, mode='lines', name='m2'))
    fig.update_layout(title=f'Time Series for Plot ID: {pid}',
                      xaxis_title='Timestamp',
                      yaxis_title='Sensor Readings',
                      yaxis=dict(range=[30, 105]),
                    #   xaxis=dict(
                    #                 tickmode='array',
                    #                 tickvals=list(range(0,len(timestamps))),  # Positions of the ticks
                    #                 ticktext=formatted_dates,  
                    #                 tickangle=90  
                    #             ),
                      width=900, height=500)
    # fig.update_xaxes(tickangle=0)
    st.plotly_chart(fig)

    
    tag1 = st.selectbox(f"{len(untagged_pids)} Remaining, {len(st.session_state.labels)-len(untagged_pids)} done.\n\nSelect a tag for m1:",
                       ["", "air gap", "water inside", "correct", "slow drop", 'not-tagged'])
    tag2 = st.selectbox(f"Select a tag for m2:",
                       ["", "air gap", "water inside", "correct", "slow drop", 'not-tagged'])

    
    if st.button("Next"):
        st.session_state.labels[pid]['m1'] = tag1
        st.session_state.labels[pid]['m2'] = tag2
        with open(LABELS_PATH, "w") as f:
            json.dump(st.session_state.labels, f, indent=2)
        
        st.rerun()
