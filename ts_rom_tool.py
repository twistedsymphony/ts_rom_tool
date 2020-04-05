# 2020-01-11 twistedsymphony solid-orange.com
import os
import sys

#calculates the size in bits
def calc_size(bits):
  multiplier = 1;
  if bits.upper()[-1:] == 'K':
    bits = bits[:-1]
    multiplier = 1024
  elif bits.upper()[-1:] == 'M':
    bits = bits[:-1]
    multiplier = 131072 #128*1024
  if not bits.isdigit():
    print("bits must be specified as an intiger")
    sys.exit()
  return int(bits)*multiplier

def get_file_size(file_name):
  st = os.stat(file_name)
  return st.st_size

#checks that all of the arguments have been provided
def check_input_count(count):
  if len(sys.argv) <= count:
    print("too few arguments to perform operation")
    sys.exit()
  
  
#combines two or more files into one
def concat(input_files, output_file):
  with open(output_file, 'wb') as outfile:
    for fname in input_files:
      with open(fname, 'rb') as infile:
        for line in infile:
          outfile.write(line)


#pads a file to a specified length with a specified byte
def pad(input_file, bits, output_file, byte_string):
  target_size = calc_size(bits)
  with open(input_file, 'rb') as infile:
    chunk = infile.read(target_size)
    with open(output_file, 'wb') as outfile:
      outfile.write(chunk.ljust(target_size, byte_string))

#creates a file filled to a specified length with a specified byte
def fill(bits, output_file, byte_string):
  target_size = calc_size(bits)
  with open(output_file, 'wb') as outfile:
    outfile.write(byte_string.ljust(target_size, byte_string))
    
    
#splits binary files into smaller files of a given size
def half (input_file, output_file_a, output_file_b):
  file_name = output_file_a
  chunk_size = int(get_file_size(input_file)/2)
  with open(input_file, 'rb') as infile:
    chunk = infile.read(chunk_size)
    while chunk:
      with open(file_name, 'wb') as outfile:
        outfile.write(chunk)
      file_name = output_file_b
      chunk = infile.read(chunk_size)
  

#splits binary files into smaller files of a given size
def split (input_file, bits, output_base):
  file_number = 0
  chunk_size = calc_size(bits)
  with open(input_file, 'rb') as infile:
    chunk = infile.read(chunk_size)
    while chunk:
      with open(output_base + str(file_number), 'wb') as outfile:
        outfile.write(chunk)
      file_number += 1
      chunk = infile.read(chunk_size)


#truncates a binary files into smaller files of a given size
def truncate (input_file, bits, output_file):
  chunk_size = calc_size(bits)
  
  with open(output_file, 'wb') as outfile:
    with open(input_file, 'rb') as infile:
      outfile.write(infile.read(chunk_size))


#byte swaps a binary file
def byteswap(input_file, output_file):
  with open(output_file, 'wb+') as outfile:
    with open(input_file, 'rb') as infile:
      chunk = infile.read(16) #1byte = 8 bits so we need 2bytes to swap at a time
      while chunk:
        swapped_chunk = bytes([c for t in zip(chunk[1::2], chunk[::2]) for c in t])
        outfile.write(swapped_chunk)
        chunk = infile.read(16)


#wordswaps a specified number of bytes in a binary file 
def swap(input_file, output_file, bytes):
  with open(output_file, 'wb+') as outfile:
    with open(input_file, 'rb') as infile:
      chunk = infile.read(bytes)
      A = chunk
      chunk = infile.read(bytes)
      B = chunk
      while chunk:
        outfile.write(B)
        outfile.write(A)
        chunk = infile.read(bytes)
        A = chunk
        chunk = infile.read(bytes)
        B = chunk


#interleaves two files by a specified number of bytes
def interleave(input_file_a, input_file_b, output_file, bytes):
  with open(output_file, 'wb+') as outfile:
    with open(input_file_a, 'rb') as fa:
      with open(input_file_b, 'rb') as fb:
        chunk = fa.read(bytes)
        A = chunk
        chunk = fb.read(bytes)
        B = chunk
        while chunk:
          outfile.write(A)
          outfile.write(B)
          chunk = fa.read(bytes)
          A = chunk
          chunk = fb.read(bytes)
          B = chunk


#deinterleaves a file into two files by a specified number of bytes
def deinterleave(input_file, output_file_a, output_file_b, bytes):
  with open(output_file_a, 'wb+') as oa:
    with open(output_file_b, 'wb+') as ob:
      with open(input_file, 'rb') as infile:
        chunk = infile.read(bytes)
        A = chunk
        chunk = infile.read(bytes)
        B = chunk
        while chunk:
          oa.write(A)
          ob.write(B)
          chunk = infile.read(bytes)
          A = chunk
          chunk = infile.read(bytes)
          B = chunk

process = '-help'
if len(sys.argv) > 1:
  process = sys.argv[1]

if process == '-split': 
  check_input_count(4)
  split(sys.argv[2], sys.argv[3], sys.argv[4])
elif process == '-half':
  check_input_count(4)
  half(sys.argv[2], sys.argv[3], sys.argv[4])
elif process == '-concat':
  check_input_count(4)
  concat([sys.argv[2], sys.argv[3]], sys.argv[4])
elif process == '-multiconcat':
  check_input_count(4)
  input_files = []
  i = 3
  while i < len(sys.argv):
    input_files.append(sys.argv[i])
    i += 1
  concat(input_files, sys.argv[2])
elif process == '-trunc':
  check_input_count(4)
  truncate(sys.argv[2], sys.argv[3], sys.argv[4])
elif process == '-padz': #0 pad
  check_input_count(4)
  pad(sys.argv[2], sys.argv[3], sys.argv[4], b'\x00')
elif process == '-padf': #F pad
  check_input_count(4)
  pad(sys.argv[2], sys.argv[3], sys.argv[4], b'\xFF')
elif process == '-fillz': #0 filled file
  check_input_count(3)
  fill(sys.argv[2], sys.argv[3], b'\x00')
elif process == '-fillf': #F filled file
  check_input_count(3)
  fill(sys.argv[2], sys.argv[3], b'\xFF')
elif process == '-interleave': 
  check_input_count(4)
  interleave(sys.argv[2], sys.argv[3], sys.argv[4], 1)
elif process == '-deinterleave':
  check_input_count(4)
  deinterleave(sys.argv[2], sys.argv[3], sys.argv[4], 1)
elif process == '-byteswap':
  check_input_count(3)
  #byteswap(sys.argv[2], sys.argv[3])
  swap(sys.argv[2], sys.argv[3], 1)
elif process == '-wordswap':
  check_input_count(3)
  swap(sys.argv[2], sys.argv[3], 2)
else: #help
  print ("Here are the available commands:")
  print ("#CONCATENATE two files together:")
  print (" -concat [input file A] [input file B] [output file]")
  print (" ")
  print ("#CONCATENATE two or more files together:")
  print (" -multiconcat [output file] [input file 1] [input file 2] [input file n]...")
  print (" ")
  print ("#HALF a file into two smaller pieces of equal size:")
  print (" -half [input file] [output file A] [output file B]")
  print (" ")
  print ("#SPLIT a file into smaller pieces of a specified size:")
  print (" -split [input file] [size in bits[M][K]] [output file base]")
  print (" ")
  print ("#TRUNCATE a file to a specified size:")
  print (" -trunc [input file] [size in bits[M][K]] [output file]")
  print (" ")
  print ("#PAD a file to a specified size using 0x00:")
  print (" -padz [input file] [size bits[M][K]] [output file]")
  print (" ")
  print ("#PAD a file to a specified size using 0xFF:")
  print (" -padf [input file] [size in bits[M][K]] [output file]")
  print (" ")
  print ("#CREATE A FILL file to a specified size using 0x00:")
  print (" -fillz [size in bits[M][K]] [output file]")
  print (" ")
  print ("#CREATE A FILL file to a specified size using 0xFF:")
  print (" -fillf [size in bits [M][K]] [output file]")
  print (" ")
  print ("#BYTESWAP a file:")
  print (" -byteswap [input file] [output file]")
  print (" ")
  print ("#WORDSWAP a file:")
  print (" -wordswap [input file] [output file]")
  print (" ")
  print ("#INTERLEAVE two 8-bit files into a one 16-bit file:")
  print (" -interleave [input file A] [input file B] [output file]")
  print (" ")
  print ("#DEINTERLEAVE one 16-bit file into two 8-bit files:")
  print (" -deinterleave [input file] [output file A] [output file B]")
  print (" ")