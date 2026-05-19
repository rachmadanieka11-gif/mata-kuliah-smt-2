#membuat queue dari linked ;ost 
#buat class node

class node:
    def init(self, data):
        self.data = data
        self.next = None

# membuat kelas myqueue
class Queue:
    def init(self):
        self.head = None
        self.tail = None
        self.size = 0

# membuat methode enqueue
    def enqueue(self, data):
        new_node = node(data)
        if  self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1
        print(f"Data {data} berhasil ditambahkan ke antrean")

#membuat method dequeue : input element atau data
    def dequeue(self):
        if self.is_empty():
            print("queue is empty")
            return None
        data = self.head.data
        self.head = self.head.next
        self.size -= 1
        print(f"dequeued : {data} ")
        return data

    def peek(self):
        if self.is_empty():
            print("queue is empty")
            return None
        return self.head.data

#methode untuk mengecek apakah queue kosong atau tidak
    def is_empty(self):
        return self.size == 0

#methode untuk menampilkan queue
    def printQueue(self):
        if self.is_empty():
            print("queue is empty")
            return None

Antrian = Queue()
Antrian.enqueue("andi")
Antrian.enqueue("budi")
Antrian.enqueue("caca")