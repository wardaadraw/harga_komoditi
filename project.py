import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout='wide')

# Judul dan Pengantar
st.title("Pasar Pangan Indonesia: Antara Keberagaman dan Fluktuasi Harga")
st.markdown("__Bayangkan berjalan melalui pasar tradisional Indonesia, di mana warna-warni komoditas pangan lokal menarik perhatian Anda. Dari beras yang menjadi pokok, telur yang serba guna, hingga gula yang memaniskan hidup kita. Tapi, pernahkah Anda bertanya-tanya mengapa harga-harga ini naik turun seperti rollercoaster? Dari tahun 2019 hingga 2023, kita melihat kisah harga pangan yang penuh drama—dipengaruhi oleh musim, hari raya, dan tentu saja, pandemi yang tak terduga. Melalui web ini, saya mengajak Anda untuk menyelami dunia dinamika harga pangan lokal Indonesia, menjelajahi bagaimana setiap unsur membentuk cerita unik mereka sendiri.__")
st.markdown(
    """
    <hr style="border:2px solid #8B4513; background-color: #FFA07A;">

    """,
    unsafe_allow_html=True
)

# Load data
def load_data(file_path):
    return pd.read_csv(file_path)

#Sidebar untuk Analisis
analysis = st.sidebar.radio("Pilih Analisis:",
    ("Disparitas Harga Nasional", 
    "Harga Pangan di 4 Provinsi",
    "Tren Harga Musim Panen", 
    "Dampak Pandemi",
    "Rekomendasi"))

# Analisis: Disparitas Harga Nasional
if analysis == "Disparitas Harga Nasional":
    data_path = 'disparsitas.csv'
    data = load_data(data_path)

    st.subheader("Disparitas Harga Nasional")
    st.write("""
    Dalam analisis pertama kita, kita akan menyusuri peta Indonesia, mengeksplorasi bagaimana harga beras, telur, dan gula berfluktuasi antar provinsi dari tahun 2019 hingga 2023. Kita melakukan ini untuk mengungkap bagaimana geografi, logistik, dan kebijakan lokal mempengaruhi harga pangan, memberikan kita wawasan tentang tantangan dan peluang dalam pemerataan akses pangan.
    """)

    #Dropdown pemilihan tahun
    tahun = st.sidebar.selectbox('Pilih Tahun', options=sorted(data['Tahun'].unique()))
    # MultiSelect untuk pemilihan Provinsi
    provinsi = st.sidebar.multiselect('Pilih Provinsi', options=sorted(data['Provinsi'].unique()), default=sorted(data['Provinsi'].unique()))
    # Filter data berdasarkan tahun dan provinsi yang dipilih
    filtered_data = data[(data['Tahun'] == tahun) & (data['Provinsi'].isin(provinsi))]
    # Membuat visualisasi dengan Plotly
    fig = px.bar(filtered_data, x='Provinsi', y='rata2_harga', color='Provinsi', 
                 labels={'rata2_harga': 'Rata-Rata Harga'}, height=400, 
                 title='Rata-Rata Harga per Provinsi')
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig)

    st.write("Data menunjukkan fluktuasi harga beras, gula, dan telur antar provinsi dari 2019-2023, mengindikasikan disparitas harga signifikan. Faktor geografi, logistik, dan kebijakan lokal berperan penting.")
    st.markdown(
    """
    * Beras relatif stabil tetapi lebih tinggi di daerah terpencil
    * Gula dan telur menunjukkan kenaikan harga yang lebih signifikan, terutama di provinsi terpencil, dipengaruhi oleh biaya produksi dan distribusi
    """
    )


