import streamlit as st

# ------------------------
# FUNGSI FUZZY MEMBERSHIP
# ------------------------
def rumah_kecil(x): return max(min((50 - x) / 25, 1), 0)
def rumah_sedang(x): return max(min((x - 30) / 35, (100 - x) / 35), 0)
def rumah_besar(x): return max(min((x - 80) / 85, 1), 0)

def daya_ringan(x): return max(min((500 - x) / 200, 1), 0)
def daya_sedang(x): return max(min((x - 300) / 200, (1000 - x) / 200), 0)
def daya_berat(x): return max(min((x - 800) / 200, 1), 0)

def alat_sedikit(x): return max(min((5 - x) / 4, 1), 0)
def alat_sedang(x): return max(min((x - 3) / 4, (10 - x) / 5), 0)
def alat_banyak(x): return max(min((x - 8) / 10, 1), 0)

# ------------------------
# TARIF PLN BERDASARKAN DAYA TERPASANG
# ------------------------
def get_tarif(daya_terpasang_va):
    if daya_terpasang_va == 900:
        return 1352.00
    elif 1300 <= daya_terpasang_va <= 2200:
        return 1444.70
    elif 3500 <= daya_terpasang_va <= 5500:
        return 1699.53
    elif daya_terpasang_va >= 6600:
        return 1699.53
    else:
        return 1444.70  # default

# ------------------------
# FUNGSI OUTPUT SUGENO ORDE-1
# ------------------------
def rule_output(luas, alat, daya_digunakan, tarif):
    kwh_luas = luas * 1.5
    kwh_alat = alat * 2
    kwh_daya = daya_digunakan * 1.8
    total_kwh = kwh_luas + kwh_alat + kwh_daya
    return total_kwh * tarif

# ------------------------
# PREDIKSI BIAYA DENGAN FIS SUGENO
# ------------------------
def prediksi_biaya_listrik(luas_rumah, jumlah_alat, daya_digunakan, daya_terpasang_va):
    tarif = get_tarif(daya_terpasang_va)
    μ = []
    rumah_f = [rumah_kecil, rumah_sedang, rumah_besar]
    alat_f = [alat_sedikit, alat_sedang, alat_banyak]
    daya_f = [daya_ringan, daya_sedang, daya_berat]

    for r_func in rumah_f:
        for a_func in alat_f:
            for d_func in daya_f:
                w = r_func(luas_rumah) * a_func(jumlah_alat) * d_func(daya_digunakan)
                z = rule_output(luas_rumah, jumlah_alat, daya_digunakan, tarif)
                μ.append((w, z))

    numerator = sum(w * z for w, z in μ)
    denominator = sum(w for w, _ in μ)
    return numerator / denominator if denominator != 0 else 0

# ------------------------
# STREAMLIT APP
# ------------------------

st.title("🔌 Prediksi Biaya Listrik dengan Fuzzy Sugeno")
st.markdown("""
Aplikasi ini menggunakan sistem logika fuzzy Sugeno orde-1 untuk memperkirakan biaya listrik bulanan berdasarkan beberapa parameter:

- **Luas Rumah (m²)**: antara 0 hingga 250 m²
- **Jumlah Alat Elektronik**: antara 0 hingga 25
- **Daya Digunakan (kWh)**: total pemakaian bulanan
- **Daya Terpasang (VA)**: memilih dari golongan tarif PLN

Silakan isi parameter berikut untuk menghitung estimasi biaya listrik Anda.
""")

# Input pengguna
luas_rumah = st.number_input("🏠 Luas Rumah (m²)", min_value=0.0, max_value=250.0, value=100.0)
jumlah_alat = st.number_input("📺 Jumlah Alat Elektronik", min_value=0, max_value=25, value=10)
daya_digunakan = st.number_input("⚡ Daya Digunakan per Bulan (kWh)", min_value=0.0, value=300.0)

# Selectbox daya terpasang
daya_terpasang = st.selectbox("🔌 Daya Terpasang (VA)", options=[900, 1300, 2200, 3500, 5500, 6600], index=1)

# Tombol prediksi
if st.button("Hitung Biaya Listrik"):
    hasil = prediksi_biaya_listrik(luas_rumah, jumlah_alat, daya_digunakan, daya_terpasang)
    st.success(f"💡 Estimasi biaya listrik bulanan: **Rp {hasil:,.2f}**")

