import os
import sys


class TreeNode:
    def __init__(self, letter_byte):
        self.data = int(letter_byte)
        self.left = None
        self.right = None


class HuffmanDecoder:
    def __init__(self):
        self.root = None
        self.content = []
        self.file_name = ""
        self.out_file = None
        self.temp_pointer = None

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
        self.out_file.close()
        # if tree constructed unsuccessfully, delete the output file
        if self.root is None:
            os.remove(self.file_name + "_decoded")

    def input_file_name(self):
        print("please make sure your target file for decoding is under the same directory with this script")
        return input("File Name：")

    def read_file(self, file_name, execute, execute1):
        try:
            file = open(file_name, 'r')
            # read and build huffman tree
            tree = file.readline().split()
            self.root = execute1(tree)
            # read and travel the tree to write the corresbonding output
            if self.root is not None:
                self.temp_pointer = self.root
                temp_byte = file.read(1024)
                while temp_byte:
                    execute(temp_byte)
                    temp_byte = file.read(1024)
            file.close()
        except FileNotFoundError:
            self.input_file_name()
        except PermissionError:
            print("you don't have the read permisson to this file")
            self.input_file_name()

    def construct_tree(self, tree):
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
        for each in temp_byte:
            if self.temp_pointer.left is None:
                self.out_file.write(bytes((self.temp_pointer.data,)))
                self.temp_pointer = self.root
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
