import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set global seaborn theme
sns.set_style("whitegrid")

# Page Config
st.set_page_config(
    page_title="😴 Sleep Health Dashboard",
    layout="wide",
    page_icon="💤"
)

# Stylish title
st.markdown("<h1 style='text-align: center; color: #4B8BBE;'>💤 Sleep Health and Lifestyle Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("Sleep_health_and_lifestyle_dataset.csv")
    df.drop("Person ID", axis=1, inplace=True)
    df.dropna(inplace=True)

    # Create age groups
    bins = [0, 25, 35, 45, 55, 100]
    labels = ['18-25', '26-35', '36-45', '46-55', '56+']
    df['Age Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)

    return df

df = load_data()

# 🔍 Engineer-specific KPIs
engineer_df = df[df["Occupation"] == "Engineer"]

avg_stress = round(engineer_df["Stress Level"].mean(), 2)
avg_activity = round(engineer_df["Physical Activity Level"].mean(), 2)
avg_steps = round(engineer_df["Daily Steps"].mean(), 2)

st.markdown("## 🧑‍🔧 Engineer Insights")

kpi1, kpi2, kpi3 = st.columns(3)

kpi1.metric(label="😖 Avg Stress Level", value=avg_stress)
kpi2.metric(label="🏃 Avg Physical Activity Level", value=avg_activity)
kpi3.metric(label="🚶 Avg Daily Steps", value=f"{avg_steps:.0f} steps")

st.markdown("---")

# Sidebar
st.sidebar.header("🔍 Filter Data")
occupations = st.sidebar.multiselect("Select Occupations", df["Occupation"].unique(), default=df["Occupation"].unique())
bmi_categories = st.sidebar.multiselect("Select BMI Categories", df["BMI Category"].unique(), default=df["BMI Category"].unique())

# Filtered data
filtered_df = df[(df["Occupation"].isin(occupations)) & (df["BMI Category"].isin(bmi_categories))]

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Sleep Duration Analysis", "📉 Correlation Heatmap", "🧍 BMI Category Analysis"])

# 📊 Tab 1
with tab1:
    st.markdown("## 📊 Sleep Duration Insights")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🛏️ Sleep Duration by Occupation")
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        sns.barplot(data=filtered_df, x="Occupation", y="Sleep Duration", ci=None, palette="coolwarm", ax=ax1)
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig1)

    with col2:
        st.markdown("### 😖 Stress Level vs Sleep Duration")
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        sns.boxplot(data=filtered_df, x="Stress Level", y="Sleep Duration", palette="pastel", ax=ax2)
        plt.tight_layout()
        st.pyplot(fig2)

    st.markdown("---")

# 📉 Tab 2
with tab2:
    st.markdown("## 📉 Correlation Between Numerical Features")
    fig3, ax3 = plt.subplots(figsize=(10, 8))
    sns.heatmap(filtered_df.corr(numeric_only=True), annot=True, cmap="YlGnBu", linewidths=0.5, square=True)
    st.pyplot(fig3)

# 🧍 Tab 3
with tab3:
    st.markdown("## 🧍 BMI Category and Activity Insights")

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("### 🧓 BMI Category Count Across Age Groups")
        bmi_age = filtered_df.groupby(['Age Group', 'BMI Category']).size().unstack().fillna(0)
        fig4, ax4 = plt.subplots(figsize=(6, 4))
        bmi_age.plot(kind='bar', colormap='Set2', ax=ax4)
        plt.xticks(rotation=0)
        plt.tight_layout()
        st.pyplot(fig4)

    with col4:
        st.markdown("### 🚶 Daily Steps vs BMI Category")
        fig5, ax5 = plt.subplots(figsize=(6, 4))
        sns.boxplot(data=filtered_df, x="BMI Category", y="Daily Steps", palette="Set3", ax=ax5)
        plt.tight_layout()
        st.pyplot(fig5)

    st.markdown("---")
