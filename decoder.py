class TreeNode:
    def __init__(self,letter_byte):
        self.data = letter_byte
        self.left = None
        self.right = None


class HuffmanDecoder:
    def __init__(self):
        self.root = TreeNode(-1)
        self.content = []

    def input_file_name(self):
        print("please make sure your target file for decoding is under the same directory with this script")
        file_name = input("File Name：")
        self.read_file(file_name)

    def read_file(self,file_name):
        try:
            file = open(file_name,'rb')
            temp = file.read(1024)
            # while temp:
            print(temp)
            self.content.append(int(temp))
            self.write_file(file_name)
            file.close()
        except FileNotFoundError:
            self.input_file_name()
        except PermissionError:
            print("you don't have the read permisson to this file")
            self.input_file_name()

    def write_file(self,file_name):
        out_file = open(file_name+"_decoded",'wb')
        out_file.write(bytes(self.content))




if __name__=="__main__":

    print(bytes([32]))
    decoder = HuffmanDecoder()
    decoder.input_file_name()