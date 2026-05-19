class DoubleLinkedList:
    def display(self):
        current_node = self.head
        while current_node:
            print(current_node.data, end=" <-> ")
            current_node = current_node.next
        print("None")

    def hapus_data(self, data):
        current_node = self.head
        while current_node:
            if current_node.data == data:
                if current_node.prev:
                    current_node.prev.next = current_node.next
                else:
                    self.head = current_node.next
                
                if current_node.next:
                    current_node.next.prev = current_node.prev
                
                return
            current_node = current_node.next

# Contoh penggunaan (berdasarkan baris 39-44 di gambar)
dll = DoubleLinkedList()
dll.tambah_belakang(10)
dll.tambah_belakang(20)
dll.tambah_belakang(30)
dll.hapus_data(20) # Mencoba menghapus data yang ada
dll.display()
