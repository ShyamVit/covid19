import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from matplotlib import pyplot
import datetime
import plotly.graph_objects as go
#server = app.server
DATA_URL = ("https://api.covid19india.org/csv/latest/case_time_series.csv")
DATA_URL_statewise_timeseries = ("https://api.covid19india.org/csv/latest/state_wise_daily.csv")
DATA_URL_statewise = ("https://api.covid19india.org/csv/latest/state_wise.csv")

st.title("Covid-19 in India")

statewiseData=st.sidebar.checkbox(
        "Statewise Data "
)
if statewiseData:
    st.markdown("Statewise Covid-19 cases in India ")
    series1=pd.read_csv(DATA_URL_statewise, header=0, index_col=0, parse_dates=True, squeeze=True)
    series1=series1[["Confirmed","Recovered","Deaths","Active"]]
    st.subheader("Statewise Data")
    selectedState = st.selectbox(
    "Select a state :",
        sorted(series1.index))
    series2=series1.loc[[selectedState]]
    "Data for", selectedState
    series2
    stateDict={"Andhra Pradesh":"AP","Arunachal Pradesh":"AR","Assam":"AS","Bihar":"BR","Chhattisgarh":"CG",
                "Goa":"GA","Gujarat":"GJ","Haryana":"HR","Himachal Pradesh":"HP","Jammu and Kashmir":"JK","Jharkhand":"JH","Karnataka":"KA",
                "Kerala":"KL","Madhya Pradesh":"MP","Maharashtra":"MH","Manipur":"MN","Meghalaya":"ML","Mizoram":"MZ",
                "Nagaland":"NL","Orissa":"OR","Punjab":"PB","Rajasthan":"RJ","Sikkim":"SK","Tamil Nadu":"TN","Tripura":"TR",
                "Uttarakhand":"UK","Uttar Pradesh":"UP","West Bengal":"WB","Tamil Nadu":"TN","Tripura":"TR","Andaman and Nicobar Islands":"AN",
                "Chandigarh":"CH","Dadra and Nagar Haveli":"DH","Daman and Diu":"DD","Delhi":"DL","Lakshadweep":"LD","Pondicherry":"PY"}
    series_statewise_daily = pd.read_csv(DATA_URL_statewise_timeseries, header=0, index_col=0)
    stateForTimeSeries=stateDict[selectedState]
    timeSeriesDataforLast30DaysConfirmed = series_statewise_daily[stateForTimeSeries][-90::3]
    timeSeriesDataforLast30DaysRecovered = series_statewise_daily[stateForTimeSeries][-89::3]
    timeSeriesDataforLast30DaysDeceased = series_statewise_daily[stateForTimeSeries][-88::3]
    listOfVariables=["Daily Confirmed","Daily Recovered","Daily Deceased"]
    option = st.selectbox(
        'Select a category:',
        listOfVariables)
    if option=="Daily Confirmed":
        figD=px.line(timeSeriesDataforLast30DaysConfirmed,title="Daily confirmed cases in {s}".format(s=selectedState),labels={stateForTimeSeries:selectedState})
    elif option=="Daily Recovered":
        figD=px.line(timeSeriesDataforLast30DaysRecovered,title="Daily recovered cases in {s}".format(s=selectedState))
    elif option=="Daily Deceased":
        figD=px.line(timeSeriesDataforLast30DaysDeceased,title="Daily deceased cases in {s}".format(s=selectedState))
    figD.update_yaxes(title_text='No. of Cases')
    figD.update_layout(legend_title_text = "State")
    st.write(figD)
    st.subheader("Data for all States and Union Territories")
    fig = go.Figure(data=[go.Table(header=dict(values=["States","Confirmed","Recovered","Deaths","Active"]),
                 cells=dict(values=[series1.index,series1.Confirmed,series1.Recovered,series1.Deaths,series1.Active],
               fill_color='lavender',align='center'))
                     ])
    fig.update_layout(width=800, height=700)
    st.write(fig)
else:
    series = pd.read_csv(DATA_URL, header=0, index_col=0, parse_dates=True, squeeze=True)
    daily_confirmed = series["Daily Confirmed"]
    daily_recovered = series["Daily Recovered"]
    total_confirmed = series["Total Confirmed"]
    total_recovered = series["Total Recovered"]
    daily_deceased = series["Daily Deceased"]
    total_deceased = series["Total Deceased"]
    listOfVariables=["Daily Confirmed","Daily Recovered","Daily Deceased","Total Confirmed","Total Recovered","Total Deceased"]
    option = st.selectbox(
        'Select a category:',
        listOfVariables)
    option1=st.checkbox(
        "Select starting date")
    if option1:
        dateStart = st.date_input('start date', datetime.date(2020,5,30))
    else:
        dateStart= datetime.date(2020,5,30)
    'Showing graph for : ', option
    option, "Cases in India since ",dateStart
    startDate1=datetime.date(2020,1,30)
    delta = dateStart-startDate1
    linedata =series[option][delta.days:]
    fig = px.line(linedata)
    fig.update_xaxes(title_text='Date')
    fig.update_layout(hovermode="x")
    fig.update_layout(legend_title_text = "Parameter")
    fig.update_yaxes(title_text='No. of Cases')
    st.write(fig)

    total_active_today = series["Total Confirmed"][-1] - series["Total Recovered"][-1] - series["Total Deceased"][-1]
    pie = [total_active_today,series["Total Recovered"][-1],series["Total Deceased"][-1]]
    name=["Total Active Cases","Total Recovered Cases","Total Deaths"]
    colors=["lightcyan","cyan","royalblue"]
    fig1 = px.pie(pie, values=pie,names=name,
                title='Distribution of total cases in India')

    st.write(fig1)
