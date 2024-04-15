import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import matplotlib
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.font_manager as fm
import seaborn as sns
import numpy as np

import center as da

# App
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

st.subheader("ชั้นปีการศึกษา")
st.bar_chart(data=da.df['ชั้นปี'])

select = st.selectbox('คณะ',da.df['คณะ'].unique())

df_buff = da.df_kanasaka[da.df_kanasaka['คณะ'] == select]
fig = px.pie(df_buff, values='จำนวน', names='สาขา', 
                title=f'สัดส่วนแต่ละสาขา ของคณะ {select}')
st.plotly_chart(fig)


fig = px.bar(da.df_sug1[da.df_sug1['คณะ'] == select], 
             y='คณะ', x='จำนวน', 
             color='ผลการเรียนในรายวิชาที่พึงพอใจ', 
             title='คณะ / ผลการเรียนที่พึงพอใจ',
             orientation='h', 
             height=500)

fig.update_layout(xaxis_title='จำนวน', yaxis_title='คณะ', xaxis_tickangle=-45)
st.plotly_chart(fig)

fig = px.bar(da.df_sug2[da.df_sug2['คณะ'] == select], 
             y='คณะ', x='จำนวน', 
             color='ผลการเรียนในรายวิชาที่ไม่พึงพอใจ', 
             title='คณะ / ผลการเรียนในรายวิชาที่ไม่พึงพอใจ',
             orientation='h', 
             height=500)
fig.update_layout(xaxis_title='จำนวน', yaxis_title='คณะ', xaxis_tickangle=-45)
st.plotly_chart(fig)

print(123)