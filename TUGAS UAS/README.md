# 🚌 PesonaTour: Bus Seat Booking System with Voice Guide

Sebuah aplikasi kasir pemesanan tiket bus pariwisata interaktif yang memanfaatkan implementasi struktur data **User-Defined Singly Circular Linked List** secara manual untuk melakukan penelusuran kursi tanpa henti (melingkar), dilengkapi dengan panduan dan asisten suara interaktif berbasis Text-to-Speech (gTTS).

---

## 📌 Fitur Utama

- **Struktur Data Circular Linked List Manual**: Manajemen data kursi bus dirancang dari nol menggunakan visualisasi node saling terhubung secara melingkar. Pointer akhir (*tail*) otomatis mengunci kembali ke pointer awal (*head*).
- **Navigasi Tanpa Henti (*Infinite Carousel*)**: User dapat menggeser ke kursi selanjutnya (`next`) atau kursi sebelumnya (`prev`) secara terus-menerus tanpa takut mengalami *out of bounds* karena ujung data akan kembali ke awal/akhir.
- **Asisten Suara Interaktif (gTTS Integration)**: Setiap kali kursi digeser, status dibaca, tiket dipesan, atau dibatalkan, sistem akan mengeluarkan output suara berbahasa Indonesia secara natural.
- **Dashboard Manifes & Statistik Real-time**: Menampilkan visualisasi okupansi persentase kursi terisi, sisa kursi, tabel manifest penumpang terintegrasi Pandas DataFrame, hingga diagram denah visual struktur data melingkarnya.
- **Pemesanan & Pembatalan Instan**: Validasi nama penumpang minimal 3 karakter dengan fungsi mutasi status langsung pada node yang sedang ditunjuk oleh *pointer active current*.

---

## 📂 Struktur Proyek

Proyek ini terbagi menjadi dua komponen utama yang saling terhubung:

1. **`logictiket.py` (Backend)**: Berisi representasi `KursiNode` dan class utamanya `BusSeatCircularList`. Menangani alokasi memori denah baris depan-tengah-belakang serta logika traversal sirkular.
2. **`app.py` (Frontend)**: Berisi antarmuka web berbasis **Streamlit** untuk visualisasi interaktif, manajemen session state untuk menjaga keutuhan linked list, serta `VoiceManager` untuk memproses Text-to-Speech.

---

## 🛠️ Logika Kode & Cara Kerja Struktur Data

### 1. Struktur Node dan Circular Linked List (`logictiket.py`)
Setiap objek kursi dibungkus dalam sebuah `KursiNode` yang menyimpan referensi alamat pointer berikutnya (`self.next`). Class `BusSeatCircularList` menghubungkan node-node ini sehingga membentuk lingkaran tertutup:

```python
class KursiNode:
    def __init__(self, nomor_kursi, posisi):
        self.nomor_kursi = nomor_kursi  # Contoh: "Kursi 01"
        self.posisi = posisi            # Contoh: "Baris Depan-Kiri"
        self.status = "Tersedia"        # Default awal
        self.nama_penumpang = ""
        self.next = None                # Pointer ke node berikutnya

class BusSeatCircularList:
    def __init__(self, jumlah_kursi):
        self.head = None
        self.current = None             # Melacak node yang sedang dilihat user
        self.total_kursi = jumlah_kursi
        self._buat_denah_kursi()
```

### 2. Navigasi Melingkar (Traversal)
- **Geser Maju (`next`)**: Hanya perlu memindahkan pointer aktif ke alamat berikutnya: `self.current = self.current.next`.
- **Geser Mundur (`prev`)**: Karena ini merupakan *Singly* Linked List, untuk mencari node sebelumnya kita melakukan traversal pembantu (`bantu`) dari `head` hingga menemukan node yang `next`-nya adalah `current`:
  ```python
  bantu = self.head
  while bantu.next != self.current:
      bantu = bantu.next
  self.current = bantu
  ```

---

## 🚀 Panduan Instalasi dan Menjalankan Aplikasi

Pastikan Anda telah menginstal Python di komputer Anda (versi 3.8 ke atas direkomendasikan).

### 1. Persiapan Berkas
Pastikan Anda memisahkan kode backend dan frontend ke dalam dua file terpisah di dalam satu folder yang sama:
- Simpan kode **Backend** dengan nama file **`logictiket.py`**.
- Simpan kode **Frontend** dengan nama file **`app.py`**.

### 2. Instalasi Dependensi
Buka terminal/command prompt, masuk ke direktori proyek, lalu instal pustaka (libraries) yang dibutuhkan melalui pip:

```bash
pip install streamlit pandas gtts
```

### 3. Menjalankan Aplikasi
Jalankan server lokal Streamlit dengan mengeksekusi perintah berikut pada terminal Anda:

```bash
streamlit run app.py
```

Setelah itu, browser Anda akan otomatis terbuka dan menampilkan alamat `http://localhost:8501`.

---

## 🎵 Petunjuk Penggunaan Kontrol Suara

1. **Koneksi Internet**: Library `gTTS` memerlukan koneksi internet aktif untuk mengubah teks informasi tiket menjadi file audio (.mp3).
2. **Aktifkan Fitur**: Secara default fitur suara aktif. Jika Anda merasa terganggu atau ingin menghemat kuota, Anda dapat menekan tombol **"Matikan Suara"** di sidebar kiri.
3. **Interaksi Manual**: Jika suara tidak berputar otomatis di peramban (akibat kebijakan *Autoplay Block* pada browser modern), Anda cukup menekan tombol simbol **🔊** atau **"Info Kursi"** yang disediakan di sebelah baris menu navigasi.

---

## 📊 Ilustrasi Alur Data Circular Linked List

Visualisasi rantai memori melingkar pada terminal aplikasi digambarkan sebagai berikut:
```text
🟢01🟢 → 🟢02🟢 → 🔴👉[03]👈🔴 → 🟢04🟢 → ... → 🟢12🟢 → 🔄 (kembali ke awal/01)
```
- **🟢01🟢**: Menandakan nomor kursi tersebut berstatus **Tersedia**.
- **🔴03🔴**: Menandakan nomor kursi tersebut telah **Dipesan**.
- **👉[03]👈**: Menandakan posisi *Pointer Current* aktif yang sedang diulas oleh kasir/sistem.
