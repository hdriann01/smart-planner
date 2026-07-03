import streamlit as st
import pandas as pd

from models.user import User
from models.enums import ActivityLevel

from planner.planner import Planner

from utils.formatter import (
    schedule_table,
    comparison_table,
    summary,
)

from utils.metrics import summary_metrics

from utils.charts import (
    calories_chart,
    fatigue_chart,
    workout_pie_chart,
    comparison_chart,
    execution_time_chart,
    fatigue_progress_chart,
)

from utils.score import ScheduleScorer


# ==========================================================
# KONFIGURASI HALAMAN
# ==========================================================

st.set_page_config(
    page_title="Smart Planner",
    page_icon="🏃",
    layout="wide",
    initial_sidebar_state="expanded",
)

planner = Planner()


# ==========================================================
# SESSION STATE
# ==========================================================

if "generated" not in st.session_state:
    st.session_state.generated = False

if "greedy_result" not in st.session_state:
    st.session_state.greedy_result = None

if "astar_result" not in st.session_state:
    st.session_state.astar_result = None

if "best_result" not in st.session_state:
    st.session_state.best_result = None

if "greedy_score" not in st.session_state:
    st.session_state.greedy_score = 0.0

if "astar_score" not in st.session_state:
    st.session_state.astar_score = 0.0

if "user" not in st.session_state:
    st.session_state.user = None


# ==========================================================
# HEADER
# ==========================================================

st.title("🏃 Sistem Smart Planner Rutinitas Kebugaran Mingguan")

st.markdown(
    """
### Sistem Rekomendasi Jadwal Olahraga Mingguan

Aplikasi ini menyusun jadwal olahraga mingguan secara otomatis
menggunakan kombinasi:

- Rule-Based System (Forward Chaining)
- Greedy Best First Search
- A* Search

Setelah kedua algoritma dijalankan, sistem akan membandingkan
hasilnya dan memberikan rekomendasi jadwal terbaik.
"""
)

st.divider()


# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("👤 Profil Pengguna")

with st.sidebar.form("planner_form"):

    st.markdown("### Data Pengguna")

    nama = st.text_input(
        "Nama",
        value="Hadrian",
    )

    umur = st.number_input(
        "Umur",
        min_value=10,
        max_value=80,
        value=20,
    )

    berat = st.number_input(
        "Berat Badan (kg)",
        min_value=30.0,
        max_value=200.0,
        value=65.0,
    )

    tinggi = st.number_input(
        "Tinggi Badan (cm)",
        min_value=120.0,
        max_value=220.0,
        value=170.0,
    )

    tingkat_aktivitas = st.selectbox(
        "Tingkat Aktivitas",
        list(ActivityLevel),
        format_func=lambda level:
        level.name.replace("_", " ").title(),
    )

    target_kalori = st.number_input(
        "Target Kalori Mingguan",
        min_value=500,
        max_value=10000,
        value=2500,
        step=100,
    )

    durasi_maksimal = st.slider(
        "Durasi Maksimal per Hari (Menit)",
        min_value=15,
        max_value=120,
        value=60,
        step=5,
    )

    st.markdown("---")

    submitted = st.form_submit_button(
        "🚀 Buat Jadwal",
        use_container_width=True,
    )


# ==========================================================
# AREA KONTEN UTAMA
# ==========================================================

main_container = st.container()
# ==========================================================
# PROSES PEMBUATAN JADWAL
# ==========================================================

if submitted:

    try:

        # --------------------------------------------------
        # Membuat objek User
        # --------------------------------------------------

        user = User(
            id=1,
            name=nama,
            age=umur,
            weight=berat,
            height=tinggi,
            activity_level=tingkat_aktivitas,
            target_calories=target_kalori,
            max_duration=durasi_maksimal,
        )

        st.session_state.user = user

        # --------------------------------------------------
        # Menjalankan Planner
        # --------------------------------------------------

        with st.spinner("⏳ Sedang menyusun jadwal olahraga mingguan..."):

            greedy_result = planner.run_greedy(user)

            astar_result = planner.run_astar(user)

        # --------------------------------------------------
        # Menghitung skor masing-masing algoritma
        # --------------------------------------------------

        greedy_score = ScheduleScorer.calculate(
            user,
            greedy_result,
        )

        astar_score = ScheduleScorer.calculate(
            user,
            astar_result,
        )

        # --------------------------------------------------
        # Memilih hasil terbaik
        # --------------------------------------------------

        best_result = ScheduleScorer.compare(
            user,
            greedy_result,
            astar_result,
        )

        # --------------------------------------------------
        # Menyimpan hasil ke Session State
        # --------------------------------------------------

        st.session_state.greedy_result = greedy_result
        st.session_state.astar_result = astar_result
        st.session_state.best_result = best_result

        st.session_state.greedy_score = greedy_score
        st.session_state.astar_score = astar_score

        st.session_state.generated = True

        # --------------------------------------------------
        # Pesan sukses
        # --------------------------------------------------

        if best_result.algorithm.upper() == "ASTAR":

            algoritma = "A* Search"

        elif best_result.algorithm.upper() == "GREEDY":

            algoritma = "Greedy Best First Search"

        else:

            algoritma = best_result.algorithm

        st.success(
            f"""
✅ Jadwal olahraga berhasil dibuat.

Sistem telah menjalankan **Greedy Best First Search**
dan **A* Search**, kemudian membandingkan keduanya.

**Algoritma yang direkomendasikan: {algoritma}**
"""
        )

    except Exception as error:

        st.session_state.generated = False

        st.error(
            f"""
❌ Terjadi kesalahan saat membuat jadwal.

Detail kesalahan:

{error}
"""
        )

        # ==========================================================
# DASHBOARD HASIL
# ==========================================================

if st.session_state.generated:

    result = st.session_state.best_result
    user = st.session_state.user

    score = ScheduleScorer.calculate(
        user,
        result,
    )

    metrics = summary_metrics(
        user,
        result,
    )

    with main_container:

        st.divider()

        # ==================================================
        # KARTU REKOMENDASI
        # ==================================================

        st.subheader("🏆 Jadwal Mingguan yang Direkomendasikan")

        if result.algorithm.upper() == "ASTAR":
            algoritma = "A* Search"

        elif result.algorithm.upper() == "GREEDY":
            algoritma = "Greedy Best First Search"

        else:
            algoritma = result.algorithm

        st.success(
            f"""
### ✅ Jadwal Berhasil Dibuat

**Algoritma Terbaik : {algoritma}**

**Skor Akhir : {score:.2f}/100**

Sistem telah mengevaluasi hasil Greedy Best First Search dan
A* Search, kemudian memilih jadwal terbaik berdasarkan
hasil evaluasi.
"""
        )

        # ==================================================
        # METRIC CARD
        # ==================================================

        st.subheader("📌 Ringkasan Hasil")

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "🔥 Total Kalori",
                f"{result.total_calories} kkal",
            )

        with col2:

            st.metric(
                "💪 Total Kelelahan",
                result.total_fatigue,
            )

        with col3:

            st.metric(
                "🏃 Hari Latihan",
                result.total_workout_days(),
            )

        with col4:

            st.metric(
                "⭐ Skor Akhir",
                f"{score:.2f}",
            )

        st.divider()

        # ==================================================
        # JADWAL MINGGUAN
        # ==================================================

        st.subheader("📅 Jadwal Olahraga Mingguan")

        schedule_df = pd.DataFrame(
            schedule_table(result)
        )

        schedule_df = schedule_df.rename(
            columns={
                "Day": "Hari",
                "Activity": "Aktivitas",
                "Duration (min)": "Durasi (Menit)",
                "Calories": "Kalori",
                "Fatigue": "Kelelahan",
                "Intensity": "Intensitas",
            }
        )

        st.dataframe(
            schedule_df,
            use_container_width=True,
            hide_index=True,
        )

        st.divider()

        # ==================================================
        # RINGKASAN STATISTIK
        # ==================================================

        st.subheader("📊 Ringkasan Statistik")

        metric_df = pd.DataFrame(
            metrics.items(),
            columns=[
                "Metrik",
                "Nilai",
            ],
        )

        metric_df["Metrik"] = metric_df["Metrik"].replace({

            "Target Achievement (%)":
                "Pencapaian Target (%)",

            "Average Calories":
                "Rata-rata Kalori",

            "Average Fatigue":
                "Rata-rata Kelelahan",

            "Workout Ratio (%)":
                "Persentase Hari Latihan",

            "Rest Ratio (%)":
                "Persentase Hari Istirahat",

            "Efficiency (%)":
                "Efisiensi Jadwal (%)",

            "Remaining Calories":
                "Sisa Target Kalori",

            "Fatigue Utilization (%)":
                "Penggunaan Fatigue (%)",
        })

        st.dataframe(
            metric_df,
            use_container_width=True,
            hide_index=True,
        )

        st.info(
            """
💡 **Keterangan**

Ringkasan statistik digunakan untuk mengevaluasi kualitas
jadwal olahraga yang dihasilkan berdasarkan target kalori,
tingkat kelelahan, efisiensi jadwal, serta distribusi hari
latihan dan hari istirahat.
"""
        )
                # ==================================================
        # PERBANDINGAN ALGORITMA
        # ==================================================

        st.divider()

        st.subheader("⚖️ Perbandingan Algoritma")

        comparison_df = pd.DataFrame(
            comparison_table(
                st.session_state.greedy_result,
                st.session_state.astar_result,
            )
        )

        comparison_df = comparison_df.rename(
            columns={
                "Algorithm": "Algoritma",
                "Calories": "Total Kalori",
                "Fatigue": "Total Kelelahan",
                "Workout Days": "Hari Latihan",
                "Rest Days": "Hari Istirahat",
                "Expanded Nodes": "Node Diekspansi",
                "Execution Time (s)": "Waktu Eksekusi (detik)",
            }
        )

        st.dataframe(
            comparison_df,
            use_container_width=True,
            hide_index=True,
        )

        st.info(
            """
Tabel di atas memperlihatkan hasil yang diperoleh dari
Greedy Best First Search dan A* Search sehingga pengguna
dapat membandingkan performa kedua algoritma.
"""
        )

        # ==================================================
        # SKOR ALGORITMA
        # ==================================================

        st.divider()

        st.subheader("🏅 Evaluasi Algoritma")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Greedy Best First Search",
                f"{st.session_state.greedy_score:.2f}",
            )

        with col2:

            st.metric(
                "A* Search",
                f"{st.session_state.astar_score:.2f}",
            )

        # ==================================================
        # VISUALISASI
        # ==================================================

        st.divider()

        st.subheader("📈 Visualisasi Hasil")

        grafik1, grafik2 = st.columns(2)

        with grafik1:

            st.plotly_chart(
                calories_chart(result),
                use_container_width=True,
            )

        with grafik2:

            st.plotly_chart(
                fatigue_chart(result),
                use_container_width=True,
            )

        grafik3, grafik4 = st.columns(2)

        with grafik3:

            st.plotly_chart(
                workout_pie_chart(result),
                use_container_width=True,
            )

        with grafik4:

            st.plotly_chart(
                fatigue_progress_chart(result),
                use_container_width=True,
            )

        st.plotly_chart(
            comparison_chart(
                st.session_state.greedy_result,
                st.session_state.astar_result,
            ),
            use_container_width=True,
        )

        st.plotly_chart(
            execution_time_chart(
                st.session_state.greedy_result,
                st.session_state.astar_result,
            ),
            use_container_width=True,
        )

        # ==================================================
        # TENTANG SISTEM
        # ==================================================

        st.divider()

        st.subheader("ℹ️ Tentang Sistem")

        st.info(
            """
### Smart Planner System

Smart Planner System merupakan aplikasi berbasis
Kecerdasan Buatan (Artificial Intelligence) yang
digunakan untuk menyusun jadwal rutinitas kebugaran
mingguan secara otomatis.

Metode yang digunakan dalam sistem ini meliputi:

✅ Rule-Based System (Forward Chaining)

✅ Greedy Best First Search

✅ A* Search

Rule-Based System digunakan untuk melakukan validasi
dan penyaringan aktivitas olahraga sesuai kondisi
pengguna.

Selanjutnya Greedy Best First Search dan A* Search
digunakan untuk menghasilkan jadwal olahraga yang
optimal berdasarkan target kalori, durasi latihan,
dan tingkat kelelahan.

Hasil kedua algoritma kemudian dibandingkan sehingga
sistem dapat memberikan rekomendasi jadwal terbaik.
"""
        )

        # ==================================================
        # FOOTER
        # ==================================================

        st.divider()

        st.caption(
            "Smart Planner System © 2026 | "
            "Implementasi Rule-Based System dan Heuristic Search "
            "pada Smart Planner System Rutinitas Kebugaran Mingguan"
        )