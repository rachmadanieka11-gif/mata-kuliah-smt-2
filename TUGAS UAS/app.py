#Frontend: Antarmuka Streamlit untuk Seat Booking Bus Pariwisata dengan Suara
# Versi Final - Lengkap dengan Semua Fitur

import streamlit as st
import pandas as pd
from logictiket import BusSeatCircularList
from gtts import gTTS
import tempfile
import os
import time

st.set_page_config(
    page_title="Travel Seat Center", 
    layout="centered",
    page_icon="🚌"
)

# ========== KELAS MANAJEMEN SUARA ==========
class VoiceManager:
    """Manajemen suara - versi sederhana dengan st.audio"""
    
    def __init__(self):
        self.mute = False
        self.last_audio = None
        self.last_audio_time = 0
        
    def text_to_speech_bytes(self, text, language='id'):
        """Konversi teks ke bytes audio (untuk st.audio)"""
        if self.mute or not text:
            return None
        
        # Cegah duplikat suara yang sama dalam 2 detik
        current_time = time.time()
        if self.last_audio == text and (current_time - self.last_audio_time) < 2:
            return None
            
        try:
            # Generate suara
            tts = gTTS(text=text, lang=language, slow=False)
            
            # Simpan ke temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                temp_path = fp.name
            
            tts.save(temp_path)
            
            # Baca file
            with open(temp_path, 'rb') as fp:
                audio_bytes = fp.read()
            
            # Hapus file
            os.unlink(temp_path)
            
            # Update cache
            self.last_audio = text
            self.last_audio_time = current_time
            
            return audio_bytes
        except Exception as e:
            st.error(f"Error generating voice: {e}")
            return None
    
    def get_welcome_audio(self):
        return self.text_to_speech_bytes("Selamat datang di sistem pemesanan tiket PesonaTour.")
    
    def get_seat_info_audio(self, nomor, posisi, status, nama=None):
        """Informasi kursi - suara yang natural"""
        # Ekstrak nomor saja (hapus kata "Kursi" dari string)
        nomor_clean = nomor.replace("Kursi ", "")
        if status == "Tersedia":
            teks = f"Nomor {nomor_clean}, {posisi}, tersedia"
        else:
            teks = f"Nomor {nomor_clean}, {posisi}, sudah dipesan oleh {nama}"
        return self.text_to_speech_bytes(teks)
    
    def get_booking_success_audio(self, nomor, nama):
        nomor_clean = nomor.replace("Kursi ", "")
        teks = f"Nomor {nomor_clean} berhasil dipesan untuk {nama}"
        return self.text_to_speech_bytes(teks)
    
    def get_booking_error_audio(self):
        return self.text_to_speech_bytes("Mohon isi nama penumpang terlebih dahulu")
    
    def get_cancel_success_audio(self, nomor):
        nomor_clean = nomor.replace("Kursi ", "")
        teks = f"Pemesanan nomor {nomor_clean} telah dibatalkan"
        return self.text_to_speech_bytes(teks)
    
    def get_test_audio(self):
        return self.text_to_speech_bytes("Suara berfungsi dengan baik")

# ========== INISIALISASI ==========
if "bus_pariwisata" not in st.session_state:
    st.session_state.bus_pariwisata = BusSeatCircularList(jumlah_kursi=12)

if "voice_manager" not in st.session_state:
    st.session_state.voice_manager = VoiceManager()

bus = st.session_state.bus_pariwisata
vm = st.session_state.voice_manager

# Fungsi untuk memutar audio
def play_audio(audio_bytes):
    if audio_bytes and not vm.mute:
        st.audio(audio_bytes, format='audio/mp3')

# ========== TAMPILAN UTAMA ==========
st.title("🚌 PesonaTour: Sistem Pemilihan Kursi Travel")
st.markdown("### ✨ Dengan Panduan Suara Interaktif ✨")
st.markdown("*Aplikasi kasir pemesanan tiket agen pariwisata menggunakan User-Defined Circular Linked List*")

# Sidebar untuk kontrol suara
with st.sidebar:
    st.header("🎵 Kontrol Suara")
    
    # Tombol mute/unmute
    if vm.mute:
        if st.button("🔊 Aktifkan Suara", use_container_width=True):
            vm.mute = False
            st.rerun()
    else:
        if st.button("🔇 Matikan Suara", use_container_width=True):
            vm.mute = True
            st.rerun()
    
    # Tombol test suara
    if not vm.mute:
        if st.button("🔊 Test Suara", use_container_width=True):
            test_audio = vm.get_test_audio()
            if test_audio:
                play_audio(test_audio)
                st.success("✅ Test suara diputar!")
            else:
                st.error("❌ Gagal menghasilkan suara. Cek koneksi internet.")
    
    st.divider()
    st.caption("💡 **Tips:**")
    st.caption("1. Pastikan volume komputer tidak mute")
    st.caption("2. Klik tombol ▶️ Play di audio player")
    st.caption("3. Koneksi internet diperlukan untuk suara (gTTS)")
    
    st.divider()
    if st.button("🔄 Reset Semua Kursi", use_container_width=True):
        bus.reset_all_seats()
        st.success("✅ Semua kursi telah direset!")
        st.rerun()

# Welcome audio (manual)
if not vm.mute:
    st.info("🎵 **Selamat Datang!** Klik tombol di bawah untuk mendengar sambutan:")
    if st.button("🔊 Putar Sambutan", use_container_width=True):
        welcome_audio = vm.get_welcome_audio()
        if welcome_audio:
            play_audio(welcome_audio)

st.markdown("---")

# ========== BAGIAN 1: MONITOR KURSI ==========
st.subheader("🔎 Penelusuran Nomor Kursi")

# Tampilkan info kursi saat ini
current_info = bus.get_current_seat_info()

if current_info:
    # Tampilkan visual kursi yang lebih baik
    col_info, col_play, col_status = st.columns([3, 1, 1])
    with col_info:
        if current_info["status"] == "Tersedia":
            st.success(f"💺 **{current_info['nomor']}**")
            st.caption(f"📍 {current_info['posisi']}")
        else:
            st.error(f"💺 **{current_info['nomor']}**")
            st.caption(f"📍 {current_info['posisi']}")
    
    with col_status:
        if current_info["status"] == "Tersedia":
            st.markdown("### ✅ TERSEDIA")
        else:
            st.markdown("### ❌ DIPESAN")
            st.caption(f"👤 {current_info['nama']}")
    
    with col_play:
        if not vm.mute and st.button("🔊 Info Kursi", key="info_current", use_container_width=True):
            audio = vm.get_seat_info_audio(
                current_info["nomor"], 
                current_info["posisi"], 
                current_info["status"],
                current_info.get("nama")
            )
            if audio:
                play_audio(audio)

# Tombol navigasi
st.markdown("### 🔎 Navigasi Kursi")
col_next, col_prev, col_refresh = st.columns(3)

with col_next:
    if st.button("⏭️ Kursi Selanjutnya", use_container_width=True):
        bus.geser_ke_kursi_berikutnya()
        new_info = bus.get_current_seat_info()
        if new_info and not vm.mute:
            audio = vm.get_seat_info_audio(
                new_info["nomor"], 
                new_info["posisi"], 
                new_info["status"],
                new_info.get("nama")
            )
            if audio:
                play_audio(audio)
        st.rerun()

with col_prev:
    if st.button("⏪ Kursi Sebelumnya", use_container_width=True):
        bus.geser_ke_kursi_sebelumnya()
        new_info = bus.get_current_seat_info()
        if new_info and not vm.mute:
            audio = vm.get_seat_info_audio(
                new_info["nomor"], 
                new_info["posisi"], 
                new_info["status"],
                new_info.get("nama")
            )
            if audio:
                play_audio(audio)
        st.rerun()

with col_refresh:
    if st.button("🔄 Refresh Tampilan", use_container_width=True):
        st.rerun()

st.divider()

# ========== BAGIAN BOOKING ==========
st.subheader("📝 Pemesanan & Pembatalan")

col_book, col_cancel = st.columns(2)

with col_book:
    st.markdown("### 🎟️ Pesan Kursi")
    if current_info and current_info["status"] == "Tersedia":
        nama_input = st.text_input("✍️ Nama Penumpang:", key="input_nama", 
                                  placeholder="Masukkan nama lengkap (min. 3 karakter)")
        
        col_book_btn, col_play_book = st.columns([3, 1])
        with col_book_btn:
            if st.button("✅ Booking Kursi Ini", type="primary", use_container_width=True):
                if nama_input and len(nama_input.strip()) >= 3:
                    if bus.pesan_kursi_aktif(nama_input.strip()):
                        st.success(f"✅ {current_info['nomor']} berhasil dipesan untuk {nama_input}!")
                        audio = vm.get_booking_success_audio(current_info['nomor'], nama_input)
                        if audio:
                            play_audio(audio)
                        st.rerun()
                    else:
                        st.error("❌ Gagal memesan kursi!")
                else:
                    st.warning("⚠️ Silakan isi nama penumpang (minimal 3 karakter)!")
                    audio = vm.get_booking_error_audio()
                    if audio:
                        play_audio(audio)
        
        with col_play_book:
            if not vm.mute and st.button("🔊", key="play_book", help="Dengar suara"):
                if nama_input and len(nama_input.strip()) >= 3:
                    audio = vm.get_booking_success_audio(current_info['nomor'], nama_input)
                else:
                    audio = vm.get_booking_error_audio()
                if audio:
                    play_audio(audio)
    else:
        st.info("🚫 Kursi sudah terisi, silakan pilih kursi lain")

with col_cancel:
    st.markdown("### ❌ Batalkan Tiket")
    if current_info and current_info["status"] == "Dipesan":
        st.warning(f"⚠️ Kursi {current_info['nomor']} sedang dipesan oleh:")
        st.caption(f"👤 **{current_info['nama']}**")
        
        col_cancel_btn, col_play_cancel = st.columns([3, 1])
        with col_cancel_btn:
            if st.button("🗑️ Batalkan Tiket", use_container_width=True):
                nomor_kursi = current_info['nomor']
                if bus.batalkan_kursi_aktif():
                    st.warning(f"🔄 Tiket {nomor_kursi} telah dibatalkan")
                    audio = vm.get_cancel_success_audio(nomor_kursi)
                    if audio:
                        play_audio(audio)
                    st.rerun()
        
        with col_play_cancel:
            if not vm.mute and st.button("🔊", key="play_cancel", help="Dengar suara"):
                audio = vm.get_cancel_success_audio(current_info['nomor'])
                if audio:
                    play_audio(audio)
    else:
        st.info("✅ Kursi saat ini belum dipesan, tidak ada yang bisa dibatalkan")

st.markdown("---")

# ========== BAGIAN 2: MANIFES DAN STATISTIK ==========
st.subheader("📋 Manifes Seluruh Penumpang")

manifes_data = bus.dapatkan_manifes_bus()

if manifes_data:
    df = pd.DataFrame(manifes_data)
    
    total_terisi = len(df[df["Status"] == "Dipesan"])
    sisa_kursi = bus.total_kursi - total_terisi
    persentase = (total_terisi / bus.total_kursi) * 100
    
    # Statistik dengan metric yang lebih baik
    col_terisi, col_sisa, col_persen = st.columns(3)
    with col_terisi:
        st.metric("🎫 Kursi Terjual", f"{total_terisi} Tiket")
    with col_sisa:
        st.metric("💺 Sisa Kursi", f"{sisa_kursi} Kursi")
    with col_persen:
        st.metric("📊 Okupansi", f"{persentase:.0f}%")
    
    # Progress bar visual
    st.progress(persentase / 100)
    
    # Tabel manifest - tampilan bersih
    display_df = df.copy()
    if "Navigasi" in display_df.columns:
        display_df = display_df.drop(columns=["Navigasi"])
    display_df = display_df.rename(columns={
        "Letak Baris": "Posisi",
        "Nama Penumpang": "Penumpang"
    })
    
    # Warna baris berdasarkan status
    st.dataframe(
        display_df.set_index("Nomor Kursi"),
        use_container_width=True,
        height=400,
        column_config={
            "Status": st.column_config.Column(
                "Status",
                help="Status kursi (Tersedia/Dipesan)"
            ),
            "Penumpang": st.column_config.Column(
                "Penumpang",
                help="Nama penumpang jika sudah dipesan"
            )
        }
    )
    
    # Visualisasi Circular Linked List - Lebih menarik
    st.markdown("### 🔄 Struktur Data Circular Linked List")
    
    # Buat diagram dengan emoji yang lebih jelas
    diagram_parts = []
    for k in manifes_data:
        nomor_clean = k['Nomor Kursi'].replace("Kursi ", "")
        if k.get("Navigasi") == "📍 Sedang Dilihat":
            diagram_parts.append(f"🔴👉[{nomor_clean}]👈🔴")
        elif k["Status"] == "Dipesan":
            diagram_parts.append(f"🔴{nomor_clean}🔴")
        else:
            diagram_parts.append(f"🟢{nomor_clean}🟢")
    
    diagram = " → ".join(diagram_parts) + " → 🔄 (kembali ke awal)"
    
    # Tampilkan diagram dalam kotak kode
    st.code(diagram, language="text")
    
    # Legend
    col_leg1, col_leg2, col_leg3, col_leg4 = st.columns(4)
    with col_leg1:
        st.caption("👉👈 Kursi aktif")
    with col_leg2:
        st.caption("🔴 Terisi/Dipesan")
    with col_leg3:
        st.caption("🟢 Tersedia")
    with col_leg4:
        st.caption("🔄 Circular")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray; padding: 20px;">
    <p>© 2024 PesonaTour - Circular Linked List Booking System with Voice Guide</p>
    <p>🚌 Sistem pemesanan tiket bus pariwisata berbasis Circular Linked List</p>
</div>
""", unsafe_allow_html=True)