import streamlit as st
import pandas as pd
import plotly.express as px
from analysis import moving_average,StandardDeviation,Anomaly
from weatherapi import getinfo,checkfile
st.title("Информация о погоде")
uploaded_file = st.file_uploader("Загрузите файл с историческими данными",type=["csv"])
if uploaded_file is not None:
    df=pd.read_csv(uploaded_file)
    df["timestamp"]=pd.to_datetime(df["timestamp"])
    whichcity=st.selectbox("Выберите город",sorted(df["city"].unique()))
    datachoose=df[df["city"]==whichcity].copy()
    datachoose=moving_average(datachoose)
    datachoose=Anomaly(datachoose)
    statistics=StandardDeviation(df)
    st.subheader("Конкретные данные")
    st.write(datachoose["temperature"].describe())
    st.subheader("Графический показатель колебания температы")
    fig=px.line(datachoose,x="timestamp",y="temperature",title=f"Показатель в городе {whichcity}")
    anomalies=datachoose[datachoose["anomaly"]==1]
    fig.add_scatter(x=anomalies["timestamp"],y=anomalies["temperature"],mode="markers",name="Аномалии")
    st.plotly_chart(fig)
    st.subheader("Сезонные профили")
    st.write(statistics[statistics["city"]==whichcity])
    st.subheader("Текущая температура")
    api = st.text_input("Введдите api....", type="password")
    if api:
        temp=getinfo(whichcity,api)
        if isinstance(temp,dict) and temp.get("cod") in [400,401,402,403,404,405]:
            st.error(temp["message"])
        else:
            st.write(f"Текущая температура в {whichcity}:{temp} °C")
            month = pd.Timestamp.now().month
            if month in [1,2,12]:
                season="winter"
            elif month in [3,4,5]:
                season="spring"
            elif month in [6,7,8]:
                season="summer"
            elif month in [9,10,11]:
                season="autumnf"
        result = checkfile(whichcity, season, temp, statistics)
        st.write(result)




