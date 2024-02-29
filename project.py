import streamlit as st
import pandas as pd
import sqlalchemy
from sqlalchemy.sql import text
from sqlalchemy import create_engine
import plotly.express as px

# Konfigurasi Database
DATABASE_URL = "mysql+pymysql://root:01234@localhost/pangan"
engine = sqlalchemy.create_engine(DATABASE_URL)

# Fungsi untuk menjalankan query
def run_query(query):
    with engine.connect() as conn:
        return pd.read_sql(query, conn)

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

# Sidebar untuk Analisis
analysis = st.sidebar.radio("Pilih Analisis:", 
    ("Disparitas Harga Nasional", 
    "Harga Pangan di 4 Provinsi",
    "Tren Harga Musim Panen", 
    "Dampak Pandemi",
    "Rekomendasi"))

# Analisis: Disparitas Harga Nasional
if analysis == "Disparitas Harga Nasional":
    st.subheader("Disparitas Harga Nasional")
    st.write("""
    Dalam analisis pertama kita, kita akan menyusuri peta Indonesia, mengeksplorasi bagaimana harga beras, telur, dan gula berfluktuasi antar provinsi dari tahun 2019 hingga 2023. Kita melakukan ini untuk mengungkap bagaimana geografi, logistik, dan kebijakan lokal mempengaruhi harga pangan, memberikan kita wawasan tentang tantangan dan peluang dalam pemerataan akses pangan.
    """)
    query = text("""
    SELECT 
        YEAR(BulanTahun) AS Tahun, Provinsi, jenis_pangan, AVG(Harga) AS rata2_harga
    FROM   
        komoditi
    WHERE 
        Provinsi NOT IN ('Semua Provinsi') AND jenis_pangan IN ('Beras', 'Gula', 'Telur')
    GROUP BY 
        Provinsi, jenis_pangan, YEAR(BulanTahun);
    """)
    df = run_query(query)
    # st.dataframe(df)

    # Dropdown untuk pemilihan Tahun dan Jenis Pangan
    year_option = df['Tahun'].unique().tolist()
    jenis_pangan_option = df['jenis_pangan'].unique().tolist()

    selected_year = st.selectbox('Pilih Tahun:', year_option)
    selected_jenis_pangan = st.selectbox('Pilih Jenis Pangan:', jenis_pangan_option)
    
    # MultiSelect untuk pemilihan Provinsi
    provinsi_option = df['Provinsi'].unique().tolist()
    selected_provinsi = st.multiselect('Pilih Provinsi:', provinsi_option, default=provinsi_option)

    # Filter dataframe berdasarkan tahun, jenis pangan, dan provinsi
    filtered_df = df[(df['Tahun'] == selected_year) & 
                     (df['jenis_pangan'] == selected_jenis_pangan) & 
                     (df['Provinsi'].isin(selected_provinsi))]

    # Membuat grafik dengan Plotly
    fig = px.bar(filtered_df, x='Provinsi', y='rata2_harga', color='Provinsi',
                 labels={'rata2_harga': 'Rata-Rata Harga'}, height=400)
    fig.update_layout(title_text='Rata-Rata Harga per Provinsi', title_x=0.5)

    # Menampilkan grafik
    st.plotly_chart(fig)
    
    st.write("Data menunjukkan fluktuasi harga beras, gula, dan telur antar provinsi dari 2019-2023, mengindikasikan disparitas harga signifikan. Faktor geografi, logistik, dan kebijakan lokal berperan penting.")
    st.markdown(
    """
    * Beras relatif stabil tetapi lebih tinggi di daerah terpencil
    * Gula dan telur menunjukkan kenaikan harga yang lebih signifikan, terutama di provinsi terpencil, dipengaruhi oleh biaya produksi dan distribusi
    """
    )

# Analisis: Perbandingan Harga di DKI Jakarta, Papua, Bali, dan Provinsi Produksi Utama
if analysis == "Harga Pangan di 4 Provinsi":
    st.subheader("Perbandingan Harga di DKI Jakarta, Papua, Bali, dan Provinsi Produksi Utama ")
    st.write("""
    Mengapa harga pangan di Jakarta berbeda dengan di Papua atau Bali? Dalam segmen ini, kita akan membandingkan harga pangan khusus di provinsi-provinsi ini untuk memahami dinamika pasar dan distribusi pangan di Indonesia. Kita memilih provinsi-provinsi ini karena perannya yang unik dalam ekonomi dan pola konsumsi pangan nasional, memberikan kita gambaran yang lebih luas tentang bagaimana pangan diperdagangkan dan dikonsumsi di seluruh negeri.
    """)
    query = text("""
    WITH Rata2Harga AS (
    SELECT
        YEAR(BulanTahun) AS Tahun,
        Provinsi,
        jenis_pangan,
        AVG(Harga) AS rata2_harga
    FROM 
        komoditi
    WHERE 
        Provinsi IN ('DKI Jakarta', 'Jawa Timur', 'Bali', 'Papua')
        AND jenis_pangan IN ('Beras', 'Telur', 'Gula')
    GROUP BY 
        YEAR(BulanTahun), Provinsi, jenis_pangan
    ), HargaRanking AS (
        SELECT
            Tahun,
            Provinsi,
            jenis_pangan,
            rata2_harga,
            RANK() OVER (PARTITION BY Tahun, jenis_pangan ORDER BY rata2_harga ASC) AS RankTerendah,
            RANK() OVER (PARTITION BY Tahun, jenis_pangan ORDER BY rata2_harga DESC) AS RankTertinggi
        FROM
            Rata2Harga
    )
    SELECT
        Tahun,
        Provinsi,
        jenis_pangan,
        rata2_harga,
        CASE
            WHEN RankTerendah = 1 THEN 'Terendah'
            WHEN RankTertinggi = 1 THEN 'Tertinggi'
            ELSE NULL
        END AS status_harga
    FROM
        HargaRanking
    ORDER BY
        Tahun, jenis_pangan, Provinsi;
    """)
    df = run_query(query)
    # st.dataframe(df)

     # Dropdown untuk pemilihan Tahun dan Jenis Pangan
    year_option = df['Tahun'].unique().tolist()
    jenis_pangan_option = df['jenis_pangan'].unique().tolist()

    selected_year = st.selectbox('Pilih Tahun:', year_option)
    selected_jenis_pangan = st.selectbox('Pilih Jenis Pangan:', jenis_pangan_option)
    
    # Filter dataframe
    filtered_df = df[(df['Tahun'] == selected_year) & 
                     (df['jenis_pangan'] == selected_jenis_pangan)]

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
    * DKI Jakarta secara konsisten mencatatkan harga tertinggi, mencerminkan biaya hidup yang lebih tinggi dan permintaan pasar yang kuat. 
    * Sebaliknya, Jawa Timur seringkali memiliki harga terendah, yang mungkin disebabkan oleh perannya sebagai salah satu pusat produksi utama, mempengaruhi biaya distribusi menjadi lebih rendah.
    * Papua menonjol dengan harga telur tertinggi secara konsisten, mengindikasikan biaya logistik yang signifikan. 
    """
    )

# Analisis: Tren Musim Panen
if analysis == "Tren Harga Musim Panen":
    st.subheader("Tren Harga Musim Panen")
    st.write("""
    Musim panen adalah momen krusial yang menentukan harga pangan. Dalam analisis ini, kita akan mengeksplorasi bagaimana musim panen beras, periode giling gula, dan permintaan telur selama hari raya mempengaruhi harga komoditas ini. Memahami ini akan membantu kita dalam merencanakan distribusi dan stok pangan lebih baik, mengurangi risiko kekurangan pasokan dan harga yang melonjak.
    """)
    st.subheader("Secara Nasional")
    query = text("""
    SELECT  
	    YEAR(BulanTahun) AS Tahun,
	    AVG(harga) AS 'rata2_harga',
 	    AVG(CASE WHEN jenis_pangan = 'Beras' AND MONTH(BulanTahun) BETWEEN 3 AND 4 THEN harga ELSE NULL END) AS 'Harga_Panen_Beras',
 	    100 * (AVG(CASE WHEN jenis_pangan = 'Beras' AND MONTH(BulanTahun) BETWEEN 3 AND 4 THEN harga ELSE NULL END) - AVG(harga)) / AVG(harga) AS 'PctChange_Beras',
 	    AVG(CASE WHEN jenis_pangan = 'Gula' AND MONTH(BulanTahun) BETWEEN 5 AND 11 THEN harga ELSE NULL END) AS 'Harga_Panen_Gula',
 	    100 * (AVG(CASE WHEN jenis_pangan = 'Gula' AND MONTH(BulanTahun) BETWEEN 5 AND 11 THEN harga ELSE NULL END) - AVG(harga)) / AVG(harga) AS 'PctChange_Gula',
 	    AVG(CASE WHEN jenis_pangan = 'Telur' AND MONTH(BulanTahun) = 1 THEN harga ELSE NULL END) AS 'Harga_Tahun_Baru_Telur',
 	    100 * (AVG(CASE WHEN jenis_pangan = 'Telur' AND MONTH(BulanTahun) = 1 THEN harga ELSE NULL END) - AVG(harga)) / AVG(harga) AS 'PctChange_Telur'
    FROM 
	    komoditi k 
    WHERE 
	    jenis_pangan IN ('Beras', 'Telur', 'Gula')
    GROUP BY 
	    YEAR(BulanTahun)
    ORDER BY 
	    YEAR(BulanTahun);
    """)
    df = run_query(query)
    # st.dataframe(df)

    # Melakukan pivot data untuk visualisasi
    df_melted = df.melt(id_vars='Tahun', value_vars=['PctChange_Beras', 'PctChange_Gula', 'PctChange_Telur'],
                        var_name='Jenis Pangan', value_name='Persentase Perubahan')

    # Membuat grafik dengan Plotly
    fig = px.line(df_melted, x='Tahun', y='Persentase Perubahan', color='Jenis Pangan', 
                  title='Tren Persentase Perubahan Harga Berdasarkan Jenis Pangan')

    # Menampilkan grafik
    st.plotly_chart(fig)

    st.markdown(
    """
    * Harga beras menunjukkan stabilitas dengan fluktuasi yang lebih rendah
    * Harga gula mengalami lonjakan signifikan pada tahun 2021 diikuti oleh penurunan
    * Harga telur terus meningkat, menunjukkan kemungkinan permintaan atau kenaikan biaya yang berkelanjutan
    """
    )

    # FOKUS 4 PROVINSI
    st.subheader("Provinsi Tertentu")
    query = text("""
    SELECT
        YEAR(BulanTahun) AS Tahun,
        Provinsi,
        AVG(CASE WHEN jenis_pangan = 'Beras' THEN harga ELSE NULL END) AS 'Harga_Beras_Rata2',
        AVG(CASE WHEN jenis_pangan = 'Beras' AND MONTH(BulanTahun) BETWEEN 3 AND 4 THEN harga ELSE NULL END) AS 'Harga_Panen_Beras',
        100 * (AVG(CASE WHEN jenis_pangan = 'Beras' AND MONTH(BulanTahun) BETWEEN 3 AND 4 THEN harga ELSE NULL END) - AVG(CASE WHEN jenis_pangan = 'Beras' THEN harga ELSE NULL END)) / AVG(CASE WHEN jenis_pangan = 'Beras' THEN harga ELSE NULL END) AS 'PctChange_Beras',
        AVG(CASE WHEN jenis_pangan = 'Gula' THEN harga ELSE NULL END) AS 'Harga_Gula_Rata2',
        AVG(CASE WHEN jenis_pangan = 'Gula' AND MONTH(BulanTahun) BETWEEN 5 AND 11 THEN harga ELSE NULL END) AS 'Harga_Panen_Gula',
        100 * (AVG(CASE WHEN jenis_pangan = 'Gula' AND MONTH(BulanTahun) BETWEEN 5 AND 11 THEN harga ELSE NULL END) - AVG(CASE WHEN jenis_pangan = 'Gula' THEN harga ELSE NULL END)) / AVG(CASE WHEN jenis_pangan = 'Gula' THEN harga ELSE NULL END) AS 'PctChange_Gula',
        AVG(CASE WHEN jenis_pangan = 'Telur' THEN harga ELSE NULL END) AS 'Harga_Telur_Rata2',
        AVG(CASE WHEN jenis_pangan = 'Telur' AND MONTH(BulanTahun) = 1 THEN harga ELSE NULL END) AS 'Harga_Panen_Telur',
        100 * (AVG(CASE WHEN jenis_pangan = 'Telur' AND MONTH(BulanTahun) = 1 THEN harga ELSE NULL END) - AVG(CASE WHEN jenis_pangan = 'Telur' THEN harga ELSE NULL END)) / AVG(CASE WHEN jenis_pangan = 'Telur' THEN harga ELSE NULL END) AS 'PctChange_Telur'
    FROM
        komoditi
    WHERE
        jenis_pangan IN ('Beras', 'Telur', 'Gula')
        AND Provinsi IN ('DKI Jakarta', 'Jawa Timur', 'Bali', 'Papua')
    GROUP BY
        Provinsi, YEAR(BulanTahun)
    ORDER BY
        YEAR(BulanTahun), Provinsi;
    """)
    df = run_query(query)
    # st.dataframe(df)
    
    # Judul dan Pengantar
    st.title("Tren Persentase Perubahan Harga Pangan di Provinsi Tertentu")

    # Dropdown untuk pemilihan Jenis Pangan
    jenis_pangan_option = ['Beras', 'Gula', 'Telur']
    selected_jenis_pangan = st.selectbox('Pilih Jenis Pangan:', jenis_pangan_option)

    # Memutuskan kolom berdasarkan jenis pangan yang dipilih
    kolom = f'PctChange_{selected_jenis_pangan}'

    # Membuat grafik dengan Plotly
    fig = px.line(df, x='Tahun', y=kolom, color='Provinsi',
                labels={kolom: f'Persentase Perubahan {selected_jenis_pangan}'}, title=f'Tren Persentase Perubahan {selected_jenis_pangan} per Provinsi')
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
if analysis == "Dampak Pandemi":
    st.subheader("Evaluasi Harga Pangan Secara Nasional Akibat Pandemi")
    st.write("""
    Pandemi COVID-19 telah mengguncang ekonomi global, termasuk pasar pangan Indonesia. Dalam bagian ini, kita akan menganalisis bagaimana rata-rata harga beras, telur, dan gula berubah secara nasional dari tahun ke tahun, sebelum, selama, dan pasca pandemi. Analisis ini vital untuk memahami dampak pandemi terhadap ketahanan pangan dan ekonomi, serta untuk merencanakan langkah-langkah pemulihan.
    """)
    query = text("""
    SELECT  
        jenis_pangan,
        AVG(harga) AS 'rata2_harga',
        AVG(CASE WHEN YEAR(BulanTahun) = 2019 THEN harga ELSE NULL END) AS 'Harga_Pra',
        100 * (AVG(CASE WHEN YEAR(BulanTahun) = 2019 THEN harga ELSE NULL END) - AVG(harga)) / AVG(harga) AS Pctdiff_pra,
        AVG(CASE WHEN YEAR(BulanTahun) BETWEEN 2020 AND 2021 THEN harga ELSE NULL END) AS 'Harga_Covid',
        100 * (AVG(CASE WHEN YEAR(BulanTahun) BETWEEN 2020 AND 2021 THEN harga ELSE NULL END) - AVG(harga)) / AVG(harga) AS Pctdiff_covid,
        AVG(CASE WHEN YEAR(BulanTahun) BETWEEN 2022 AND 2023 THEN harga ELSE NULL END) AS 'Harga_Pasca',
        100 * (AVG(CASE WHEN YEAR(BulanTahun) BETWEEN 2022 AND 2023 THEN harga ELSE NULL END) - AVG(harga)) / AVG(harga) AS Pctdiff_pasca
    FROM 
        komoditi k 
    WHERE 
        jenis_pangan IN ('Beras', 'Telur', 'Gula')
    GROUP BY 
        jenis_pangan
    ORDER BY 
        jenis_pangan;
    """)
    df = run_query(query)
    # st.dataframe(df)

    # Transformasi dataframe untuk mempersiapkan data untuk plot
    df_melted = df.melt(id_vars='jenis_pangan', value_vars=['Pctdiff_pra', 'Pctdiff_covid', 'Pctdiff_pasca'],
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
    * Harga ketiga jenis pangan memiliki pola yang hampir sama
    * Harga pada saat sebelum covid (2019), harga beras cukup stabil sedangkan gula dan telur mengalami penurunan harga yang cukup memuaskan yaitu >5%
    * Kondisi saat covid (2020-2021), harga cendertung turun
    * Kondisi pasca covid (2022-2023) harga ketiga pangan secara nasional mengalami kenaikan yang cukup tinggi berada di angka >5%
    """
    )

    # FOKUS 4 PROVINSI
    st.subheader("Evaluasi Harga Pangan Akibat Pandemi 4 Provinsi")
    st.write("""
    Lebih dalam lagi, kita akan membedah perubahan harga tiap komoditas pangan secara terpisah, membandingkan dinamika harga di empat provinsi kunci sebelum dan selama pandemi. Ini akan memberikan kita wawasan spesifik tentang bagaimana setiap komoditas terpengaruh dan strategi apa yang efektif untuk mengatasi fluktuasi harga.
    """)
    query = text("""
    SELECT  
        jenis_pangan,
        Provinsi, 
        AVG(harga) AS 'rata2_harga',
        AVG(CASE WHEN YEAR(BulanTahun) = 2019 THEN harga ELSE NULL END) AS 'Harga_Pra',
        100 * (AVG(CASE WHEN YEAR(BulanTahun) = 2019 THEN harga ELSE NULL END) - AVG(harga)) / AVG(harga) AS Pctdiff_pra,
        AVG(CASE WHEN YEAR(BulanTahun) BETWEEN 2020 AND 2021 THEN harga ELSE NULL END) AS 'Harga_Covid',
        100 * (AVG(CASE WHEN YEAR(BulanTahun) BETWEEN 2020 AND 2021 THEN harga ELSE NULL END) - AVG(harga)) / AVG(harga) AS Pctdiff_covid,
        AVG(CASE WHEN YEAR(BulanTahun) BETWEEN 2022 AND 2023 THEN harga ELSE NULL END) AS 'Harga_Pasca',
        100 * (AVG(CASE WHEN YEAR(BulanTahun) BETWEEN 2022 AND 2023 THEN harga ELSE NULL END) - AVG(harga)) / AVG(harga) AS Pctdiff_pasca
    FROM 
        komoditi k 
    WHERE 
        jenis_pangan IN ('Beras', 'Telur', 'Gula')
        AND Provinsi IN ('DKI Jakarta', 'Jawa Timur', 'Bali', 'Papua')
    GROUP BY 
        jenis_pangan, Provinsi
    ORDER BY 
        jenis_pangan ;
        """)
    df = run_query(query)
    # st.dataframe(df)  

    # Menambahkan pilihan jenis pangan
    jenis_pangan_pilihan = st.selectbox("Pilih Jenis Pangan:", df['jenis_pangan'].unique())

    # Filter dataframe berdasarkan pilihan jenis pangan
    df_filtered = df[df['jenis_pangan'] == jenis_pangan_pilihan]

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
    * Harga Beras dan Gula menurun selama pandemi, yang mungkin mengindikasikan kelebihan pasokan atau penurunan permintaan
    * Setelah pandemi, kenaikan harga menandakan fase penyesuaian pasar dan pemulihan ekonomi
    """
    )

if analysis == "Rekomendasi":
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
