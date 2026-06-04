#Backend: Struktur Data Circular Linked List Manual untuk Seat Booking Bus

class KursiNode:
    """Representasi satu kursi fisik di dalam armada bus pariwisata."""
    def __init__(self, nomor_kursi, posisi):
        self.nomor_kursi = nomor_kursi        # Contoh: "Kursi 01", "Kursi 02"
        self.posisi = posisi                  # Contoh: "Depan-Kiri", "Belakang-Kanan"
        self.status = "Tersedia"              # Status awal kursi saat aplikasi dibuka
        self.nama_penumpang = ""              # Menyimpan nama jika sudah dipesan
        self.next = None                      # Pointer ke kursi urutan berikutnya

class BusSeatCircularList:
    """User-Defined Singly Circular Linked List untuk penelusuran kursi tanpa henti."""
    def __init__(self, jumlah_kursi):
        self.head = None
        self.current = None  # Pointer aktif untuk melacak kursi yang sedang dilihat user
        self.total_kursi = jumlah_kursi
        
        self._buat_denah_kursi()

    def _buat_denah_kursi(self):
        """Membangun rantai melingkar otomatis untuk kursi bus."""
        for i in range(1, self.total_kursi + 1):
            # Penentuan posisi lebih detail
            if i <= 4:
                posisi_detail = "Baris Depan"
                sub_posisi = "Kiri" if i % 2 == 1 else "Kanan"
                posisi_detail = f"{posisi_detail}-{sub_posisi}"
            elif i <= 8:
                posisi_detail = "Baris Tengah"
                sub_posisi = "Kiri" if i % 2 == 1 else "Kanan"
                posisi_detail = f"{posisi_detail}-{sub_posisi}"
            else:
                posisi_detail = "Baris Belakang"
                sub_posisi = "Kiri" if i % 2 == 1 else "Kanan"
                posisi_detail = f"{posisi_detail}-{sub_posisi}"
            
            baru = KursiNode(f"Kursi {i:02d}", posisi_detail)
            
            if self.head is None:
                self.head = baru
                baru.next = self.head  # Melingkar ke dirinya sendiri di awal
                self.current = baru
            else:
                # Cari ujung ekor saat ini untuk menyambungkan node baru
                bantu = self.head
                while bantu.next != self.head:
                    bantu = bantu.next
                
                bantu.next = baru
                baru.next = self.head  # Mengunci ekor baru agar kembali ke kepala
                
    def geser_ke_kursi_berikutnya(self):
        """Fungsi navigasi untuk bergeser ke nomor kursi selanjutnya."""
        if self.current:
            self.current = self.current.next
            return self.current
        return None
    
    def geser_ke_kursi_sebelumnya(self):
        """Fungsi navigasi untuk bergeser ke nomor kursi sebelumnya."""
        if self.current and self.head:
            bantu = self.head
            # Cari node yang next-nya menunjuk ke current
            while bantu.next != self.current:
                bantu = bantu.next
            self.current = bantu
            return self.current
        return None

    def pesan_kursi_aktif(self, nama):
        """Mengubah status kursi yang sedang ditunjuk oleh pointer current."""
        if self.current and self.current.status == "Tersedia":
            self.current.status = "Dipesan"
            self.current.nama_penumpang = nama
            return True
        return False

    def batalkan_kursi_aktif(self):
        """Mengosongkan kembali manifes penumpang pada kursi aktif."""
        if self.current and self.current.status == "Dipesan":
            self.current.status = "Tersedia"
            self.current.nama_penumpang = ""
            return True
        return False

    def dapatkan_manifes_bus(self):
        """Traversal sirkular untuk mengumpulkan seluruh data kursi tanpa loop tak terbatas."""
        daftar_manifes = []
        if self.head is None:
            return daftar_manifes
            
        bantu = self.head
        count = 0
        
        while count < self.total_kursi:
            status_pointer = "📍 Sedang Dilihat" if bantu == self.current else ""
            
            daftar_manifes.append({
                "Nomor Kursi": bantu.nomor_kursi,
                "Letak Baris": bantu.posisi,
                "Status": bantu.status,
                "Nama Penumpang": bantu.nama_penumpang if bantu.nama_penumpang else "-",
                "Navigasi": status_pointer
            })
            bantu = bantu.next
            count += 1
            
        return daftar_manifes
    
    def get_current_seat_info(self):
        """Mendapatkan informasi kursi yang sedang aktif"""
        if self.current:
            return {
                "nomor": self.current.nomor_kursi,
                "posisi": self.current.posisi,
                "status": self.current.status,
                "nama": self.current.nama_penumpang if self.current.nama_penumpang else None
            }
        return None
    
    def reset_all_seats(self):
        """Reset semua kursi ke status tersedia (untuk testing)"""
        if self.head is None:
            return
        
        bantu = self.head
        count = 0
        while count < self.total_kursi:
            bantu.status = "Tersedia"
            bantu.nama_penumpang = ""
            bantu = bantu.next
            count += 1
        self.current = self.head