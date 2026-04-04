import streamlit as st

# Judul Aplikasi
st.title("🚀 Word Count Application 🚀")

# Input teks dari pengguna
textInput = st.text_area("Input your Paragraph here")

# Tombol untuk memproses
if st.button("Count Words"):
    if textInput:
        # 1. Memisahkan kata dan mengubah ke huruf kecil
        words = textInput.lower().split()
        
        # 2. Menghitung frekuensi kata dengan dictionary
        counts = {}
        for word in words:
            counts[word] = counts.get(word, 0) + 1
            
        # 3. Menampilkan Total Kata
        st.subheader("Word Total")
        st.write(f"Jumlah total kata: {len(words)}")
        
        # 4. Menampilkan Tabel Frekuensi
        st.subheader("Word Frequency")
        st.write(counts)
        
        # 5. Menampilkan Grafik
        st.subheader("Visualisasi")
        st.bar_chart(counts)
    else:
        st.warning("Silakan masukkan teks terlebih dahulu!") 