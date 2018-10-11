'''
Byte Comparer for 2 files
Requirement: python3
execution order sample: 
    python3 test.py test.txt test_out.txt
Author: Yixuan Wei
2018.10.11
'''
import sys
import os


class CompareFile:
    def __init__(self):
        self.file1 = None
        self.file2 = None
        self.same = True

    def process(self):
        # names of two files to be compared
        if len(sys.argv) == 3:
            self.file1 = open(sys.argv[1], 'rb')
            self.file2 = open(sys.argv[2], 'rb')
            if self.file1 and self.file2:
                temp1 = self.file1.read(1024)
                temp2 = self.file2.read(1024)
                while self.same and (temp1 or temp2):
                    self.same = self.compare_bytes(temp1, temp2)
                    temp1 = self.file1.read(1024)
                    temp2 = self.file2.read(1024)
                if self.same:
                    print("RESULT: True, two files are same")
                else:
                    print("RESULT: False, two files are different")
            else:
                print("ERROR: opening files failed! check route")
                sys.exit(1)
            self.file1.close()
            self.file2.close()
            sys.exit(0)
        else:
            print("ERROR: number of files not right, only compare two files")
            sys.exit(2)

    def compare_bytes(self, temp1, temp2):
        if len(temp1) != len(temp2):
            print("length ",len(temp1)," & ",len(temp2)," are different")
            return False
        else:
            for i in range(len(temp1)):
                if temp1[i] != temp2[i]:
                    print("on position ",i," ",temp1[i],' & ',temp2[i],' are different')
                    return False
            print("1024 bytes same")
            return True


if __name__ == "__main__":
    compare_file = CompareFile()
    compare_file.process()
