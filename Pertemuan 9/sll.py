#membuat Single linked list dengan python 
class Node:
    def init(self, data):
        self.data = data
        self.next = None

class SingleLinkedList:
    def init(self):
        self.head = None

    def Tambahan_belakang(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node

    def display(self):
        current_node = self.head
        while current_node:
            print(current_node.data, end=' ')
            current_node = current_node.next
        print("none")

    def hapus_depan(self):
        if self.head is None:
            print("Single Linked List kosong")
            return
        self.head = self.head.next
    def hapus_data(self, data):
        if self.head is None:
            print("Single Linked List kosong")
            return
        if self.head.data == data:
            self.head = self.head.next
            return
        current_node = self.head
        while current_node.next:
            if current_node.next.data == data:
                current_node.next = current_node.next.next
                return
            current_node = current_node.next
        print(f"Data {data} tidak ditemukan dalam Single Linked List")

sll = SingleLinkedList()    
sll.Tambahan_belakang(10)
sll.Tambahan_belakang(20)
sll.Tambahan_belakang(30)
sll.hapus_depan()
print("isi Single linked list")
sll.display()
