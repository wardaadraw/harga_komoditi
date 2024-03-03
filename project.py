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
analysis = st.sidebar.radio("__Pilih Analisis:__",
    ("__Disparitas Harga Nasional__", 
    "__Harga Pangan di 4 Provinsi__",
    "__Tren Harga Musim Panen__", 
    "__Dampak Pandemi__",
    "__Rekomendasi__"))

# Analisis: Disparitas Harga Nasional
if analysis == "__Disparitas Harga Nasional__":
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

# Analisis: Harga Pangan di 4 Provinsi
if analysis == "__Harga Pangan di 4 Provinsi__":
    data_path = 'perbandingan harga.csv'
    data = load_data(data_path)

    st.subheader("Perbandingan Harga di DKI Jakarta, Papua, Bali, dan Provinsi Produksi Utama")
    st.write("""
    Mengapa harga pangan di Jakarta berbeda dengan di Papua atau Bali? 
    Dalam segmen ini, kita akan membandingkan harga pangan khusus di provinsi-provinsi 
    ini untuk memahami dinamika pasar dan distribusi pangan di Indonesia. Kita memilih 
    provinsi-provinsi ini karena perannya yang unik dalam ekonomi dan pola konsumsi pangan nasional, 
    memberikan kita gambaran yang lebih luas tentang bagaimana pangan diperdagangkan dan dikonsumsi 
    di seluruh negeri.
    """)
    # Dropdown untuk pemilihan Tahun dan Jenis Pangan
    year_option = data['Tahun'].unique().tolist()
    jenis_pangan_option = data['jenis_pangan'].unique().tolist()

    selected_year = st.sidebar.selectbox('Pilih Tahun:', year_option)
    selected_jenis_pangan = st.sidebar.selectbox('Pilih Jenis Pangan:', jenis_pangan_option)
    
    # Filter dataframe
    filtered_df = data[(data['Tahun'] == selected_year) & 
                     (data['jenis_pangan'] == selected_jenis_pangan)]

    # Membuat line chart dengan Plotly
    fig = px.line(filtered_df, x='Provinsi', y='rata2_harga', color='Provinsi', 
                  text='status_harga', title=f'Rata-Rata Harga {selected_jenis_pangan} pada {selected_year}')
    
    # Menunjukkan label hanya untuk "Tertinggi" dan "Terendah"
    fig.for_each_trace(lambda t: t.update(textposition="top center"))
    fig.update_traces(textposition='top center')

    fig.update_layout(showlegend=True)
    fig.update_xaxes(title_text='Provinsi')
    fig.update_yaxes(title_text='Rata-Rata Harga')

    # Menampilkan grafik
    st.plotly_chart(fig)

    st.write("Data dari 2019 hingga 2023 mengungkap disparitas harga beras, gula, dan telur di Bali, DKI Jakarta, Jawa Timur, dan Papua, menyoroti dinamika pasar dan distribusi pangan yang kompleks di Indonesia.")
    st.markdown(
    """
    * DKI Jakarta secara konsisten mencatatkan harga tertinggi pada pangan Beras, mencerminkan biaya hidup yang lebih tinggi dan permintaan pasar yang kuat. 
    * Papua menonjol dengan harga telur dan gula tertinggi secara konsisten, mengindikasikan biaya logistik yang signifikan. 
    * Sebaliknya, Jawa Timur seringkali memiliki harga terendah di ketiga pangan, yang mungkin disebabkan oleh perannya sebagai salah satu pusat produksi utama, mempengaruhi biaya distribusi menjadi lebih rendah.
    """
    )

if analysis == "__Tren Harga Musim Panen__":
    st.subheader("Tren Harga Musim Panen")
    st.write("""
            Musim panen adalah momen krusial yang menentukan harga pangan. Dalam analisis ini, kita akan mengeksplorasi bagaimana musim panen beras, periode giling gula, dan permintaan telur selama hari raya mempengaruhi harga komoditas ini. Memahami ini akan membantu kita dalam merencanakan distribusi dan stok pangan lebih baik, mengurangi risiko kekurangan pasokan dan harga yang melonjak.
            """)
    #Plot 1
    st.subheader("Secara Nasional")
    data_path = 'pct nasional.csv'
    data = load_data(data_path)
    # Melakukan pivot data
    data_melted = data.melt(id_vars='Tahun', value_vars=['PctChange_Beras', 'PctChange_Gula', 'PctChange_Telur'],
                            var_name='Jenis Pangan', value_name='Persentase Perubahan')

    # Mengganti nama variabel untuk memudahkan visualisasi
    data_melted['Jenis Pangan'] = data_melted['Jenis Pangan'].str.replace('PctChange_', '')

    # Membuat grafik dengan Plotly
    fig = px.line(data_melted, x='Tahun', y='Persentase Perubahan', color='Jenis Pangan', 
                title='Tren Persentase Perubahan Harga Berdasarkan Jenis Pangan')

    # Menampilkan grafik di Streamlit
    st.plotly_chart(fig)

    st.markdown(
        """
        * Harga beras menunjukkan stabilitas dengan fluktuasi yang lebih rendah
        * Harga gula mengalami lonjakan signifikan pada tahun 2021 diikuti oleh penurunan
        * Harga telur terus meningkat, menunjukkan kemungkinan permintaan atau kenaikan biaya yang berkelanjutan
        """
        )
    
    #Plot 2
    st.subheader("Provinsi Tertentu")
    data_path = 'pct panen provinsi.csv'
    data = load_data(data_path)

    # Dropdown untuk pemilihan Jenis Pangan
    jenis_pangan_option = ['Beras', 'Gula', 'Telur']
    selected_jenis_pangan = st.selectbox('Pilih Jenis Pangan:', jenis_pangan_option)

    # Memutuskan kolom berdasarkan jenis pangan yang dipilih
    kolom = f'PctChange_{selected_jenis_pangan}'

    # Membuat grafik dengan Plotly
    fig = px.line(data, x='Tahun', y=kolom, color='Provinsi',
                labels={kolom: f'Persentase Perubahan Harga {selected_jenis_pangan}'}, title=f'Tren Persentase Perubahan {selected_jenis_pangan} per Provinsi')
    fig.update_xaxes(type='category')

    # Menampilkan grafik
    st.plotly_chart(fig)

    st.markdown(
    """
    * Provinsi seperti Papua mengalami fluktuasi harga yang lebih besar, yang mungkin dipengaruhi oleh faktor geografis dan tantangan logistik
    * DKI Jakarta dan Bali, dengan karakteristik urban dan wisata, menunjukkan kenaikan harga untuk Gula dan Telur, yang bisa dipengaruhi oleh dinamika permintaan yang tinggi
    * Jawa Timur menunjukkan indikasi stabilitas harga yang lebih baik, yang mungkin mencerminkan kondisi produksi yang konsisten dan kebijakan lokal yang efektif dalam mengelola fluktuasi pasar
    """
    )

# Analisis: Evaluasi Dampak Pandemi
if analysis == "__Dampak Pandemi__":
    # Secara Nasional
    st.subheader("Evaluasi Harga Pangan Secara Nasional Akibat Pandemi")
    st.write("""
    Pandemi COVID-19 telah mengguncang ekonomi global, termasuk pasar pangan Indonesia. Dalam bagian ini, kita akan menganalisis bagaimana rata-rata harga beras, telur, dan gula berubah secara nasional dari tahun ke tahun, sebelum, selama, dan pasca pandemi. Analisis ini vital untuk memahami dampak pandemi terhadap ketahanan pangan dan ekonomi, serta untuk merencanakan langkah-langkah pemulihan.
    """)
    # Load data
    data_path = 'pct pandemi nasional.csv'
    data = load_data(data_path)
    # Transformasi dataframe untuk mempersiapkan data untuk plot
    df_melted = data.melt(id_vars='jenis_pangan', value_vars=['Pctdiff_pra', 'Pctdiff_covid', 'Pctdiff_pasca'],
                        var_name='Kondisi', value_name='Persentase Perubahan')

    # Membuat line chart dengan Plotly, kali ini 'Kondisi' akan menjadi sumbu x dan 'jenis_pangan' akan digunakan untuk warna
    fig = px.line(df_melted, x='Kondisi', y='Persentase Perubahan', color='jenis_pangan', 
                title='Persentase Perubahan Harga Akibat Pandemi untuk Beras, Telur, dan Gula')

    # Menampilkan grafik
    st.plotly_chart(fig)

    st.write("""
    """)
    st.markdown(
    """
    * Harga telur dan beras mengalami penurunan pada kondisi covid (2020-2021), sedangkan gula konsisten mengalami kenaikan pada 3 periode ini
    * Harga pada saat sebelum covid (2019), harga beras cukup stabil sedangkan gula dan telur mengalami penurunan harga yang cukup memuaskan yaitu >5%
    * Kondisi saat covid (2020-2021), harga cenderung turun
    * Kondisi pasca covid (2022-2023) harga ketiga pangan secara nasional mengalami kenaikan yang cukup tinggi berada di angka >5%
    """
    )

    # FOKUS 4 PROVINSI
    st.subheader("Evaluasi Harga Pangan Akibat Pandemi 4 Provinsi")
    st.write("""
    Lebih dalam lagi, kita akan membedah perubahan harga tiap komoditas pangan secara terpisah, membandingkan dinamika harga di empat provinsi kunci sebelum dan selama pandemi. Ini akan memberikan kita wawasan spesifik tentang bagaimana setiap komoditas terpengaruh dan strategi apa yang efektif untuk mengatasi fluktuasi harga.
    """)
    # Load data
    data_path = 'pct pandemi provinsi.csv'
    data = load_data(data_path)
    # Menambahkan pilihan jenis pangan
    jenis_pangan_pilihan = st.selectbox("Pilih Jenis Pangan:", data['jenis_pangan'].unique())

    # Filter dataframe berdasarkan pilihan jenis pangan
    df_filtered = data[data['jenis_pangan'] == jenis_pangan_pilihan]

    # Transformasi dataframe untuk mempersiapkan data untuk plot, kali ini 'Kondisi' akan menjadi sumbu x
    df_melted = df_filtered.melt(id_vars=['Provinsi'], value_vars=['Pctdiff_pra', 'Pctdiff_covid', 'Pctdiff_pasca'],
                        var_name='Kondisi', value_name='Persentase Perubahan')

    # Membuat line chart dengan Plotly, kali ini 'Kondisi' akan menjadi sumbu x dan 'Provinsi' akan digunakan untuk warna
    fig = px.line(df_melted, x='Kondisi', y='Persentase Perubahan', color='Provinsi', 
                title=f'Perubahan Persentase Harga {jenis_pangan_pilihan} Akibat Pandemi per Provinsi')

    # Menampilkan grafik
    st.plotly_chart(fig)
    
    st.write(" Perubahan harga yang terjadi menunjukkan dampak pandemi COVID-19 terhadap ekonomi dan pasar pangan di Indonesia")
    st.markdown(
    """
    * Jawa Timur cenderung menunjukkan perubahan yang lebih kecil dan lebih stabil untuk beras dan telur, menunjukkan ketahanan harga terhadap kondisi pandemi.
    * DKI Jakarta dan Papua menunjukkan perubahan harga yang lebih besar, khususnya pasca-pandemi, yang mungkin menandakan perubahan dalam permintaan atau pasokan yang lebih signifikan.
    * Bali menunjukkan penurunan yang sangat tajam selama pandemi pada harga telur yang diikuti dengan peningkatan yang tajam, yang bisa jadi karena faktor-faktor eksternal seperti perubahan dalam kebijakan perdagangan atau permintaan yang berubah drastis.
    """
    )

# Rekomendasi
if analysis == "__Rekomendasi__":
    st.write("""
    Berdasarkan analisis data harga beras, gula, dan telur dari tahun 2019 hingga 2023, 
    terlihat adanya fluktuasi harga yang signifikan di provinsi DKI Jakarta, Jawa Timur, Bali, dan Papua. 
    Fluktuasi ini dipengaruhi oleh berbagai faktor termasuk geografi, logistik, kebijakan lokal, dan dampak pandemi COVID-19.
    """)
    st.subheader("Insights")
    st.markdown("""
        1. Pemulihan Pasca Pandemi: Pasca pandemi, terjadi kenaikan harga yang mencerminkan pemulihan ekonomi. Hal ini menunjukkan perlunya kebijakan yang mendukung pemulihan sektor pertanian dan pangan untuk memastikan ketersediaan dan keterjangkauan pangan bagi masyarakat
        2. Strategi Pengendalian Harga: Pemerintah harus mempertimbangkan strategi pengendalian harga dan stabilisasi pasar, termasuk cadangan pangan strategis dan intervensi pasar bila perlu
        3. Penelitian dan Pengembangan: Investasi dalam penelitian dan pengembangan sektor pertanian sangat diperlukan untuk meningkatkan produktivitas dan efisiensi, yang pada akhirnya akan membantu menstabilkan harga dan mendorong kesejahteraan masyarakat
    """)

    st.subheader("Rekomendasi Nasional")
    st.markdown("""
        1. Manajemen Harga: Diperlukan kebijakan yang menargetkan subsidi pada waktu-waktu tertentu untuk menstabilkan harga, terutama selama masa krisis seperti pandemi
        2. Ketahanan Pangan: Pengembangan program ketahanan pangan yang dapat memperkuat akses masyarakat terhadap pangan berkualitas dengan harga terjangkau
    """)

    st.subheader("Rekomendasi Provinsi")
    st.markdown("""
        1. DKI Jakarta: Optimalisasi logistik untuk menekan biaya distribusi
        2. Jawa Timur: Memperkuat efisiensi rantai pasokan antarprovinsi
        3. Bali: Menyesuaikan stok dan pasokan dengan fluktuasi permintaan wisata
        4. Papua: Meningkatkan infrastruktur untuk mengurangi biaya logistik
    """)
