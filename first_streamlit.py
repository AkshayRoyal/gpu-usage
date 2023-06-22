import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import datetime

st.set_page_config(layout="wide")
st.title('GPU Usage')



##########BASIC DATA PRE-PROCESSING##########
#wrap the below code in a function
def preprocess_data():
    df = pd.read_csv('gpu_usage.csv')
    df1 = df[::2]
    #rename the header columns by removing special characters and spaces
    df1.columns = ['timestamp', 'index_gpu','name', 'pci_bus_id','gpu_utilization', 
                   'gpu_memory_utilization', 'gpu_memory_used', 'gpu_memory_free', 
                   'gpu_memory_total']
    df1['timestamp'] = pd.to_datetime(df1['timestamp'], format='mixed')
    df1['timestamp'] = df1['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
    df1['gpu_utilization'] = df1['gpu_utilization'].str.replace('%', '').astype('int64')
    df1['gpu_memory_utilization'] = df1['gpu_memory_utilization'].str.replace('%', '').astype('int64')
    df1['gpu_memory_used'] = df1['gpu_memory_used'].str.replace('MiB', '').astype('int64')
    df1['gpu_memory_free'] = df1['gpu_memory_free'].str.replace('MiB', '').astype('int64')
    df1['gpu_memory_total'] = df1['gpu_memory_total'].str.replace('MiB', '').astype('int64')
    df1.to_csv('gpu_usage_cleaned.csv', index=False)
    return df1


df1=preprocess_data()

st.write('GPU data')
st.write(df1)

#create a sidebar to select different gpus
gpu_list = df1['index_gpu'].unique()
#convert each element in the list to string with prefix 'GPU'
gpu_list = ['GPU '+str(i) for i in gpu_list]
gpu_list = np.array(gpu_list,dtype='<U10')
gpu_list = np.insert(gpu_list, 0, 'All GPUs')
gpu_choice = st.sidebar.selectbox('Select GPU', gpu_list)

#create a multiselect sidebar to select different graphs
graph_list = ['GPU Memory Utilization', 'GPU Memory']
graph_choice = st.sidebar.multiselect('Select Graphs', graph_list,default=graph_list[-1])


#use the graph_choice to display the graphs

if 'GPU Memory Utilization' in graph_choice:
    #plot both the memory utilization and memory used
    fig = px.line(df1, x='timestamp', y=['gpu_memory_utilization', 'gpu_utilization'], title='GPU Memory Utilization')
    st.plotly_chart(fig,use_container_width=True)

if 'GPU Memory' in graph_choice:
    fig = px.line(df1, x='timestamp', y=['gpu_memory_used', 'gpu_memory_free'], title='GPU Memory')
    st.plotly_chart(fig,use_container_width=True)


