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


matplotlib.font_manager.fontManager.addfont('Sarabun-Regular.ttf')
matplotlib.rc('font', family='Sarabun')

df = pd.read_csv("https://raw.githubusercontent.com/MySavEv/datavi/master/datasetEducation.csv")
new_columns = {
    "คุณยินยอมให้ใช้ข้อมูลส่วนตัวและข้อมูลด้านการศึกษาของคุณ เพื่อใช้ในการศึกษาและนำไปพัฒนา":"ความยินยอม",
    "สาขา ( กรอกด้วยชื่อเต็มของสาขา ,หากไม่มีกรอก ' - ')":"สาขา",
    "ชั้นปีที่":"ชั้นปี",
    "คุณเคยได้รับผลการเรียนที่ไม่พึงพอใจหรือไม่":"เคยได้รับผลการเรียนที่ไม่พึงพอใจ"
}

df.rename(columns=new_columns,inplace=True)
cols = list(df.columns)
kery = [10,45]
maikery = [45,79]

df_kery = df[df[df.columns[9]] == "เคย"];
df_kery.drop(columns=df.columns[maikery[0]:maikery[1]],inplace=True); # Drop คำถามส่วน ไม่เคยออก

df_maikery = df[df[df.columns[9]] == "ไม่เคย"];
df_maikery.drop(columns=df.columns[kery[0]:kery[1]],inplace=True); # Drop คำถามส่วน เคยออก

similar_names = {
    "วิทยาการคอมพิวเตอร์": ["สาขาวิชาวิทยาการคอมพิวเตอร์", "คอมพิวเตอร์", "วิทยาการ คอมพิวเตอร์", "วิทยากรคอมพิวเตอร์","COMSCI" , "สาขาวิทยาการคอมพิวเตอร์","วิทยการคอมพิวเตอร์","วิทยาการคอมพิวเคอร์ ภาคพิเศษ","คอม"],
    "การเมืองการปกครอง": ["บริหารรัฐกิจ","สาขาการเมืองการปกครอง","สาขาการเมืองการปกครอง "],
    "บัญชีบัณฑิต": ["บัญชี"],
    "วิชาการบัญชีธุรกิจแบบบูรณาการ": ["การบัญชีธุรกิจแบบบูรณาการ","สาขาวิชาการบัญชีธุรกิจแบบบูรณาการ","สาขาวิชาการบัญชีธุรกิจแบบบูรณาการ "],
    "อุตสาหกรรม": ["เทคโนโลยีพลังงานชีวภาพและการแปรรูปเคมีชีวภาพ","อุตสาหการ"],
    "สถิติ": ["สถิตอประยุกต์"],
    "การเงิน": ["Bachelor of economics","การเงิน "],
    "ผังเมือง": ["การผังเมือง"],
    "ภูมิศาสตร์และภูมิสารสนเทศ":["ภูมิศาสตร์"],
    "สื่อศึกษา":["สาขาวิชาสาขาวิชาสื่อศึกษา "],
    "วิทยาการเรียนรู้":["สาขาวิชาวิทยาการเรียนรู้"],
    "สิ่งแวดล้อม":["สาขาสิ่งแวดล้อม"],
    "ไม่ระบุ":["ข"],
    "คณิตศาสตร์":["คณิตภาคพิเศษ"],
    "เคมี":["วิศวกรรมเคมี"],
    "วิทยาศาสตร์การกีฬาและการออกกำลังกาย":["สาขาวิชาวิทยาศาสตร์การกีฬาและการออกกำลังกาย"],
    "เทคโนโลยีการอาหาร":["วิทยาศาสตร์และเทคโนโลยีการอาหาร","เทคโลยีการอาหาร"]
}

def replace_value(value):
    for i in similar_names:
        if value in similar_names[i]:
            return i
    return value

df["สาขา"] = df["สาขา"].map(replace_value)
df_kanasaka = df.groupby(['คณะ','สาขา']).size().reset_index(name="จำนวน")
df_sug1 = df.groupby(["คณะ","ผลการเรียนในรายวิชาที่พึงพอใจ"]).size().reset_index(name="จำนวน")
df_sug2 = df.groupby(["คณะ","ผลการเรียนในรายวิชาที่ไม่พึงพอใจ"]).size().reset_index(name="จำนวน")

def plot_kanasaka(kana):
    fig, ax = plt.subplots(figsize=(5, 5))
    
    df_buff = df_kanasaka[df_kanasaka['คณะ'] == kana]
    sizes = df_buff['จำนวน']
    labels = df_buff['สาขา']
    colors = ['cornflowerblue', 'skyblue', 'lightgreen', 'lightgray']
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)

    ax.set_title('สัดส่วนแต่ละสาขา ของคณะ {}'.format(kana))
    ax.legend()
    
    return fig

def kana_tor_grade(kana):
    # สร้าง figure และ axes
    fig, ax = plt.subplots(figsize=(5, 5))

    
    # สร้างกราฟ
    sns.barplot(ax=ax, y='คณะ', x='จำนวน', hue='ผลการเรียนในรายวิชาที่พึงพอใจ', data=df_sug1[df_sug1['คณะ'] == kana], palette='pastel')


    # กำหนดชื่อแกนและหัวข้อกราฟ
    ax.set_title('คณะ / ผลการเรียนที่พึงพอใจ')
    ax.set_xlabel('จำนวน')
    ax.set_ylabel('คณะ')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    return fig