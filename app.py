import streamlit as st
import pandas as pd
import io
from datetime import datetime
import openpyxl

# Konfigurasi halaman
st.set_page_config(
    page_title="Paxlist Data Processor",
    page_icon="✈️",
    layout="wide"
)

# Judul aplikasi
st.title("✈️ Paxlist Data Processing System")
st.markdown("---")

# Sidebar untuk menu
st.sidebar.title("📋 Menu")
menu_options = ["JT OUTGOING", "JT INCOMING", "IW", "IU", "ID"]
selected_menu = st.sidebar.selectbox("Pilih Menu:", menu_options)

# Kolom wajib yang harus ada dalam file
REQUIRED_COLUMNS = [
    'Departure Date Time (LT)',
    'Dep Station',
    'Flight',
    'Pairing Code',
    'Rank'
]

def validate_file(df):
    """Validasi apakah file memiliki kolom yang diperlukan"""
    missing_columns = []
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            missing_columns.append(col)
    
    return len(missing_columns) == 0, missing_columns

def custom_rank_sort(rank):
    """Custom sorting untuk kolom Rank"""
    rank_order = {'CPT': 1, 'FO': 2, 'PU': 3, 'SFA': 4, 'FA': 5}
    return rank_order.get(rank, 6)  # 6 untuk nilai yang tidak dikenali

def process_data(df, menu_type):
    """Memproses data sesuai dengan menu yang dipilih"""
    processed_df = df.copy()
    
    # Konversi Departure Date Time (LT) ke datetime jika belum
    if 'Departure Date Time (LT)' in processed_df.columns:
        processed_df['Departure Date Time (LT)'] = pd.to_datetime(processed_df['Departure Date Time (LT)'], errors='coerce')
    
    # Filter berdasarkan menu
    if menu_type == "JT OUTGOING":
        # Hapus semua baris selain CGK
        processed_df = processed_df[processed_df['Dep Station'] == 'CGK']
        
    elif menu_type == "JT INCOMING":
        # Hapus semua baris dengan nilai CGK
        processed_df = processed_df[processed_df['Dep Station'] != 'CGK']
    
    # Untuk IW, IU, ID tidak ada filter khusus
    
    # Sorting untuk semua menu
    # Buat kolom helper untuk custom rank sorting
    processed_df['rank_sort_order'] = processed_df['Rank'].apply(custom_rank_sort)
    
    # Urutkan data
    processed_df = processed_df.sort_values([
        'Departure Date Time (LT)',
        'Flight',
        'Pairing Code',
        'rank_sort_order'
    ], ascending=[True, True, True, True])
    
    # Hapus kolom helper
    processed_df = processed_df.drop('rank_sort_order', axis=1)
    
    return processed_df

def convert_df_to_excel(df):
    """Konversi DataFrame ke Excel untuk download"""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Processed_Data', index=False)
    output.seek(0)
    return output

# Interface utama
st.sidebar.markdown("---")
st.sidebar.markdown("### 📁 Upload File")

# Upload file
uploaded_file = st.sidebar.file_uploader(
    "Choose a file", 
    type=['csv', 'xlsx', 'xls'],
    help="Upload file CSV atau Excel yang berisi data penerbangan"
)

if uploaded_file is not None:
    try:
        # Baca file - skip baris pertama, gunakan baris kedua sebagai header
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, skiprows=1)
        else:
            df = pd.read_excel(uploaded_file, skiprows=1)
        
        st.success(f"✅ File '{uploaded_file.name}' berhasil diupload!")
        
        # Validasi file
        is_valid, missing_columns = validate_file(df)
        
        if not is_valid:
            st.error("❌ File tidak sesuai format!")
            st.error(f"Kolom yang hilang: {', '.join(missing_columns)}")
            st.info("Kolom yang diperlukan:")
            for col in REQUIRED_COLUMNS:
                st.write(f"- {col}")
        else:
            st.success("✅ Format file valid!")
            
            # Tampilkan informasi dataset
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Baris", len(df))
            with col2:
                st.metric("Total Kolom", len(df.columns))
            with col3:
                st.metric("Menu Aktif", selected_menu)
            
            # Proses data
            processed_df = process_data(df, selected_menu)
            
            # Tampilkan hasil filtering
            st.markdown("---")
            st.subheader(f"📊 Hasil Pemrosesan: {selected_menu}")
            
            if len(processed_df) == 0:
                st.warning("⚠️ Tidak ada data yang sesuai dengan kriteria filtering.")
            else:
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Data Asli", len(df))
                with col2:
                    st.metric("Setelah Diproses", len(processed_df))
                
                # Preview data (10 baris teratas)
                st.subheader("👁️ Preview Data (10 baris teratas)")
                st.dataframe(processed_df.head(10), use_container_width=True)
                
                # Tombol download
                st.markdown("---")
                excel_data = convert_df_to_excel(processed_df)
                
                # Buat nama file dengan timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{selected_menu}_{timestamp}.xlsx"
                
                st.download_button(
                    label="📥 Download Excel",
                    data=excel_data.getvalue(),
                    file_name=filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    help="Download hasil pemrosesan dalam format Excel"
                )
                
                # Tampilkan statistik tambahan
                st.markdown("---")
                
                # Layout untuk statistik dalam 2 kolom
                stat_col1, stat_col2 = st.columns(2)
                
                # Statistik Rank
                if 'Rank' in processed_df.columns:
                    with stat_col1:
                        st.subheader("📈 Statistik Rank")
                        rank_counts = processed_df['Rank'].value_counts()
                        
                        # Urutkan berdasarkan custom order
                        rank_order = ['CPT', 'FO', 'PU', 'SFA', 'FA']
                        rank_counts = rank_counts.reindex([r for r in rank_order if r in rank_counts.index])
                        
                        # Chart
                        st.bar_chart(rank_counts, height=300)
                        
                        # Metrics dalam grid 2x3
                        metric_cols = st.columns(2)
                        for i, (rank, count) in enumerate(rank_counts.items()):
                            with metric_cols[i % 2]:
                                st.metric(f"Rank {rank}", count)
                
                # Statistik Stasiun
                if 'Dep Station' in processed_df.columns:
                    with stat_col2:
                        st.subheader("✈️ Statistik Stasiun")
                        
                        # Departure Stations
                        dep_counts = processed_df['Dep Station'].value_counts().head(10)
                        
                        # Chart
                        st.bar_chart(dep_counts, height=300)
                        
                        # Top 5 stations sebagai metrics
                        st.write("**Top 5 Departure Stations:**")
                        top_5_dep = dep_counts.head(5)
                        
                        # Buat grid 2 kolom untuk metrics
                        dep_metric_cols = st.columns(2)
                        for i, (station, count) in enumerate(top_5_dep.items()):
                            with dep_metric_cols[i % 2]:
                                st.metric(station, count)
                
                # Statistik Arrival Stations (jika kolom ada)
                if 'Arr Station' in processed_df.columns:
                    st.markdown("---")
                    st.subheader("🛬 Arrival Stations")
                    
                    arr_counts = processed_df['Arr Station'].value_counts().head(10)
                    
                    # Layout dalam 2 kolom
                    arr_col1, arr_col2 = st.columns([2, 1])
                    
                    with arr_col1:
                        st.bar_chart(arr_counts, height=300)
                    
                    with arr_col2:
                        st.write("**Top 5 Destinations:**")
                        for station, count in arr_counts.head(5).items():
                            st.metric(station, count)
                
                # Route Analysis (Origin-Destination pairs)
                if 'Dep Station' in processed_df.columns and 'Arr Station' in processed_df.columns:
                    st.markdown("---")
                    st.subheader("🛫➡️🛬 Route Analysis")
                    
                    # Buat route combinations
                    processed_df['Route'] = processed_df['Dep Station'] + ' → ' + processed_df['Arr Station']
                    route_counts = processed_df['Route'].value_counts().head(10)
                    
                    route_col1, route_col2 = st.columns([2, 1])
                    
                    with route_col1:
                        st.bar_chart(route_counts, height=300)
                    
                    with route_col2:
                        st.write("**Top 5 Routes:**")
                        for i, (route, count) in enumerate(route_counts.head(5).items(), 1):
                            st.write(f"{i}. **{route}**: {count} flights")
                
                # Summary Statistics
                st.markdown("---")
                st.subheader("📋 Summary Statistics")
                
                summary_cols = st.columns(4)
                
                with summary_cols[0]:
                    unique_dep = processed_df['Dep Station'].nunique() if 'Dep Station' in processed_df.columns else 0
                    st.metric("Unique Dep. Stations", unique_dep)
                
                with summary_cols[1]:
                    unique_arr = processed_df['Arr Station'].nunique() if 'Arr Station' in processed_df.columns else 0
                    st.metric("Unique Arr. Stations", unique_arr)
                
                with summary_cols[2]:
                    unique_flights = processed_df['Flight'].nunique() if 'Flight' in processed_df.columns else 0
                    st.metric("Unique Flights", unique_flights)
                
                with summary_cols[3]:
                    unique_routes = len(route_counts) if 'Dep Station' in processed_df.columns and 'Arr Station' in processed_df.columns else 0
                    st.metric("Unique Routes", unique_routes)
                
                # Tampilkan full data jika diminta
                if st.checkbox("🔍 Tampilkan semua data"):
                    st.subheader("📋 Data Lengkap")
                    st.dataframe(processed_df, use_container_width=True)
    
    except Exception as e:
        st.error(f"❌ Error membaca file: {str(e)}")
        st.info("Pastikan file dalam format yang benar dan tidak corrupt.")

else:
    # Tampilan ketika belum ada file
    st.info("👆 Silakan upload file CSV atau Excel di sidebar untuk memulai.")
    
    # Tampilkan informasi tentang menu
    st.markdown("---")
    st.subheader("ℹ️ Informasi Menu")
    
    menu_info = {
        "JT OUTGOING": {
            "description": "Filter data dengan Dep Station = 'CGK' saja",
            "filter": "Dep Station == 'CGK'",
            "sort": "Departure Date Time, Flight, Pairing Code, Rank (CPT→FO→PU→SFA→FA)"
        },
        "JT INCOMING": {
            "description": "Filter data dengan Dep Station ≠ 'CGK'",
            "filter": "Dep Station != 'CGK'",
            "sort": "Departure Date Time, Flight, Pairing Code, Rank (CPT→FO→PU→SFA→FA)"
        },
        "IW": {
            "description": "Tanpa filter Dep Station",
            "filter": "Tidak ada filter",
            "sort": "Departure Date Time, Flight, Pairing Code, Rank (CPT→FO→PU→SFA→FA)"
        },
        "IU": {
            "description": "Tanpa filter Dep Station",
            "filter": "Tidak ada filter",
            "sort": "Departure Date Time, Flight, Pairing Code, Rank (CPT→FO→PU→SFA→FA)"
        },
        "ID": {
            "description": "Filter: Hapus baris dengan Flight mengandung 'TAXI'",
            "filter": "Flight tidak mengandung 'TAXI' (case-insensitive)",
            "sort": "Departure Date Time, Flight, Pairing Code, Rank (CPT→FO→PU→SFA→FA)"
        }
    }
    
    for menu, info in menu_info.items():
        with st.expander(f"📋 {menu}"):
            st.write(f"**Deskripsi:** {info['description']}")
            st.write(f"**Filter:** {info['filter']}")
            st.write(f"**Sorting:** {info['sort']}")
    
    # Tampilkan kolom yang diperlukan
    st.markdown("---")
    st.subheader("📄 Kolom yang Diperlukan")
    for i, col in enumerate(REQUIRED_COLUMNS, 1):
        st.write(f"{i}. {col}")
    
    st.markdown("---")
    st.info("💡 **Tips:** Pastikan file Excel/CSV Anda memiliki semua kolom yang diperlukan di atas.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Flight Data Processing System | Built with Streamlit"
    "</div>", 
    unsafe_allow_html=True
)