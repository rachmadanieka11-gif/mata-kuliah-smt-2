class node:
    def __init__(self, data):
        self.data = data
        self.next = None


class stack:
    def __init__(self):
        self.top = None

    def is_empty(self):
        return self.top is None

    def push(self, data):
        new_node = node(data)
        new_node.next = self.top
        self.top = new_node

    def pop(self):
        if self.top is None:
            print("Stack kosong")
            return None
        popped_data = self.top.data
        self.top = self.top.next
        return popped_data

    def peek(self):
        if self.top is None:
            print("Stack kosong")
            return None
        return self.top.data

    def display(self):
        if self.is_empty():
            print("Stack kosong")
            return
        current = self.top
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print("None")


# contoh penggunaan
mystack = stack()
print(mystack.is_empty())
mystack.push(10)
mystack.push(20)
mystack.push(30)
mystack.display()
print(mystack.peek())
print(mystack.pop())
print(mystack.peek())
mystack.display()