import streamlit as st

# ------------------------
# FUNGSI FUZZY MEMBERSHIP
# ------------------------
def rumah_kecil(x): return max(min((75 - x) / 50, 1), 0)  # aktif dari 0 sampai 75
def rumah_sedang(x): return max(min((x - 50) / 50, (150 - x) / 50), 0)  # aktif dari 50 sampai 150
def rumah_besar(x): return max(min((x - 125) / 75, 1), 0)  # aktif dari 125 sampai 250


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
# PREDIKSI BIAYA DENGAN FIS SUGENO ORDE 1
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
                μ_r = r_func(luas_rumah)
                μ_a = a_func(jumlah_alat)
                μ_d = d_func(daya_digunakan)
                w = μ_r * μ_a * μ_d

                # Output linear Sugeno orde 1: gabungan berbobot dari masing-masing fitur
                z = (μ_r * luas_rumah * 0.05 + μ_a * jumlah_alat * 2 + μ_d * daya_digunakan) * tarif
                μ.append((w, z))

    numerator = sum(w * z for w, z in μ)
    denominator = sum(w for w, _ in μ)
    return numerator / denominator if denominator != 0 else 0

# ------------------------
# STREAMLIT APP
# ------------------------

st.title("💸 Cek Perkiraan Tagihan Listrik Anda, Sebelum Kaget di Akhir Bulan!🔌 ")
st.markdown("""
<div style='background-color:#f0f8ff; padding:20px; border-radius:10px'>
    <h4 style='color:#1e90ff;'>🔍 Penasaran berapa kira-kira biaya listrik di rumah kamu tiap bulan?</h4>
    <p style='color:#333333; font-size:16px;'>
    Sekarang nggak perlu tebak-tebakan lagi!<br><br>
    Web ini bantu kamu <b>menghitung estimasi tagihan listrik bulanan</b> dengan cepat, cukup dari 
    <b>luas rumah</b>, <b>jumlah alat elektronik</b>, dan <b>pemakaian listrik (kWh)</b> yang kamu isi.<br><br>
    Sistem kami pakai <b style='color:#ff4500;'>logika fuzzy Sugeno</b>, jadi hasilnya tetap realistis dan menyesuaikan dengan tarif PLN terbaru.<br><br>
    Cocok banget buat:
    <ul style='margin-top:0;'>
        <li>Kamu yang lagi ngatur keuangan rumah tangga</li>
        <li>Pemilik kost atau kontrakan</li>
        <li>Siapa pun yang mau tahu konsumsi listrik rumahnya</li>
    </ul>
    Yuk coba sekarang, isi datanya dan lihat <b style='color:#2e8b57;'>berapa tagihan listrikmu seandainya dihitung hari ini!</b> ⚡
    </p>
</div>
""", unsafe_allow_html=True)

# Input Luas Rumah
luas_rumah = st.number_input("🏠 Luas Rumah (m²)", min_value=0.0, max_value=250.0, value=100.0)
st.caption("Masukkan luas rumah antara 0 hingga 250 meter persegi.")

# Input Jumlah Alat
jumlah_alat = st.number_input("📺 Jumlah Alat Elektronik", min_value=0, max_value=25, value=10)
st.caption("Masukkan total alat elektronik utama di rumah, antara 0 hingga 25 alat.")

# Input Daya Digunakan
daya_digunakan = st.number_input("⚡ Daya Digunakan per Bulan (kWh)", min_value=0.0, max_value=2000.0, value=150.0)
st.caption("Masukkan estimasi penggunaan listrik per bulan dalam kWh (maksimum 2000 kWh).")

# Selectbox Daya Terpasang
daya_terpasang = st.selectbox("🔌 Daya Terpasang (VA)", options=[900, 1300, 2200, 3500, 5500, 6600], index=0)
st.caption("Pilih daya terpasang sesuai golongan tarif PLN rumah Anda.")

# Tombol Prediksi
if st.button("🔍 Hitung Biaya Listrik"):
    hasil = prediksi_biaya_listrik(luas_rumah, jumlah_alat, daya_digunakan, daya_terpasang)
    st.success(f"💡 Estimasi biaya listrik bulanan: **Rp {hasil:,.2f}**")
