import streamlit as st
import pandas as pd
import plotly.express as px

F1DriversDataset = pd.read_csv('F1DriversDataset.csv')


def preprocess_data(df):
    df['Championship Years'] = df['Championship Years'].apply(lambda x: x.split(',') if pd.notna(x) else [])
    return df


F1DriversDataset = preprocess_data(F1DriversDataset)

st.title('F1 Drivers Dashboard')

st.sidebar.header('Filter Options')
selected_nationalities = st.sidebar.multiselect('Select Nationalities', F1DriversDataset['Nationality'].unique())
selected_drivers = st.sidebar.multiselect('Select Drivers', F1DriversDataset['Driver'].unique())

filtered_data = F1DriversDataset.copy()
if selected_nationalities:
    filtered_data = filtered_data[filtered_data['Nationality'].isin(selected_nationalities)]
if selected_drivers:
    filtered_data = filtered_data[filtered_data['Driver'].isin(selected_drivers)]

st.header('F1 Drivers Data')
st.dataframe(filtered_data)

st.header('Statistics')
st.write('Total Drivers:', len(filtered_data))
st.write('Total Championships:', filtered_data['Championships'].sum())
st.write('Total Race Wins:', filtered_data['Race_Wins'].sum())

st.header('Charts')

st.subheader('Championships by Nationality')
if not filtered_data.empty:
    fig = px.bar(filtered_data.groupby('Nationality')['Championships'].sum().reset_index(),
                 x='Nationality', y='Championships', title='Championships by Nationality')
    st.plotly_chart(fig)

st.subheader('Average Points Per Entry by Nationality')
if not filtered_data.empty:
    fig = px.bar(filtered_data.groupby('Nationality')['Points_Per_Entry'].mean().reset_index(),
                 x='Nationality', y='Points_Per_Entry', title='Average Points Per Entry by Nationality')
    st.plotly_chart(fig)

if selected_drivers:
    st.subheader('Comparisons Among Selected Drivers')

    fig = px.scatter(filtered_data, x='Pole_Rate', y='Win_Rate', text='Driver',
                     title='Win Rate vs. Pole Rate per Driver')
    fig.update_traces(textposition='top center')
    st.plotly_chart(fig)

    avg_points_per_entry_driver = filtered_data.groupby('Driver')['Points_Per_Entry'].mean().reset_index()
    fig = px.bar(avg_points_per_entry_driver, x='Driver', y='Points_Per_Entry',
                 title='Average Points Per Entry by Driver')
    st.plotly_chart(fig)

    win_rate_driver = filtered_data.groupby('Driver')['Win_Rate'].mean().reset_index()
    fig = px.bar(win_rate_driver, x='Driver', y='Win_Rate', title='Win Rate by Driver')
    st.plotly_chart(fig)

    podium_rate_driver = filtered_data.groupby('Driver')['Podium_Rate'].mean().reset_index()
    fig = px.bar(podium_rate_driver, x='Driver', y='Podium_Rate', title='Podium Rate by Driver')
    st.plotly_chart(fig)

st.subheader('Race Wins by Driver')
if not filtered_data.empty:
    st.bar_chart(filtered_data.groupby('Driver')['Race_Wins'].sum())

st.subheader('Pole Positions by Driver')
if not filtered_data.empty:
    st.bar_chart(filtered_data.groupby('Driver')['Pole_Positions'].sum())

st.header('Filtered Data')
st.dataframe(filtered_data)
