
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_lottie import st_lottie
import json
from utils.recommender import recommend_charts

st.set_page_config(page_title="✨ AI-Powered Insights", layout="wide")
st.title("📊 AI-Powered Data Insights & Chart Recommender")

# Load Lottie animation
def load_lottie(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

lottie_chart = load_lottie("assets/chart_anim.json")
st_lottie(lottie_chart, speed=1, height=200)

uploaded_file = st.file_uploader("📁 Upload your CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    with st.expander("🔍 Data Preview", expanded=False):
        st.dataframe(df.head())

    with st.expander("📈 Statistical Summary", expanded=False):
        st.write(df.describe(include='all'))

    st.subheader("🧠 AI Chart Recommender")
    recs = recommend_charts(df)

    for rec in recs:
      with st.expander(f"📌 {rec['column']} → {rec['recommended_chart']}"):
        st.markdown(f"""
        **📊 Recommended Chart:** `{rec['recommended_chart']}`  
        🧠 *Reason:* {rec['reason']}
        """)
        fig = None

        if rec['recommended_chart'] == "Histogram":
            fig = px.histogram(df, x=rec['column'], title=rec['column'])

        elif rec['recommended_chart'] == "Bar Chart":
            data = df[rec['column']].value_counts().reset_index()
            data.columns = [rec['column'], 'count']
            fig = px.bar(data, x=rec['column'], y='count', title=rec['column'])

        elif rec['recommended_chart'] == "Line Chart":
            df_sorted = df.sort_values(by=rec['column'])
            fig = px.line(df_sorted, y=rec['column'], title=rec['column'])

        elif rec['recommended_chart'] == "Pie Chart":
            data = df[rec['column']].value_counts().reset_index()
            data.columns = [rec['column'], 'count']
            fig = px.pie(data, names=rec['column'], values='count', title=rec['column'])

        if fig:
            st.plotly_chart(fig, use_container_width=True)
