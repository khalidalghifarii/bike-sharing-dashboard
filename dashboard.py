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
    
    # Remove instant column as it's not useful
    day_df.drop(columns=['instant'], inplace=True, errors='ignore')
    hour_df.drop(columns=['instant'], inplace=True, errors='ignore')
    
    return day_df, hour_df

# Load data
day_df, hour_df = load_data()

# Extract month from datetime for monthly analysis
day_df['month'] = day_df['dteday'].dt.month

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
        
        # Updated visualization: bar chart with better labels
        weather_working_grouped = day_df.groupby(['weathersit', 'workingday'])['cnt'].mean().reset_index()
        sns.barplot(data=weather_working_grouped, x='weathersit', y='cnt', hue='workingday', palette='coolwarm', ax=ax)
        
        # Add better labels
        weather_labels = {1: 'Cerah', 2: 'Berawan', 3: 'Hujan Ringan', 4: 'Hujan Lebat'}
        working_labels = {0: 'Akhir Pekan', 1: 'Hari Kerja'}
        
        ax.set_xlabel("Kondisi Cuaca", fontsize=12)
        ax.set_ylabel("Rata-rata Jumlah Penyewaan", fontsize=12)
        
        # Update x-tick labels
        current_labels = ax.get_xticklabels()
        ax.set_xticklabels([weather_labels.get(float(label.get_text()), label.get_text()) for label in current_labels])
        
        # Update legend
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, [working_labels.get(int(float(label)), label) for label in labels], title="Jenis Hari", fontsize=10)
        
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        st.pyplot(fig)
        
        st.markdown("""
        **Insight:**
        - Jumlah penyewaan lebih tinggi pada cuaca yang baik (kondisi 1 & 2) dibandingkan dengan kondisi hujan (kondisi 3)
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
    
    # Additional visualization: pie chart for weather conditions
    st.subheader("Distribusi Total Penyewaan Berdasarkan Kondisi Cuaca")
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Calculate total rentals by weather condition
    weather_totals = day_df.groupby('weathersit')['cnt'].sum()
    
    # Create descriptive labels for pie chart
    weather_labels = {1: 'Cerah', 2: 'Berawan', 3: 'Hujan Ringan', 4: 'Hujan Lebat'}
    pie_labels = [weather_labels.get(i, f'Kondisi {i}') for i in weather_totals.index]
    
    # Create pie chart
    plt.pie(weather_totals, labels=pie_labels, autopct='%1.1f%%', startangle=90, shadow=True, 
            colors=['#66b3ff','#99ff99','#ffcc99','#ff9999'])
    plt.axis('equal')  # Ensure pie chart is circular
    plt.title('Distribusi Total Penyewaan Sepeda berdasarkan Kondisi Cuaca', fontsize=14)
    
    st.pyplot(fig)

elif analysis_options == "Pola Penggunaan Berdasarkan Waktu":
    st.header("Pola Penggunaan Sepeda Berdasarkan Waktu")
    
    tab1, tab2, tab3 = st.tabs(["Berdasarkan Jam", "Berdasarkan Musim", "Berdasarkan Bulan"])
    
    with tab1:
        st.subheader("Pola Penggunaan Sepeda Berdasarkan Jam")
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Calculate average rentals per hour by workday
        hourly_usage = hour_df.groupby(['hr', 'workingday'])['cnt'].mean().reset_index()
        
        # Create enhanced line plot
        sns.lineplot(data=hourly_usage, x='hr', y='cnt', hue='workingday', palette='coolwarm', 
                    markers=True, dashes=False, linewidth=3, markersize=8, ax=ax)
        
        ax.set_title("Pola Penggunaan Sepeda Berdasarkan Jam", fontsize=14)
        ax.set_xlabel("Jam (0-23)", fontsize=12)
        ax.set_ylabel("Rata-rata Jumlah Penyewaan Sepeda", fontsize=12)
        
        ax.legend(title="Jenis Hari", labels=["Akhir Pekan", "Hari Kerja"], fontsize=10)
        
        # Display labels for every hour (0-23)
        ax.set_xticks(range(0, 24, 1))
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Add annotation for peak hours
        max_workday = hourly_usage[hourly_usage['workingday'] == 1]['cnt'].max()
        max_workday_hour = hourly_usage[(hourly_usage['workingday'] == 1) & 
                                      (hourly_usage['cnt'] == max_workday)]['hr'].values[0]
        
        plt.annotate(f'Jam tersibuk\nhari kerja', 
                    xy=(max_workday_hour, max_workday),
                    xytext=(max_workday_hour+1, max_workday+200),
                    arrowprops=dict(facecolor='black', shrink=0.05, width=1.5),
                    fontsize=10)
        
        st.pyplot(fig)
        
        st.markdown("""
        **Insight:**
        - Hari kerja: Dua puncak aktivitas di pagi (08:00) dan sore (17:00)
        - Akhir pekan: Penggunaan lebih merata dengan puncak di siang hingga sore hari
        """)
    
    with tab2:
        st.subheader("Pola Penggunaan Sepeda Berdasarkan Musim")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Calculate average rentals by season
        seasonal_usage = day_df.groupby('season')['cnt'].mean().reset_index()
        
        # Create enhanced bar plot
        ax = sns.barplot(data=seasonal_usage, x='season', y='cnt', palette='viridis', ax=ax)
        
        # Add more descriptive labels for seasons
        season_labels = {1: 'Musim Semi', 2: 'Musim Panas', 3: 'Musim Gugur', 4: 'Musim Dingin'}
        ax.set_xticklabels([season_labels[i] for i in range(1, 5)], fontsize=12)
        
        # Add values above each bar
        for i, p in enumerate(ax.patches):
            height = p.get_height()
            ax.text(p.get_x() + p.get_width()/2., height + 50,
                    f'{int(height)}',
                    ha="center", fontsize=11)
        
        ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Musim", fontsize=14)
        ax.set_xlabel("Musim", fontsize=12)
        ax.set_ylabel("Rata-rata Jumlah Penyewaan Sepeda", fontsize=12)
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        st.pyplot(fig)
        
        st.markdown("""
        **Insight:**
        - Penyewaan tertinggi terjadi pada musim gugur (Musim Gugur)
        - Diikuti oleh musim panas (Musim Panas) dan musim dingin (Musim Dingin)
        - Musim semi (Musim Semi) memiliki jumlah penyewaan terendah
        """)
        
    with tab3:
        st.subheader("Tren Penyewaan Sepeda Bulanan")
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Calculate average rentals per month
        monthly_usage = day_df.groupby('month')['cnt'].mean().reset_index()
        
        # Create line plot for monthly trends
        sns.lineplot(data=monthly_usage, x='month', y='cnt', marker='o', 
                    color='purple', linewidth=3, markersize=10, ax=ax)
        
        ax.set_title("Tren Penyewaan Sepeda Bulanan", fontsize=14)
        ax.set_xlabel("Bulan", fontsize=12)
        ax.set_ylabel("Rata-rata Jumlah Penyewaan Sepeda", fontsize=12)
        
        # Set x-axis labels with month names
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels(month_names, fontsize=11, rotation=45)
        
        ax.grid(True, linestyle='--', alpha=0.7)
        
        st.pyplot(fig)
        
        st.markdown("""
        **Insight:**
        - Penyewaan sepeda tertinggi terjadi pada bulan Juni dan September
        - Penyewaan terendah terjadi pada bulan-bulan musim dingin (Desember-Januari)
        - Terdapat tren peningkatan dari awal tahun hingga puncak di pertengahan tahun
        """)

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
    
    # Add better labels
    season_labels = {1: 'Musim Semi', 2: 'Musim Panas', 3: 'Musim Gugur', 4: 'Musim Dingin'}
    ax.set_xticklabels([season_labels.get(i, f'Season {i}') for i in season_usage.index], rotation=45)
    
    ax.set_xlabel("Musim")
    ax.set_ylabel("Persentase (%)")
    ax.legend(title="Kategori Penggunaan")
    st.pyplot(fig)
    
    st.subheader("Distribusi Kategori Penggunaan Berdasarkan Cuaca")
    weather_usage = pd.crosstab(day_df['weathersit'], day_df['usage_category'], normalize='index') * 100
    
    fig, ax = plt.subplots(figsize=(10, 6))
    weather_usage.plot(kind='bar', stacked=True, colormap='viridis', ax=ax)
    
    # Add better labels
    weather_labels = {1: 'Cerah', 2: 'Berawan', 3: 'Hujan Ringan', 4: 'Hujan Lebat'}
    ax.set_xticklabels([weather_labels.get(i, f'Weather {i}') for i in weather_usage.index], rotation=45)
    
    ax.set_xlabel("Kondisi Cuaca")
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