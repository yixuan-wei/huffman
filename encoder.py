from collections import Counter
from collections import defaultdict
import matplotlib.pyplot as plt


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
        self.out_file = None
        self.tree = []

    def process(self):
        self.file_name = self.input_file_name()
        self.read_file(self.file_name, self.dictionary.update, self.update_total_count)
        self.dictionary = self.dictionary.most_common()
        self.print_frequency()
        self.root = self.build_huffman_tree()
        if self.root:
            self.build_huffman_reference()
        else:
            print("ERROR: the tree root is still null after building the tree")
        self.out_file = open(self.file_name + "_encoded", 'w')
        if self.out_file and self.tree:
            self.out_file.write(" ".join(self.tree))
            self.out_file.write("\n")
            self.read_file(self.file_name, self.translate_write_file)
        else:
            print("ERROR: opening encoding out file failed")

    def input_file_name(self):
        print("please make sure your target file for encoding is under the same directory with this script")
        return input("File Name：")

    def update_total_count(self, count):
        self.total_count += count

    def read_file(self, file_name, execute, execute1=None):
        try:
            file = open(file_name, 'rb')
            temp = file.read(1024)
            while temp:
                if execute1 is not None:
                    execute1(len(temp))
                # self.total_count += len(temp)
                print(temp)
                execute(temp)
                # self.dictionary.update(temp)
                temp = file.read(1024)
            file.close()
        except FileNotFoundError:
            print("file not found")
            self.input_file_name()
        except PermissionError:
            print("you don't have the read permission to this file")
            self.input_file_name()

    def print_frequency(self):
        temp_dict = [[bytes([each[0]]), each[1] / self.total_count * 100] for each in self.dictionary]
        minor = 0
        while len(temp_dict) > 0:
            if temp_dict[-1][1] < 0.05:
                minor += temp_dict[-1][1]
                temp_dict.pop()
            else:
                break
        if minor != 0:
            temp_dict.append(["Others", minor])
        fig1, ax1 = plt.subplots()
        ax1.pie([each[1] for each in temp_dict], labels=[each[0] for each in temp_dict], autopct='%1.1f%%',
                startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.show()

    def build_huffman_tree(self):
        tree_node_list = [TreeNode(each[0], each[1]) for each in self.dictionary]
        while len(tree_node_list) > 1:
            print("ready to combine tree nodes")
            x = tree_node_list.pop()
            y = tree_node_list.pop()
            z = TreeNode(-1, x.frequency + y.frequency)
            z.left = x
            z.right = y
            # insert z into sequenced list
            for t in range(len(tree_node_list)):
                if tree_node_list[-t - 1].frequency >= z.frequency:
                    print("ready to insert combined node to list")
                    tree_node_list.insert(-t, z)
                    break
                if t == len(tree_node_list) - 1:
                    print("insert combined node to list start")
                    tree_node_list.insert(0, z)
            if len(tree_node_list) == 0:
                print("insert combined node to list start when list empty")
                tree_node_list.insert(0, z)
        if len(tree_node_list) == 1:
            return tree_node_list[0]
        else:
            print("list length: %i" % len(tree_node_list))
            print("ERROR: byte frequency dictionary is null, probably read problem")
            return None

    def build_huffman_reference(self):
        path = ""
        cur = self.root
        stack = []
        self.tree = []
        while cur is not None or len(stack) > 0:
            if cur is not None:
                self.tree.append(str(cur.data))
                stack.append([cur, path])
                cur = cur.right
                path += "1"
            else:
                cur, path = stack.pop()
                print("cur.data %s : path %s" % (cur.data, path))
                self.reference[cur.data] = path
                cur = cur.left
                path += "0"

    def translate_write_file(self, temp_write):
        for each in temp_write:
            self.out_file.write(self.reference[int(each)])

    def write_file(self, file_name):
        out_file = open(file_name + "_encoded", 'w')
        out_file.write(str(list(self.dictionary.elements())[0]))


if __name__ == "__main__":
    encoder = HuffmanEncoder()
    encoder.process()
