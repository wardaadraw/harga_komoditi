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
    Dalam analisis pertama kita, kita akan menyusuri peta Indonesia, mengeksplorasi bagaimana harga beras, telur, dan gula 
    berfluktuasi antar provinsi dari tahun 2019 hingga 2023. Kita melakukan ini untuk mengungkap bagaimana geografi, 
    logistik, dan kebijakan lokal mempengaruhi harga pangan, memberikan kita wawasan tentang tantangan dan peluang 
    dalam pemerataan akses pangan. Pemilihan ketiga jenis pangan tersebut dikarenakan :
    1. Beras : menjadi pokok kebutuhan sehari-hari'
    2. Telur : bahan pangan serba guna
    3. Gula  : pemanis kehidupan 
    """)

    #Membuat pemetaan wilayah waktu untuk setiap provinsi
    wilayah_mapping = {
        "Indonesia Barat": ["Aceh", "Sumatera Utara", "Sumatera Barat", "Riau", "Jambi", "Sumatera Selatan", "Bengkulu", "Lampung", "Kepulauan Bangka Belitung", "Kepulauan Riau", "DKI Jakarta", "Jawa Barat", "Jawa Tengah", "DI Yogyakarta", "Jawa Timur", "Banten"],
        "Indonesia Tengah": ["Kalimantan Barat", "Kalimantan Tengah", "Kalimantan Selatan", "Kalimantan Timur", "Sulawesi Utara", "Sulawesi Tengah", "Sulawesi Selatan", "Sulawesi Tenggara", "Bali", "Nusa Tenggara Barat", "Nusa Tenggara Timur"],
        "Indonesia Timur": ["Maluku", "Maluku Utara", "Papua", "Papua Barat", "Sulawesi Barat", "Gorontalo", "Kalimantan Utara"]
    }

    # Fungsi untuk menentukan wilayah berdasarkan provinsi
    def determine_wilayah(provinsi):
        for wilayah, provinsis in wilayah_mapping.items():
            if provinsi in provinsis:
                return wilayah
        return "Tidak diketahui"

    # Tambahkan kolom 'Wilayah' ke dataframe
    data['Wilayah'] = data['Provinsi'].apply(determine_wilayah)

    # Dropdown tahun dan jenis pangan
    tahun = st.sidebar.selectbox('Pilih Tahun', options=sorted(data['Tahun'].unique()))
    # Filter data berdasarkan tahun yang dipilih
    filtered_data = data[data['Tahun'] == tahun]
    # Dropdown jenis pangan
    selected_jenis_pangan = st.sidebar.selectbox('Pilih Jenis Pangan:', data['jenis_pangan'].unique().tolist())
    # Kemudian, ketika menyaring data, tidak akan terjadi error karena 'selected_jenis_pangan' adalah string tunggal
    filtered_data = filtered_data[filtered_data['jenis_pangan'] == selected_jenis_pangan]

    # Modifikasi untuk menambahkan opsi "Semua"
    provinsi_options = ["Semua"] + sorted(data['Provinsi'].unique())
    selected_provinsi = st.sidebar.multiselect('Pilih Provinsi', options=provinsi_options, default="Semua")
    # Logika pemilihan provinsi (termasuk penanganan untuk pilihan "Semua")
    if "Semua" in selected_provinsi:
        # Untuk kasus "Semua", Anda mungkin tidak perlu melakukan perubahan lebih lanjut karena
        # filtered_data sudah berisi data yang sesuai dengan tahun dan jenis pangan yang dipilih
        fig = px.bar(filtered_data, x='Provinsi', y='rata2_harga', color='Wilayah', 
                    labels={'rata2_harga': 'Rata-Rata Harga'}, height=400,
                    title=f'Rata-Rata Harga {selected_jenis_pangan} per Provinsi')
    else:
        # Jika provinsi tertentu dipilih, pastikan data juga disaring berdasarkan pilihan provinsi tersebut
        filtered_data_specific = filtered_data[filtered_data['Provinsi'].isin(selected_provinsi)]
        fig = px.bar(filtered_data_specific, x='Provinsi', y='rata2_harga', color='Provinsi',
                    labels={'rata2_harga': 'Rata-Rata Harga'}, height=400,
                    title=f'Rata-Rata Harga {selected_jenis_pangan} per Provinsi')
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig)

    
    st.write("Data menunjukkan fluktuasi harga beras, gula, dan telur antar provinsi dari 2019-2023, mengindikasikan disparitas harga signifikan. Faktor geografi, logistik, dan kebijakan lokal berperan penting.")
    st.markdown(
    """
    * Harga Beras tertinggi pada 5 tahun terakhir khususnya 2020-2023 berada di Provinsi Kalimantan Tengah dan harga menengah kebawah didominasi wilayah Indonesia Tengah dan Barat khususnya Provinsi Nusa Tenggara Barat yang konsisten memiliki harga terendah.
    * Harga Gula pada wilayag Indonesia bagian Timur khusunya Provinsi Papua dan Papua Barat secara konsisten menunjukkan harga tertinggi di 5 tahun terakhir, sedangkan harga terendah dimiliki oleh Provinsi Kepulauan Riau dan didominasi oleh wilayah Indonesia bagian Barat.
    * Harga Telur pada wilayah Indonesia bagian Timur secara konsisten menunjukkan harga tertinggi di 5 tahun terakhir, khususnya Provinsi Papua yang memiliki harga > 30.000 di setiap tahunnya. Sedangkan untuk harga menengah ke bawah, didominasi oleh wilayah Indonesia Barat.
    """
    )

# Analisis: Harga Pangan di 4 Provinsi
if analysis == "__Harga Pangan di 4 Provinsi__":
    data_path = 'perbandingan harga.csv'
    data = load_data(data_path)

    st.subheader("Perbandingan Harga di DKI Jakarta, Papua, Bali, dan Provinsi Produksi Utama")
    st.write("""
    Mengapa harga pangan di Jakarta berbeda dengan di Jawa Timur, Papua atau Bali? 
    Dalam segmen ini, kita akan membandingkan harga pangan khusus di provinsi-provinsi 
    ini untuk menangkap dinamika produksi dan konsumsi yang beragam serta tantangan logistik yang memberikan
    gambaran lebih luas tentang bagaimana pangan diperdagangkan dan dikonsumsi seluruh negeri.
    1. DKI Jakarta dipilih karena umumnya menjadi provinsi dengan konsumsi tertinggi berbagai komoditas akibat karakteristiknya sebagai ibu kota negara dan urban,
    2. Jawa Timur dipilih dikarenakan merupakan salah satu provinsi pemroduksi terbesar ketiga jenis pangan yang dianalisis (Beras, Gula, Telur),
    3. Bali dipilih dikarenakan karakteristiknya sebagai provinsi andalan destinasi wisata baik domestik maupun internasional, dan
    4. Papua dipilih dikarenakan termasuk provinsi yang berat tantangan logistiknya karena dipengaruhi olek karakteristik geografisnya
    """)

    # Dropdown untuk pemilihan Tahun dan Jenis Pangan
    year_option = data['Tahun'].unique().tolist()
    jenis_pangan_option = data['jenis_pangan'].unique().tolist()

    selected_year = st.sidebar.selectbox('Pilih Tahun:', year_option)
    selected_jenis_pangan = st.sidebar.selectbox('Pilih Jenis Pangan:', jenis_pangan_option)

    # Filter dataframe
    filtered_df = data[(data['Tahun'] == selected_year) & 
                    (data['jenis_pangan'] == selected_jenis_pangan)]

    # Membuat bar chart dengan Plotly
    fig = px.bar(filtered_df, x='Provinsi', y='rata2_harga', color='Provinsi', 
                title=f'Rata-Rata Harga {selected_jenis_pangan} pada {selected_year}')

    fig.update_layout(showlegend=True)
    fig.update_xaxes(title_text='Provinsi')
    fig.update_yaxes(title_text='Rata-Rata Harga', range=[0, filtered_df['rata2_harga'].max() + (filtered_df['rata2_harga'].max() * 0.1)])

    # Opsi untuk menambahkan teks "Tertinggi" dan "Terendah" menggunakan anotasi (jika diperlukan)
    # Ini adalah contoh sederhana dan mungkin perlu disesuaikan lebih lanjut sesuai dengan kebutuhan Anda
    if not filtered_df.empty:
        max_value = filtered_df['rata2_harga'].max()
        min_value = filtered_df['rata2_harga'].min()

        max_provinsi = filtered_df[filtered_df['rata2_harga'] == max_value]['Provinsi'].iloc[0]
        min_provinsi = filtered_df[filtered_df['rata2_harga'] == min_value]['Provinsi'].iloc[0]

        fig.add_annotation(x=max_provinsi, y=max_value, text="Tertinggi", showarrow=True, arrowhead=1)
        fig.add_annotation(x=min_provinsi, y=min_value, text="Terendah", showarrow=True, arrowhead=1)

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
    data_path = 'pct panen nasional fix.csv'
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
        * Harga beras pada musim panen menunjukkan penurunan harga yang tidak terlalu signifikan atau dibawah 5% penurunannya, kecuali tahun 2020 menuju 2021 mengalami penurunan drastis hingga >40%, namun harga mulai kembali ke normal tahun 2021 menuju 2022.
        * Harga gula pada musim giling gula tebu tidak menunjukkan penurunan selama 5 tahun terakhir, bahkan sempat mengalami kenaikan harga dari harga normal gula.
        * Harga telur pada tahun baru mengalami fluktuasi dan harganya tidak pernah lebih rendah dari harga normal telur.
        """
        )
    
    #Plot 2
    st.subheader("Provinsi Tertentu")
    data_path = 'pct panen provinsi fix.csv'
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
    * Harga beras di keempat provinsi cukup terpengaruhi oleh musim panen yang ditunjukkan dengan adanya penurunan harga dibawah 0 mulai dari 2019 menuju 2020 hingga 2023. Namun keempatnya tidak memiliki perbedaan signifikan terkait tren harga beras pada saat musim panen beras, tetapi terlihat Bali menonjol dengan harga tertinggi dari tahun 2021 hingga pertengahan 2023.
    * Secara garis besar, pada saat musim panen keempat prvinsi tidak mengalami penurunan yang berarti terkait harga gula. Papua mendominasi harga gula terendah 5 tahun terakhir (2019-2023) selama musim panen dan diikuti jawa timur, sedangkan DKI Jakarta dan Bali mendominasi pada harga tinggi gula
    * Selama 5 tahun terakhir, Papua mendominasi harga telur terendah dari provinsi lain kecuali 2023, sedangkan jakarta dan bali mendominasi di harga tinggi, serta Jawa Timur berada pada posisi ke dua di harga terendah.
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
    # Menambahkan pilihan jenis pangan dan provinsi
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
        1. Fluktuasi Harga Antarprovinsi: Data menunjukkan fluktuasi harga signifikan untuk beras, gula, dan telur antarprovinsi dari tahun 2019 hingga 2023, mengungkap disparitas harga nasional.
        2. Analisis Tren Harga Berdasarkan Komoditas: Harga pangan beras, gula, dan telur yang menengah ke bawah didominasi oleh wilayah Indonesia bagian barat, sedangkan harga tinggi didominasi oleh Indoenesia timur dan beberapa barat khususnya Papua. 
        3. Dinamika Harga Spesifik Provinsi: DKI Jakarta secara konsisten mencatatkan harga tertinggi pada pangan Beras, mencerminkan biaya hidup dan permintaan pasar yang tinggi diikuti Bali sebagai provinsi karakteristik wisata. Jawa Timur sering memiliki harga terendah, berkat peranannya sebagai pusat produksi. Sementara itu, Papua yang mewakili provinsi terpencil lainnya mengalami harga tinggi, terutama untuk telur dan gula, yang menunjukkan tantangan logistik dan biaya transportasi yang lebih tinggi.
        4. Pengaruh Musim Panen dan Siklus Produksi: Secara nasional, hanya pangan beras yang menunjukkan penurunan harga di musim panennya, sedangkan gula dan telur tidak mengalami penurunan harga di bawah rata-rata harga masing-masing pangan. Secara khusus, provinsi Bali dan DKI Jakarta konsisten memiliki harga tertinggi di setiap pangan diikuti jawa timur dan papua yang mendominasi harga rendah untuk gula dan telur.
        5. Dampak Pandemi COVID-19: Harga Beras dan Telur mengalami penurunan pada saat menuju kondisi covid-19 dan naik drastis saat kondisi pasca atau pemulihan dari pandemi covid-19 baik secara nasional maupun keempat provinsi khusus. Sedangkan harga gula terus mengalami kenaikan seiring berjalannya waktu secara nasional maupun keempat provinsi khusus.
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
