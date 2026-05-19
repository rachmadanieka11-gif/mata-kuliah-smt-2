from gtts import gTTS
import streamlit as st
import queue

st.title("antrian klinik sederhana")
st.write("ini adalah aplikasi antrian klinik sederhana")

#inisialisasi state untuk menyimpan data 
if  "antrian" not in st.session_state:
    st.session_state.antrian = queue.Queue()

#membuat tombol input antrian
input_antrian = st.text_input("masukkan nama pasien ")
if st.button("tambah antrian"):
    st.session_state.antrian.put(input_antrian)
    st.write("antrian berhasil ditambahkan")

#menampilkan seluruh antrian
st.write("seluruh antrian")
nomor = 1
for i in st.session_state.antrian.queue:
    st.write(f"antrian ke {nomor} : {i}")
    nomor += 1

#membuat tombol pemanggilan antrian 
st.write   ("seluruh antrian")
if st.button("panggil antrian"):
    if not st.session_state.antrian.empty():
            pasien = st.session_state.antrian.get()
            st.write(f"memanggil antrian : {pasien}")
            tts = gTTS(f"memanggil pasien: {pasien}",lang="id")
            tts.save("output.mp3")
            st.audio("output.mp3", autoplay=True)
    else:
        st.write("antrian kosong")