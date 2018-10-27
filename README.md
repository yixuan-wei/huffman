# Huffman Encoder and Decoder
This is a tool written for encoding and decoding a file with huffman algorithm, under the requirement of programming portfolio
 assignments by SMU Guildhall 2018 Graduation admission.
 
The explanations for each file are below: 
* encoder.py: encode a file.
* decoder.py: decode a file that was encoded by encoder.py.
* test.py:    compare two files in bytes if they are identical.
* requirements.pdf: the specific requirements & instructions for huffman encoder & decoder.

**Dependences: python3, matplotlib(not necessary)**

## Encoder
**Requirement**: python3, matplotlib(not necessary)<br>
**Execution Command sample**: (suitable for any command line tool)

|Command|source|output|
|-------|:------:|------:|
|python3 encoder.py test.txt test.txt_encoded|test.txt|test.txt_encoded|
|python3 encoder.py test.txt|test.txt|./test.txt_encoded|
|python3 encoder.py|to-be-input|./to-be-input_encoded|

## Decoder
**Requirement**: python3<br>
**Execution command sample**: 

|Command|source|output|
|-------|:------:|------:|
|python3 decoder.py test.txt_encoded test.txt|test.txt_encoded|test.txt|
|python3 decoder.py test.txt_encoded|test.txt_encoded|./test.txt_encoded_decoded|
|python3 decoder.py|to-be-input|./to-be-input_decoded|

## Test
**Requirement**: python3<br>
**Execution command sample**: python3 test.py test.txt test_out.txt
