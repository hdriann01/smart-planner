import streamlit as st
import pandas as pd

from models.user import User
from models.enums import ActivityLevel

from planner.planner import Planner

from utils.formatter import schedule_table

from utils.metrics import summary_metrics

from utils.charts import (
    calories_chart,
    fatigue_chart,
    workout_pie_chart,
    fatigue_progress_chart,
)

from utils.score import ScheduleScorer


st.set_page_config(
    page_title="RUSH",
    page_icon="🏃",
    layout="wide",
    initial_sidebar_state="expanded",
)

planner = Planner()


if "generated" not in st.session_state:
    st.session_state.generated = False

if "best_result" not in st.session_state:
    st.session_state.best_result = None

if "user" not in st.session_state:
    st.session_state.user = None


st.title("✨ Temukan Jadwal Olahraga Terbaik untuk Anda")

st.markdown(
    """
### Rekomendasi Jadwal Olahraga Mingguan

Selamat datang di **RUSH**.

Aplikasi ini membantu Anda menyusun jadwal olahraga mingguan yang sesuai dengan kondisi tubuh dan target kebugaran yang ingin dicapai.

Silakan lengkapi data pada panel di sebelah kiri, kemudian tekan tombol **Buat Jadwal** untuk memperoleh rekomendasi jadwal olahraga terbaik.
"""
)

st.divider()


st.sidebar.title("👤 Profil Pengguna")

with st.sidebar.form("planner_form"):

    st.markdown("### Data Pengguna")

    nama = st.text_input(
        "Nama",
        placeholder="Masukkan nama Anda",
    )

    umur = st.number_input(
        "Umur",
        min_value=10,
        max_value=80,
        value=None,
        placeholder="Contoh: 25",
    )

    berat = st.number_input(
        "Berat Badan (kg)",
        min_value=30.0,
        max_value=200.0,
        value=None,
        placeholder="Contoh: 65",
    )

    tinggi = st.number_input(
        "Tinggi Badan (cm)",
        min_value=120.0,
        max_value=220.0,
        value=None,
        placeholder="Contoh: 170",
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
        value=None,
        placeholder="Contoh: 2500",
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


main_container = st.container()

if submitted:

    try:

        if not nama.strip():

            st.warning("Silakan masukkan nama Anda.")

            st.stop()

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

        with st.spinner("⏳ Sedang menyusun jadwal olahraga terbaik..."):

            greedy_result = planner.run_greedy(user)

            astar_result = planner.run_astar(user)

            best_result = ScheduleScorer.compare(
                user,
                greedy_result,
                astar_result,
            )

        st.session_state.best_result = best_result

        st.session_state.generated = True

        st.success(
            """
### 🎉 Jadwal Olahraga Berhasil Dibuat

Sistem telah menyusun jadwal olahraga mingguan berdasarkan profil dan target kebugaran yang Anda masukkan.

Silakan lihat rekomendasi jadwal pada bagian di bawah.
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

        st.success(
            """
## 🎉 Jadwal Olahraga Anda Siap!

Berikut merupakan rekomendasi jadwal olahraga mingguan yang telah disusun berdasarkan data dan target kebugaran yang Anda masukkan.

Semoga jadwal ini dapat membantu Anda mencapai target kebugaran secara lebih terarah dan konsisten.
"""
        )

        st.subheader("📌 Ringkasan Jadwal")

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
                "🛌 Hari Istirahat",
                result.total_rest_days(),
            )

        st.divider()

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
                "Pencapaian Target",

            "Average Calories":
                "Rata-rata Kalori",

            "Average Fatigue":
                "Rata-rata Kelelahan",

            "Workout Ratio (%)":
                "Persentase Hari Latihan",

            "Rest Ratio (%)":
                "Persentase Hari Istirahat",

            "Efficiency (%)":
                "Efisiensi Jadwal",

            "Remaining Calories":
                "Sisa Target Kalori",

            "Fatigue Utilization (%)":
                "Penggunaan Kelelahan",
        })

        st.dataframe(
            metric_df,
            use_container_width=True,
            hide_index=True,
        )

        st.info(
            """
📌 **Informasi**

Ringkasan statistik memberikan gambaran mengenai hasil jadwal olahraga yang telah disusun, mulai dari pencapaian target kalori, tingkat kelelahan, hingga keseimbangan antara hari latihan dan hari istirahat.
"""
        )

        st.divider()

        st.subheader("📈 Visualisasi Jadwal")

        st.markdown(
            """
Visualisasi berikut memberikan gambaran mengenai hasil
jadwal olahraga yang telah direkomendasikan sehingga
lebih mudah dipahami.
"""
        )

        col1, col2 = st.columns(2)

        with col1:

            st.plotly_chart(
                calories_chart(result),
                use_container_width=True,
            )

        with col2:

            st.plotly_chart(
                fatigue_chart(result),
                use_container_width=True,
            )

        col3, col4 = st.columns(2)

        with col3:

            st.plotly_chart(
                workout_pie_chart(result),
                use_container_width=True,
            )

        with col4:

            st.plotly_chart(
                fatigue_progress_chart(result),
                use_container_width=True,
            )

        st.divider()

        st.success(
            """
### 🎯 Tetap Konsisten Berolahraga

Jadwal yang dihasilkan merupakan rekomendasi yang
disesuaikan dengan data yang Anda masukkan.

Lakukan olahraga secara bertahap, konsisten,
dan sesuaikan intensitas latihan dengan kondisi tubuh
agar target kebugaran dapat tercapai secara optimal.
"""
        )

st.divider()

st.caption(
    "© 2026 RUSH | Sistem Rekomendasi Rutinitas Kebugaran Mingguan"
)