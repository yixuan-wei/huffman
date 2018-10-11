'''
Huffman Decoder
Requirement: python3
execution order sample: 
    python3 decoder.py test.txt_encoded test.txt   (source:test.txt_encoded, output:test.txt)
    python3 decoder.py test.txt_encoded (source:test.txt_encoded, output:./test.txt_encoded_decoded)
    python3 decoder.py (source:to-be-input, output:./to-be-input_decoded)
Author: Yixuan Wei
2018.10.11
'''
import os
import sys


class TreeNode:
    def __init__(self, letter_byte):
        self.data = letter_byte
        self.left = None
        self.right = None


class HuffmanDecoder:
    def __init__(self):
        self.root = None
        self.content = []
        self.file_name = ""
        self.out_file = None
        self.temp_pointer = None
        self.total_count = 0

    def process(self):
        # name of input and output files
        if len(sys.argv) == 1:
            self.file_name = self.input_file_name()
            self.out_file = open(self.file_name + "_decoded", 'wb')
        elif len(sys.argv) == 2:
            self.file_name = sys.argv[1]
            self.out_file = open(self.file_name + "_decoded", 'wb')
        elif len(sys.argv) == 3:
            self.file_name = sys.argv[1]
            self.out_file = open(sys.argv[2], 'wb')
        # construct tree, then read input and write into output
        self.read_file(self.file_name, self.write_file, self.construct_tree)
        print("File decoding finished")
        self.out_file.close()
        # if tree constructed unsuccessfully, delete the output file
        if self.root is None:
            os.remove(self.file_name + "_decoded")

    def input_file_name(self):
        print("please make sure your target file for decoding is under the same directory with this script")
        return input("File Name：")

    def read_file(self, file_name, execute, execute1):
        try:
            file = open(file_name, 'rb')
            # read the total count of bytes in original file
            self.total_count = int(file.readline().split()[0])
            total = self.total_count
            print("Total ",self.total_count," bytes")
            # read and build huffman tree
            print("Reading tree data")
            tree = file.read(1024)
            pos = tree.find(b'\n\n')
            former = 0
            while pos==-1:
                tree += file.read(1024)
                former +=1024
                pos = tree.find(b'\n\n',former)
            temp_byte = tree[pos+2:]
            tree = tree[:pos]
            # split tree into array
            i=0
            tree_array = []
            while i<len(tree)-1:
                if bytes((tree[i],))==b'-' and bytes((tree[i+1],))==b'1' and bytes((tree[i+2],))==b',':
                    tree_array.append(-1)
                    i = i+3
                elif bytes((tree[i+1],))!=b',':
                    print('ERROR: tree structure is not right, building will abort')
                    sys.exit(1)
                else:
                    tree_array.append(bytes((tree[i],)))
                    i = i+2
            tree_array.append(bytes((tree[-1],)))
            print("TREE: ",tree_array)
            self.root = execute1(tree_array)
            # read and travel the tree to write the corresponding output
            print("Translating file")
            if self.root is not None:
                self.temp_pointer = self.root
                temp_count = 0
                temp_byte += file.read(1024)
                while temp_byte:
                    temp_count+=len(temp_byte)
                    execute(temp_byte)
                    print("File processed ",int(temp_count/total*100),"%")
                    temp_byte = file.read(1024)
            file.close()
        except FileNotFoundError:
            self.input_file_name()
        except PermissionError:
            print("you don't have the read permission to this file")
            self.input_file_name()

    def construct_tree(self, tree):
        print("Constructing huffman tree")
        tree = [TreeNode(each) for each in tree]
        stack = []
        while len(tree) > 0:
            x = tree.pop()  # read from the end in this traversal post order tree
            if x.data == -1:
                if len(stack) > 1:
                    y = stack.pop()
                    z = stack.pop()
                    x.left = z
                    x.right = y
                else:
                    print("ERROR: tree structure is not right, decoding will abort")
                    return None
            stack.append(x)
        if len(stack) == 1:
            return stack[0]
        else:
            print("ERROR: tree structure is not right, decomposing will abort")
            return None

    def write_file(self, temp_byte):
        # travel the tree, temp_pointer for travel marker
        for each_byte in temp_byte:
            each_byte = bin(each_byte)[2:].zfill(8)
            for each in each_byte:
                if self.temp_pointer.left is None:
                    # print("writing ",self.temp_pointer.data)
                    self.out_file.write(self.temp_pointer.data)
                    self.temp_pointer = self.root
                    self.total_count -= 1
                    if self.total_count == 0:
                        return
                if each == '0':
                    self.temp_pointer = self.temp_pointer.left
                elif each == '1':
                    self.temp_pointer = self.temp_pointer.right
                else:
                    print("ERROR: the encoded info is broken, decoding will abort")
                    sys.exit(1)


if __name__ == "__main__":
    decoder = HuffmanDecoder()
    decoder.process()
