import streamlit as st
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import io

@st.cache_data
def load_data(file):
    data = pd.read_csv(file)
    return data

def save_and_download_plot():
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    st.sidebar.download_button("Скачать график", buf, "graph.png", "image/png")

uploaded_file = st.sidebar.file_uploader("Choose a file", type="csv")
if uploaded_file is not None:
    if uploaded_file.name == "tips.csv":
        tips = load_data(uploaded_file)
        page = st.sidebar.selectbox("Выберите страницу", [
            "DataFrame", "Динамика чаевых во времени", "Гистограмма total_bill", 
            "Scatterplot, показывающий связь между total_bill and tip", 
            "Scatterplot, показывающий связь между днем недели и размером счета", 
            "Scatter plot с днем недели по оси Y, чаевыми по оси X, и цветом по полу", 
            "Box plot c суммой всех счетов за каждый день, разбивая по time (Dinner/Lunch)",
            "Scatterplots (для мужчин и женщин), показывающие связи размера счета и чаевых, дополнительно разбив по курящим/некурящим",
            "Тепловая карта зависимостей численных переменных",
            "Влияние курения на отношение чаевых к общему счёту в зависимости от пола"
        ])
        
        np.random.seed(0)
        random_days = np.random.randint(1, 32, size=len(tips))
        tips["time_order"] = pd.to_datetime("2023-01-01") + pd.to_timedelta(random_days - 1, unit='d')

        if page == "DataFrame":
            st.title("Наш датафрейм для исследований")
            st.write(tips)

        elif page == "Динамика чаевых во времени":
            dfex4 = tips.groupby('time_order')['tip'].sum().reset_index()
            plt.figure(figsize=(10, 6))
            ax = sns.lineplot(x=dfex4["time_order"], y=dfex4["tip"], marker="o")
            ax.set_title('Tips over time')
            ax.set_xlabel('Time')
            ax.set_ylabel('Tips')
            ax.set_xticks(dfex4["time_order"].unique())
            ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
            st.pyplot(plt)
            save_and_download_plot()

        elif page == "Гистограмма total_bill":
            plt.figure(figsize=(10, 6))
            ax = sns.histplot(tips["total_bill"], bins=10, kde=True, color="red")
            ax.set_title("Histogram of Total Bill")
            st.pyplot(plt)
            save_and_download_plot()

        elif page == "Scatterplot, показывающий связь между total_bill and tip":
            fig = px.scatter(tips, x='total_bill', y='tip', color='sex', title="Scatterplot Total Bill/Tips")
            st.plotly_chart(fig)
            st.sidebar.write("Чтобы скачать график выберите зону и нажмите на 'камеру'")

        elif page == "Scatterplot, показывающий связь между днем недели и размером счета":
            plt.figure(figsize=(10, 6))
            ax = sns.scatterplot(x=tips['total_bill'], y=tips['tip'], data=tips, hue=tips['size'])
            ax.set_title("Scatterplot Total Bill/Tips/Size")
            st.pyplot(plt)
            save_and_download_plot()

        elif page == "Scatter plot с днем недели по оси Y, чаевыми по оси X, и цветом по полу":
            plt.figure(figsize=(10, 6))
            ax = sns.scatterplot(x=tips['tip'], y=tips['day'], hue=tips['sex'], data=tips)
            ax.set_title("Scatterplot Day/Tips/Sex")
            st.pyplot(plt)
            save_and_download_plot()

        elif page == "Box plot c суммой всех счетов за каждый день, разбивая по time (Dinner/Lunch)":
            plt.figure(figsize=(10, 6))
            ax = sns.boxplot(x='time', y='total_bill', hue='day', data=tips)
            ax.set_title("Boxplot Total Bill by Time and Day")
            st.pyplot(plt)
            save_and_download_plot()

        elif page == "Scatterplots (для мужчин и женщин), показывающие связи размера счета и чаевых, дополнительно разбив по курящим/некурящим":
            dfex12 = tips.copy()
            fig, ax = plt.subplots(1, 2, figsize=(14, 6))
            sns.scatterplot(x='total_bill', y='tip', data=dfex12[dfex12["sex"]=="Male"], hue='smoker', ax=ax[0], alpha=0.7)
            ax[0].set_title('Men: Total Bill vs Tips')
            ax[0].set_xlabel('Total Bill ($)')
            ax[0].set_ylabel('Tip ($)')
            sns.scatterplot(x='total_bill', y='tip', data=dfex12[dfex12["sex"]=="Female"], hue='smoker', ax=ax[1], alpha=0.7)
            ax[1].set_title('Women: Total Bill vs Tips')
            ax[1].set_xlabel('Total Bill ($)')
            ax[1].set_ylabel('Tip ($)')
            st.pyplot(plt)
            save_and_download_plot()

        elif page == "Тепловая карта зависимостей численных переменных":
            correlation_matrix = tips[["total_bill", "tip", "size"]].corr()
            plt.figure(figsize=(10, 6))
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
            plt.title('Correlation Heatmap of Numerical Variables')
            st.pyplot(plt)
            save_and_download_plot()

        elif page == "Влияние курения на отношение чаевых к общему счёту в зависимости от пола":
            dfexbon = tips.copy()
            dfexbon['t/tb'] = dfexbon['tip'] / dfexbon['total_bill']
            plt.figure(figsize=(10, 6))
            ax = sns.boxplot(x='smoker', y='t/tb', hue='sex', data=dfexbon)
            st.pyplot(plt)
            save_and_download_plot()

    else:
        st.error("Неверный файл")
