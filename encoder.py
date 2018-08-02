from collections import Counter
from collections import defaultdict


class TreeNode:
    def __init__(self, letter_byte, frequency):
        self.data = letter_byte
        self.frequency = frequency
        self.left = None
        self.right = None


class HuffmanEncoder:
    def __init__(self):
        self.dictionary = Counter()
        self.root = None
        self.file_name = ""
        self.reference = dict()
        self.total_count = 0

    def process(self):
        self.file_name = self.input_file_name()
        self.read_file(self.file_name)
        self.root=self.build_huffman_tree()
        if self.root:


    def input_file_name(self):
        print("please make sure your target file for encoding is under the same directory with this script")
        return input("File Name：")

    def read_file(self, file_name):
        try:
            file = open(file_name, 'rb')
            self.total_count= 0
            temp = file.read(1024)
            while temp:
                self.total_count+=len(temp)
                print(temp)
                self.dictionary.update(temp)
                print(list(self.dictionary.elements()))
                temp = file.read(1024)
            file.close()
        except FileNotFoundError:
            print("file not found")
            self.input_file_name()
        except PermissionError:
            print("you don't have the read permisson to this file")
            self.input_file_name()

    def print_frequency(self):
        

    def build_huffman_tree(self):
        tree_node_list = [TreeNode(each[0], each[1]) for each in self.dictionary.most_common()]
        while len(tree_node_list) > 1:
            x = tree_node_list.pop(-1)
            y = tree_node_list.pop(-1)
            z = TreeNode(-1, x.frequency + y.frequency)
            # insert z into sequenced list
            for t in range(len(tree_node_list)):
                if tree_node_list[-t - 1].frequency >= z.frequency:
                    tree_node_list.insert(-t, z)
                    break
                if t == len(tree_node_list) - 1:
                    tree_node_list.insert(0, z)
        if len(tree_node_list)==1:
            return tree_node_list[0]
        else:
            print("ERROR: byte frequency dictionary is null, probably read problem")
            return None

    def build_huffman_reference(self):
        path=""
        cur = self.root
        stack = []
        visited = set() # visited nodes
        while cur is not None:
            if cur not in visited:
                visited.add(cur)
                stack.append([cur,path])
                if cur.left is not None:
                        path+="0"
                        # stack.append(cur.right)
                        cur = cur.left
                else:
                    cur, temp_path = stack.pop()
                    print("cur.data %s : path %s"%(cur.data,temp_path))
                    self.reference[cur.data] = temp_path
                    # path.pop()
                    try:
                        cur,path = stack.pop()
                    except IndexError:
                        break
            else:
                if cur.right is not None:
                    path+="1"
                    cur = cur.right



    def write_file(self, file_name):
        out_file = open(file_name + "_encoded", 'w')
        out_file.write(str(list(self.dictionary.elements())[0]))


if __name__ == "__main__":
    encoder = HuffmanEncoder()
    encoder.input_file_name()
