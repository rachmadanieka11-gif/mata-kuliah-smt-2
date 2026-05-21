import streamlit as st
from gtts import gTTS
import base64
import pandas as pd
from datetime import datetime

# --- KONSEP MYQUEUE DENGAN LOGIKA TAMBAHAN ---
class MyQueue:
    def __init__(self):
        if 'queue_list' not in st.session_state:
            st.session_state.queue_list = []
        if 'history' not in st.session_state:
            st.session_state.history = []
        if 'quota' not in st.session_state:
            st.session_state.quota = 50 # Default kuota 50 porsi

    def enqueue(self, name):
        # Cek apakah kuota masih cukup (antrian + yang sudah makan)
        total_booked = len(st.session_state.queue_list) + len(st.session_state.history)
        if total_booked < st.session_state.quota:
            st.session_state.queue_list.append(name)
            return True, "Berhasil masuk antrian!"
        return False, "Maaf, kuota makan hari ini sudah habis!"
        
    def dequeue(self):
        if len(st.session_state.queue_list) > 0:
            student = st.session_state.queue_list.pop(0)
            # Tambahkan ke riwayat
            st.session_state.history.append({
                "Nama": student,
                "Waktu Ambil": datetime.now().strftime("%H:%M:%S")
            })
            return student
        return None

# --- FUNGSI AUDIO ---
import time # Tambahkan import ini di bagian paling atas

def play_voice(text):
    # Tempat sementara untuk menyimpan audio agar tidak bertabrakan
    audio_placeholder = st.empty()
    
    try:
        # 1. Ubah teks jadi suara
        tts = gTTS(text=text, lang='id')
        tts.save("call.mp3")
        
        # 2. Baca filenya
        with open("call.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            
            # 3. Buat ID unik menggunakan waktu (detik) agar browser tidak bingung
            unique_id = int(time.time())
            
            # 4. Susun kode HTML untuk memutar suara secara otomatis
            md = f"""
                <audio autoplay="true" id="audio_{unique_id}">
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                """
            # 5. Masukkan ke dalam halaman
            audio_placeholder.markdown(md, unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Gagal memutar suara: {e}")
        
# --- UI STREAMLIT ---
def main():
    st.set_page_config(page_title="Sistem MBG Terintegrasi", layout="wide")
    st.title("🍱Manajemen Makan Bergizi Gratis Di Sekolah Dasar")
    
    q = MyQueue()

    # SIDEBAR: PENGATURAN & INPUT
    with st.sidebar:
        st.header("⚙️ Pengaturan & Input")
        st.session_state.quota = st.number_input("Atur Total Kuota Hari Ini:", value=st.session_state.quota)
        
        st.divider()
        st.subheader("Registrasi Siswa")
        new_student = st.text_input("Nama Siswa:")
        if st.button("Daftarkan Antrian"):
            if new_student:
                success, msg = q.enqueue(new_student)
                if success: st.success(msg)
                else: st.error(msg)
            else:
                st.warning("Masukkan nama!")

    # MAIN CONTENT: 3 KOLOM
    col_q, col_call, col_hist = st.columns([1, 1, 1])

    with col_q:
        st.subheader("📋 Antrian Saat Ini")
        if st.session_state.queue_list:
            for i, name in enumerate(st.session_state.queue_list):
                st.info(f"{i+1}. {name}")
        else:
            st.write("Belum ada antrian.")

    with col_call:
        st.subheader("🔊 Panggilan")
        
        # Inisialisasi variabel untuk menyimpan nama yang dipanggil agar tetap muncul setelah klik
        if 'last_called' not in st.session_state:
            st.session_state.last_called = None

        if st.button("PANGGIL BERIKUTNYA", type="primary"):
            called = q.dequeue()
            if called:
                st.session_state.last_called = called
                play_voice(f"Panggilan untuk {called} silahkan ambil bagian anda") # Suara dulu
                # JANGAN PAKAI st.rerun() DI SINI
            else:
                st.error("Antrian kosong!")
        
        # Tampilkan status nama yang sedang dipanggil (agar tidak hilang)
        if st.session_state.last_called:
            st.success(f"SEDANG DIPANGGIL: {st.session_state.last_called}")

    with col_hist:
        st.subheader("📜 Riwayat Pengambilan")
        if st.session_state.history:
            df = pd.DataFrame(st.session_state.history)
            st.table(df)
            if st.button("Hapus Riwayat"):
                st.session_state.history = []
                st.rerun()
        else:
            st.write("Belum ada data.")

if __name__ == "__main__":
    main()