from collections import Counter
from collections import defaultdict
import matplotlib.pyplot as plt
import sys
import struct

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
        # name of input and output files
        if len(sys.argv)==1:
            self.file_name = self.input_file_name()
            self.out_file = open(self.file_name + "_encoded", 'wb')
        elif len(sys.argv)==2:
            self.file_name = sys.argv[1]
            self.out_file = open(self.file_name + "_encoded", 'wb')
        elif len(sys.argv)==3:
            self.file_name = sys.argv[1]
            self.out_file = open(sys.argv[2], 'wb')
        else:
            print("ERROR: wrong number of parameters")
            sys.exit(1)
        # read from input file and display pie chart
        self.read_file(self.file_name, self.dictionary.update, self.update_total_count)
        self.dictionary = self.dictionary.most_common()
        print("frequency list: ",self.dictionary)
        self.print_frequency()
        # build huffman tree and references
        self.root = self.build_huffman_tree()
        if self.root:
            self.build_huffman_reference()
        else:
            print("ERROR: the tree root is still null after building the tree")
        # output the encoded content
        if self.out_file and self.tree:
            self.out_file.write(bytes(" ".join(self.tree)+"\n", encoding="gbk"))
            self.read_file(self.file_name, self.translate_write_file)
        else:
            print("ERROR: opening encoding out file failed")
        self.out_file.close()

    def input_file_name(self):
        print("please make sure your target file for encoding is under the same directory with this script")
        return input("File Name：")

    def update_total_count(self, count):
        self.total_count += count

    def read_file(self, file_name, execute, execute1=None):
        try:
            file = open(file_name, 'rb')
            # read in bytes, every time 1024 bytes
            temp = file.read(1024)
            while temp:
                # accumulate total length of file in bytes
                if execute1 is not None:
                    print(len(temp))
                    execute1(len(temp))
                # print(temp)
                execute(temp)
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
        # accumulate ones except for the more frequent 20 items into class Others 
        minor = 0
        while len(temp_dict) > 20:
            minor += temp_dict[-1][1]
            temp_dict.pop()
        if minor != 0:
            temp_dict.append(["Others", minor])
        # draw pie chart
        fig1, ax1 = plt.subplots()
        ax1.pie([each[1] for each in temp_dict], labels=[each[0] for each in temp_dict], autopct='%1.1f%%',
                startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.show()

    def build_huffman_tree(self):
        # sequenced list of all nodes, from large frequency to small
        tree_node_list = [TreeNode(each[0], each[1]) for each in self.dictionary]
        while len(tree_node_list) > 1:
            # combine two leat frequency nodes x and y into node z
            x = tree_node_list.pop()
            y = tree_node_list.pop()
            z = TreeNode(-1, x.frequency + y.frequency)
            z.left = x
            z.right = y
            # insert z into sequenced list
            for t in range(len(tree_node_list)):
                if tree_node_list[-t - 1].frequency >= z.frequency:
                    # print("ready to insert combined node to list")
                    tree_node_list.insert(-t, z)
                    break
                if t == len(tree_node_list) - 1:
                    # print("insert combined node to list start")
                    tree_node_list.insert(0, z)
            if len(tree_node_list) == 0:
                # print("insert combined node to list start when list empty")
                tree_node_list.insert(0, z)
        # when only the root node is left in the list, succeed
        if len(tree_node_list) == 1:
            return tree_node_list[0]
        # when not one node in the list, fail
        else:
            print("list length: %i" % len(tree_node_list))
            print("ERROR: byte frequency dictionary is null, probably read problem")
            return None

    def build_huffman_reference(self):
        path = 0 # huffman code for one node in tree
        cur = self.root
        stack = [] # save node and corresbonding path
        self.tree = [] # store the tree in traversal post order
        # traversal post order to travel the huffman tree to calculate path
        while cur is not None or len(stack) > 0:
            if cur is not None:
                self.tree.append(str(cur.data))
                stack.append([cur, path])
                cur = cur.right
                path = 10*path+1
            else:
                cur, path = stack.pop()
                # print("cur.data %s : path %s" % (cur.data, path))
                self.reference[cur.data] = path
                cur = cur.left
                path =10*path

    def translate_write_file(self, temp_write):
        for each in temp_write:
            print(each)
            #TODO: 二进制编码的路径的合理表示？
            self.out_file.write(self.reference[each])


if __name__ == "__main__":
    encoder = HuffmanEncoder()
    encoder.process()
