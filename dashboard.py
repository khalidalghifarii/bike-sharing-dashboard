import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

# Function to load data
@st.cache_data
def load_data():
    day_df = pd.read_csv('day.csv')
    hour_df = pd.read_csv('hour.csv')
    
    # Convert dteday to datetime
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    
    # Normalize weather variables
    day_df['temp'] = day_df['temp'] * 41  # suhu dalam Celsius
    day_df['atemp'] = day_df['atemp'] * 50  # suhu terasa dalam Celsius
    day_df['hum'] = day_df['hum'] * 100  # kelembaban dalam persen
    day_df['windspeed'] = day_df['windspeed'] * 67  # kecepatan angin dalam km/h

    hour_df['temp'] = hour_df['temp'] * 41
    hour_df['atemp'] = hour_df['atemp'] * 50
    hour_df['hum'] = hour_df['hum'] * 100
    hour_df['windspeed'] = hour_df['windspeed'] * 67
    
    return day_df, hour_df

# Load data
day_df, hour_df = load_data()

# Header
st.title("🚲 Bike Sharing Dashboard")
st.markdown("**Nama:** Muhammad Khalid Al Ghifari | **Email:** alghi.bna@gmail.com | **ID Dicoding:** MC322D5Y2203")

st.markdown("---")

# Sidebar
st.sidebar.title("Bike Sharing Analysis")
st.sidebar.markdown("Dashboard ini menunjukkan analisis tentang penyewaan sepeda berdasarkan beberapa faktor.")

analysis_options = st.sidebar.radio(
    "Pilih Analisis:",
    ["Pengaruh Kondisi Cuaca", "Pola Penggunaan Berdasarkan Waktu", "Analisis Lanjutan"]
)

# Main content
if analysis_options == "Pengaruh Kondisi Cuaca":
    st.header("Pengaruh Kondisi Cuaca terhadap Jumlah Penyewaan Sepeda")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribusi Penyewaan Berdasarkan Kondisi Cuaca")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(data=day_df, x='weathersit', y='cnt', hue='workingday', palette='coolwarm', ax=ax)
        ax.set_xlabel("Kondisi Cuaca (1: Cerah, 2: Berawan, 3: Hujan)")
        ax.set_ylabel("Jumlah Penyewaan")
        st.pyplot(fig)
        
        st.markdown("""
        **Insight:**
        - Jumlah penyewaan lebih tinggi pada Cuaca yang baik (kondisi 1 & 2) dibandingkan dengan kondisi hujan (kondisi 3)
        - Perbedaan hari kerja vs akhir pekan tidak signifikan dalam distribusi penyewaan
        """)
    
    with col2:
        st.subheader("Korelasi antara Faktor Cuaca dan Jumlah Penyewaan")
        fig, ax = plt.subplots(figsize=(8, 6))
        corr_matrix = day_df[['cnt', 'temp', 'hum', 'windspeed']].corr()
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
        st.pyplot(fig)
        
        st.markdown("""
        **Insight:**
        - Temperatur memiliki korelasi positif (0.63) dengan jumlah penyewaan
        - Kelembapan dan kecepatan angin memiliki korelasi negatif dengan jumlah penyewaan
        """)
    
    # Additional analysis for Weather Impact
    st.subheader("Scatter Plot: Hubungan Temperatur dengan Penyewaan Sepeda")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=day_df, x='temp', y='cnt', hue='weathersit', palette='viridis', size='windspeed', sizes=(20, 200), ax=ax)
    ax.set_xlabel("Temperatur (°C)")
    ax.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig)
    
    # Interactive filter for weather analysis
    st.subheader("Analisis Interaktif: Pengaruh Rentang Temperatur")
    temp_range = st.slider(
        "Pilih Rentang Temperatur (°C)",
        float(day_df['temp'].min()),
        float(day_df['temp'].max()),
        (float(day_df['temp'].min()), float(day_df['temp'].max()))
    )
    
    filtered_df = day_df[(day_df['temp'] >= temp_range[0]) & (day_df['temp'] <= temp_range[1])]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=filtered_df, x='weathersit', y='cnt', hue='workingday', palette='coolwarm', ax=ax)
    ax.set_xlabel("Kondisi Cuaca")
    ax.set_ylabel("Rata-rata Jumlah Penyewaan")
    st.pyplot(fig)

elif analysis_options == "Pola Penggunaan Berdasarkan Waktu":
    st.header("Pola Penggunaan Sepeda Berdasarkan Waktu")
    
    tab1, tab2 = st.tabs(["Berdasarkan Jam", "Berdasarkan Musim"])
    
    with tab1:
        st.subheader("Pola Penggunaan Sepeda Berdasarkan Jam")
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(data=hour_df, x='hr', y='cnt', hue='workingday', palette='coolwarm', ax=ax)
        ax.set_xlabel("Jam")
        ax.set_ylabel("Jumlah Penyewaan Sepeda")
        ax.set_xticks(range(0, 24, 1))
        st.pyplot(fig)
        
        st.markdown("""
        **Insight:**
        - Hari kerja: Dua puncak aktivitas di pagi (08:00) dan sore (17:00)
        - Akhir pekan: Penggunaan lebih merata dengan puncak di siang hingga sore hari
        """)
        
        # Interactive time selection
        st.subheader("Analisis Jam Sibuk")
        hour_selection = st.multiselect(
            "Pilih jam untuk analisis:",
            options=list(range(0, 24)),
            default=[8, 17]
        )
        
        if hour_selection:
            peak_hours_df = hour_df[hour_df['hr'].isin(hour_selection)]
            
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.boxplot(data=peak_hours_df, x='hr', y='cnt', hue='workingday', palette='coolwarm', ax=ax)
            ax.set_xlabel("Jam")
            ax.set_ylabel("Jumlah Penyewaan")
            st.pyplot(fig)
    
    with tab2:
        st.subheader("Pola Penggunaan Sepeda Berdasarkan Musim")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig, ax = plt.subplots(figsize=(10, 6))
            season_avg = day_df.groupby('season')['cnt'].mean().reset_index()
            sns.barplot(data=season_avg, x='season', y='cnt', palette='viridis', ax=ax)
            ax.set_xlabel("Musim (1: Semi, 2: Panas, 3: Gugur, 4: Dingin)")
            ax.set_ylabel("Rata-rata Penyewaan")
            st.pyplot(fig)
        
        with col2:
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.boxplot(data=day_df, x='season', y='cnt', palette='viridis', ax=ax)
            ax.set_xlabel("Musim (1: Semi, 2: Panas, 3: Gugur, 4: Dingin)")
            ax.set_ylabel("Jumlah Penyewaan")
            st.pyplot(fig)
        
        st.markdown("""
        **Insight:**
        - Penyewaan tertinggi terjadi pada musim gugur (3)
        - Diikuti oleh musim panas (2) dan musim dingin (4)
        - Musim semi (1) memiliki jumlah penyewaan terendah
        """)
        
        # Season and weather correlation
        st.subheader("Hubungan antara Musim, Cuaca, dan Jumlah Penyewaan")
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.boxplot(data=day_df, x='season', y='cnt', hue='weathersit', palette='viridis', ax=ax)
        ax.set_xlabel("Musim")
        ax.set_ylabel("Jumlah Penyewaan")
        st.pyplot(fig)

else:  # Analisis Lanjutan
    st.header("Analisis Lanjutan: Kategorisasi Penggunaan Sepeda")
    
    # Define bins for categorization
    bins = [day_df["cnt"].min(), 1000, 3000, day_df["cnt"].max()]
    labels = ["Low Usage", "Moderate Usage", "High Usage"]
    
    # Categorize bike rentals based on binning
    day_df["usage_category"] = pd.cut(day_df["cnt"], bins=bins, labels=labels, include_lowest=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribusi Kategori Penggunaan Sepeda")
        fig, ax = plt.subplots(figsize=(8, 6))
        day_df["usage_category"].value_counts().plot(kind="bar", color=["green", "orange", "red"], ax=ax)
        ax.set_xlabel("Kategori Penggunaan")
        ax.set_ylabel("Jumlah Hari")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
        st.pyplot(fig)
    
    with col2:
        st.subheader("Persentase Kategori Penggunaan")
        fig, ax = plt.subplots(figsize=(8, 6))
        day_df["usage_category"].value_counts(normalize=True).plot(kind="pie", autopct='%1.1f%%', ax=ax)
        st.pyplot(fig)
    
    st.markdown("""
    ## Analisis Kategori Penggunaan Sepeda dengan Binning
    
    **Pengelompokan jumlah penyewaan sepeda (cnt) ke dalam tiga kategori:**
    - **Low Usage** (< 1000 penyewaan/hari)
    - **Moderate Usage** (1000-3000 penyewaan/hari)
    - **High Usage** (> 3000 penyewaan/hari)
    
    **Insight:**
    - **High Usage** mendominasi, menunjukkan penggunaan sepeda yang tinggi secara konsisten
    - **Moderate Usage** lebih sedikit, mengindikasikan hari-hari transisi
    - **Low Usage** sangat jarang, kemungkinan terjadi pada hari-hari dengan cuaca buruk atau libur besar
    """)
    
    # Additional analysis - Usage category by season and weather
    st.subheader("Distribusi Kategori Penggunaan Berdasarkan Musim")
    season_usage = pd.crosstab(day_df['season'], day_df['usage_category'], normalize='index') * 100
    
    fig, ax = plt.subplots(figsize=(10, 6))
    season_usage.plot(kind='bar', stacked=True, colormap='viridis', ax=ax)
    ax.set_xlabel("Musim (1: Semi, 2: Panas, 3: Gugur, 4: Dingin)")
    ax.set_ylabel("Persentase (%)")
    ax.legend(title="Kategori Penggunaan")
    st.pyplot(fig)
    
    st.subheader("Distribusi Kategori Penggunaan Berdasarkan Cuaca")
    weather_usage = pd.crosstab(day_df['weathersit'], day_df['usage_category'], normalize='index') * 100
    
    fig, ax = plt.subplots(figsize=(10, 6))
    weather_usage.plot(kind='bar', stacked=True, colormap='viridis', ax=ax)
    ax.set_xlabel("Kondisi Cuaca (1: Cerah, 2: Berawan, 3: Hujan)")
    ax.set_ylabel("Persentase (%)")
    ax.legend(title="Kategori Penggunaan")
    st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("### Kesimpulan")

st.markdown("""
### Pertanyaan 1: Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda  
Kondisi cuaca berpengaruh signifikan terhadap jumlah penyewaan sepeda, di mana cuaca yang lebih baik (kondisi 1 & 2) meningkatkan jumlah penyewaan dibandingkan cuaca buruk (kondisi 3). Tidak terdapat perbedaan signifikan antara pola penyewaan pada hari kerja dan akhir pekan. Temperatur memiliki korelasi positif yang cukup kuat dengan penyewaan sepeda, menunjukkan bahwa semakin hangat suhu, semakin tinggi jumlah penyewaan. Sebaliknya, kelembapan dan kecepatan angin memiliki korelasi negatif, yang berarti kondisi lebih lembap atau angin kencang cenderung mengurangi jumlah penyewaan sepeda.  

### Pertanyaan 2: Pola Penggunaan Sepeda Berdasarkan Musim dan Jam Sibuk  
Pola penggunaan sepeda berbeda antara hari kerja dan akhir pekan, di mana hari kerja menunjukkan dua puncak pada jam sibuk (08:00 dan 17:00), sementara akhir pekan memiliki pola penggunaan yang lebih merata dengan puncak pada siang hingga sore hari. Dari segi musim, penyewaan tertinggi terjadi pada musim gugur, diikuti musim panas dan musim dingin, sementara musim semi memiliki jumlah penyewaan terendah, kemungkinan karena kondisi cuaca yang kurang mendukung.
""")

st.markdown("_Copyright © 2025 Muhammad Khalid Al Ghifari - Dicoding Project_")