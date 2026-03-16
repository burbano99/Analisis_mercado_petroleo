
import pandas as pd
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt


df = pd.read_csv("oil_geopolitics_dataset_2010_2026.csv")
print(df.columns)

df["date"] = pd.to_datetime(df["date"])
df= df.sort_values("date")

#sidebar
min_date = df["date"].min()
max_date = df["date"].max()

date_range = st.sidebar.date_input("Seleccionar fechas", [min_date, max_date], 
                                   min_value = min_date, max_value = max_date)

if len(date_range) == 2:
   df= df[(df["date"]>= pd.to_datetime(date_range[0])) & (df["date"] <= pd.to_datetime(date_range[1]))]
   
#columnas

st.subheader("Indicadores")
col1, col2, col3 = st.columns(3)
col1.metric("Precio Brent promedio", round(df["brent_price"].mean(), 2))
col2.metric("Precio WTI promedio", round(df["wti_price"].mean(),2))
col3.metric("Spread promedio", round(df["brent_wti_spread"].mean(),2))
#evolucion precio

df_price= df.rename(columns= {"brent_price": "Brent", "wti_price": "WTI"})
fig_price = px.line(df_price, x= "date", y= ["Brent", "WTI"], labels= {"value": "precio", "variable": "tipo de petroleo"})
fig_price.update_traces(line= dict (width= 2))
fig_price.data[0].line.color = "#1f77b4"
fig_price.data[1].line.color = "#d62728"
st.plotly_chart(fig_price)

#spread

st.subheader("Spread Brent WTI")
fig_spread= px.line(df, x= "date", y= "brent_wti_spread", labels= {"date": "fecha", "brent_wti_spread": "Brent WTI Spread"})

st.plotly_chart(fig_spread)

#correlación 
st.subheader("Correlación entre Brent y WTI")
corr = df[["brent_price", "wti_price"]].corr().iloc[0,1]
st.metric("Correlación", round(corr,3))


#Volatilidad
st.subheader("Volatilidad del mercado")
df_vol = df.rename(columns={"brent_volatility_30d": "Brent volatilidad 30 días", "wti_volatility_30d": "WTI volatilidad 30 días"})
fig_vol = px.line( df_vol, x= "date", y= ["Brent volatilidad 30 días", "WTI volatilidad 30 días"])
fig_vol.update_traces(line= dict (width= 2))
fig_vol.data[0].line.color = "#1f77b4"
fig_vol.data[1].line.color = "#d62728"
st.plotly_chart(fig_vol)

#eventos geopolíticos 
st.subheader("Eventos políticos")
eventos = df[df["event_flag"]== 1]
st.dataframe(eventos[["date", "event_type", "event_severity", "event_description"]])
