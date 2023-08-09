import uuid

def process_input(topic):
    TEMPLATE = "Generate a script for youtube video on {}."
    output = TEMPLATE.format(topic)
    return output

class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
    
    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
            new_node.prev = current
    
    def prepend(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
    
    def delete(self, data):
        current = self.head
        while current:
            if current.data == data:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next
                if current.next:
                    current.next.prev = current.prev
                return
            current = current.next
    
    def search(self, data):
        current = self.head
        while current:
            if current.data == data:
                return current
            current = current.next
        return None
    
    def display(self):
        current = self.head
        while current:
            print(current.data, end=" <-> ")
            current = current.next
        print("None")

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result
    
    @classmethod
    def from_list(cls, lst):
        new_dll = cls()
        for item in lst:
            new_dll.append(item)
        return new_dll

    # Other methods like delete, insert, etc. can be added here

class Scene:
    def __init__(self):
        pass

    def change_narration(self,newNarration):
        self.narration = newNarration

    def change_img_desc(self, newImgDesc):
        self.img_desc = newImgDesc

def script_processing(temp_script):
    processed_script = temp_script.split("\n")
    new_list = []
    script_desc = {}

    for i in processed_script:
        if i == " " or not i:
            continue
        new_list.append(i)
    # print(new_list)
    SCENE = "scene#{}"
    i = 0
    while i < len(new_list):
        # ts = SCENE.format(i)#//2
        script_desc[str(uuid.uuid4())] = [new_list[i][11:-1]]
        i += 1
        # script_desc[ts].append(new_list[i][20:-1])
        # i += 1
    return script_desc
