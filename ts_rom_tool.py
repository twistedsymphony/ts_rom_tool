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
    raise ValueError("bits must be specified as an integer")
  return int(bits)*multiplier


def get_file_size(file_name):
  st = os.stat(file_name)
  return st.st_size


#checks that all of the arguments have been provided
def check_input_count(argv, count):
  if len(argv) <= count:
    print("too few arguments to perform operation")
    sys.exit(1)
  
  
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
def nibbleswap(input_file, output_file):
  def nibble_swap(byte: int) -> int:
    return ((byte & 0x0F) << 4) | ((byte & 0xF0) >> 4)

  with open(input_file, "rb") as infile, open(output_file, "wb") as outfile:
    while byte := infile.read(1):  # Read one byte at a time
      swapped_byte = nibble_swap(int.from_bytes(byte, "big"))
      outfile.write(bytes([swapped_byte]))


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


#interleaves three files by a specified number of bytes
def interleave24(input_file_a, input_file_b, input_file_c, output_file, bytes):
  with open(output_file, 'wb+') as outfile:
    with open(input_file_a, 'rb') as fa:
      with open(input_file_b, 'rb') as fb:
        with open(input_file_c, 'rb') as fc:
          chunk = fa.read(bytes)
          A = chunk
          chunk = fb.read(bytes)
          B = chunk
          chunk = fc.read(bytes)
          C = chunk
          while chunk:
            outfile.write(A)
            outfile.write(B)
            outfile.write(C)
            chunk = fa.read(bytes)
            A = chunk
            chunk = fb.read(bytes)
            B = chunk
            chunk = fc.read(bytes)
            C = chunk


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


#deinterleaves a 24-bit file into three files by a specified number of bytes
def deinterleave24(input_file, output_file_a, output_file_b, output_file_c, bytes):
  with open(output_file_a, 'wb+') as oa:
    with open(output_file_b, 'wb+') as ob:
      with open(output_file_c, 'wb+') as oc:
        with open(input_file, 'rb') as infile:
          chunk = infile.read(bytes)
          A = chunk
          chunk = infile.read(bytes)
          B = chunk
          chunk = infile.read(bytes)
          C = chunk
          while chunk:
            oa.write(A)
            ob.write(B)
            oc.write(C)
            chunk = infile.read(bytes)
            A = chunk
            chunk = infile.read(bytes)
            B = chunk
            chunk = infile.read(bytes)
            C = chunk


# ---------------------------------------------------------------------------
# IPS patch support
#
# IPS format:
#   "PATCH" header
#   records:  3-byte offset (big endian), 2-byte size
#             size > 0  -> [size] bytes of data follow
#             size == 0 -> RLE record: 2-byte run length, 1-byte value
#   "EOF" footer
#   optional 3-byte truncation size after "EOF" (common extension)
#
# Limits: offsets are 24-bit (files up to 16MB), records up to 0xFFFF bytes,
# and no record may start at offset 0x454F46 because it reads as "EOF".
# ---------------------------------------------------------------------------
IPS_HEADER = b'PATCH'
IPS_FOOTER = b'EOF'
IPS_EOF_OFFSET = 0x454F46
IPS_MAX_OFFSET = 0xFFFFFF
IPS_MAX_RECORD = 0xFFFF
IPS_RECORD_OVERHEAD = 5   # 3-byte offset + 2-byte size
IPS_RLE_SIZE = 8          # 3-byte offset + 2-byte zero + 2-byte count + 1-byte value


class IPSError(Exception):
  pass


#builds IPS patch data (bytes) that turns source_data into target_data
def make_ips(source_data, target_data):
  src = bytes(source_data)
  tgt = bytes(target_data)
  src_len = len(src)
  tgt_len = len(tgt)
  if tgt_len > IPS_MAX_OFFSET + 1:
    raise IPSError("target file is larger than 16MB, which IPS cannot address")

  out = bytearray(IPS_HEADER)

  def differs(i):
    return i >= src_len or src[i] != tgt[i]

  def write_raw(offset, data):
    # a record can't start at the "EOF" offset; back up one byte instead
    if offset == IPS_EOF_OFFSET:
      offset -= 1
      data = tgt[offset:offset + 1] + data
    while data:
      n = min(len(data), IPS_MAX_RECORD)
      if offset + n == IPS_EOF_OFFSET and n < len(data):
        # don't let the next record start at the "EOF" offset
        n = n - 1 if n > 1 else 2
      out.extend(offset.to_bytes(3, 'big'))
      out.extend(n.to_bytes(2, 'big'))
      out.extend(data[:n])
      offset += n
      data = data[n:]

  def write_rle(offset, count, value):
    if offset == IPS_EOF_OFFSET:
      write_raw(offset, bytes([value]))
      offset += 1
      count -= 1
    while count > 0:
      n = min(count, IPS_MAX_RECORD)
      if offset + n == IPS_EOF_OFFSET and n < count:
        n -= 1
      out.extend(offset.to_bytes(3, 'big'))
      out.extend(b'\x00\x00')
      out.extend(n.to_bytes(2, 'big'))
      out.append(value)
      offset += n
      count -= n

  def write_region(start, end):
    # split a changed region into raw and RLE records, whichever is smaller
    raw_start = start
    i = start
    while i < end:
      j = i + 1
      while j < end and tgt[j] == tgt[i]:
        j += 1
      run = j - i
      # an RLE in the middle of a region costs an extra record header
      at_edge = (i == raw_start) or (j == end)
      threshold = IPS_RLE_SIZE if at_edge else IPS_RLE_SIZE + IPS_RECORD_OVERHEAD
      if run > threshold:
        if raw_start < i:
          write_raw(raw_start, tgt[raw_start:i])
        write_rle(i, run, tgt[i])
        raw_start = j
      i = j
    if raw_start < end:
      write_raw(raw_start, tgt[raw_start:end])

  i = 0
  while i < tgt_len:
    if not differs(i):
      i += 1
      continue
    start = i
    end = i + 1
    while end < tgt_len:
      if differs(end):
        end += 1
        continue
      # bridge short runs of unchanged bytes: cheaper than a new record header
      gap = end
      while gap < tgt_len and not differs(gap) and gap - end < IPS_RECORD_OVERHEAD:
        gap += 1
      if gap < tgt_len and differs(gap):
        end = gap
      else:
        break
    write_region(start, end)
    i = end

  out.extend(IPS_FOOTER)
  if tgt_len < src_len:
    out.extend(tgt_len.to_bytes(3, 'big'))
  return bytes(out)


#applies IPS patch data (bytes) to source_data and returns the patched bytes
def apply_ips_patch(source_data, patch_data):
  data = bytearray(source_data)
  patch = bytes(patch_data)
  if patch[:5] != IPS_HEADER:
    raise IPSError("not an IPS file (missing PATCH header)")
  pos = 5
  plen = len(patch)
  while True:
    if pos + 3 > plen:
      raise IPSError("IPS file ended without an EOF marker")
    if patch[pos:pos + 3] == IPS_FOOTER:
      pos += 3
      break
    offset = int.from_bytes(patch[pos:pos + 3], 'big')
    pos += 3
    if pos + 2 > plen:
      raise IPSError("IPS record truncated at offset 0x%06X" % offset)
    size = int.from_bytes(patch[pos:pos + 2], 'big')
    pos += 2
    if size == 0:
      if pos + 3 > plen:
        raise IPSError("IPS RLE record truncated at offset 0x%06X" % offset)
      count = int.from_bytes(patch[pos:pos + 2], 'big')
      chunk = patch[pos + 2:pos + 3] * count
      pos += 3
    else:
      if pos + size > plen:
        raise IPSError("IPS record data truncated at offset 0x%06X" % offset)
      chunk = patch[pos:pos + size]
      pos += size
    end = offset + len(chunk)
    if end > len(data):
      data.extend(b'\x00' * (end - len(data)))
    data[offset:end] = chunk
  # optional truncation extension
  if pos + 3 <= plen:
    del data[int.from_bytes(patch[pos:pos + 3], 'big'):]
  return bytes(data)


#creates an IPS patch file from a source file and a target file
def ips_create(source_file, target_file, output_file):
  with open(source_file, 'rb') as f:
    src = f.read()
  with open(target_file, 'rb') as f:
    tgt = f.read()
  patch = make_ips(src, tgt)
  with open(output_file, 'wb') as outfile:
    outfile.write(patch)
  return patch


#applies an IPS patch file to a source file and writes the patched file
def ips_apply(source_file, ips_file, output_file):
  with open(source_file, 'rb') as f:
    src = f.read()
  with open(ips_file, 'rb') as f:
    patch = f.read()
  result = apply_ips_patch(src, patch)
  with open(output_file, 'wb') as outfile:
    outfile.write(result)
  return result


def print_help():
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
  print ("#NIBBLESWAP a file (4bits with next 4bits):")
  print (" -nibbleswap [input file] [output file]")
  print (" ")
  print ("#BYTESWAP a file (8bits with next 8bits):")
  print (" -byteswap [input file] [output file]")
  print (" ")
  print ("#WORDSWAP a file (16bits with next 16bits):")
  print (" -wordswap [input file] [output file]")
  print (" ")
  print ("#INTERLEAVE two 8-bit files into a one 16-bit file:")
  print (" -interleave [input file A] [input file B] [output file]")
  print (" ")
  print ("#DEINTERLEAVE one 16-bit file into two 8-bit files:")
  print (" -deinterleave [input file] [output file A] [output file B]")
  print (" ")
  print ("#INTERLEAVE(24-bit) three 8-bit files into a one 24-bit file:")
  print (" -interleave24 [input file A] [input file B] [input file C] [output file]")
  print (" ")
  print ("#DEINTERLEAVE(24-bit) one 24-bit file into three 8-bit files:")
  print (" -deinterleave24 [input file] [output file A] [output file B] [output file C]")
  print (" ")
  print ("#CREATE an IPS patch from a source file and a modified target file:")
  print (" -ipscreate [source file] [target file] [output .ips file]")
  print (" ")
  print ("#APPLY an IPS patch to a source file:")
  print (" -ipsapply [source file] [.ips file] [output file]")
  print (" ")


def main(argv=None):
  if argv is None:
    argv = sys.argv
  process = '-help'
  if len(argv) > 1:
    process = argv[1]

  try:
    if process == '-split':
      check_input_count(argv, 4)
      split(argv[2], argv[3], argv[4])
    elif process == '-half':
      check_input_count(argv, 4)
      half(argv[2], argv[3], argv[4])
    elif process == '-concat':
      check_input_count(argv, 4)
      concat([argv[2], argv[3]], argv[4])
    elif process == '-multiconcat':
      check_input_count(argv, 4)
      concat(argv[3:], argv[2])
    elif process == '-trunc':
      check_input_count(argv, 4)
      truncate(argv[2], argv[3], argv[4])
    elif process == '-padz': #0 pad
      check_input_count(argv, 4)
      pad(argv[2], argv[3], argv[4], b'\x00')
    elif process == '-padf': #F pad
      check_input_count(argv, 4)
      pad(argv[2], argv[3], argv[4], b'\xFF')
    elif process == '-fillz': #0 filled file
      check_input_count(argv, 3)
      fill(argv[2], argv[3], b'\x00')
    elif process == '-fillf': #F filled file
      check_input_count(argv, 3)
      fill(argv[2], argv[3], b'\xFF')
    elif process == '-interleave':
      check_input_count(argv, 4)
      interleave(argv[2], argv[3], argv[4], 1)
    elif process == '-interleave24':
      check_input_count(argv, 5)
      interleave24(argv[2], argv[3], argv[4], argv[5], 1)
    elif process == '-deinterleave':
      check_input_count(argv, 4)
      deinterleave(argv[2], argv[3], argv[4], 1)
    elif process == '-deinterleave24':
      check_input_count(argv, 5)
      deinterleave24(argv[2], argv[3], argv[4], argv[5], 1)
    elif process == '-byteswap':
      check_input_count(argv, 3)
      swap(argv[2], argv[3], 1)
    elif process == '-wordswap':
      check_input_count(argv, 3)
      swap(argv[2], argv[3], 2)
    elif process == '-nibbleswap':
      check_input_count(argv, 3)
      nibbleswap(argv[2], argv[3])
    elif process == '-ipscreate':
      check_input_count(argv, 4)
      ips_create(argv[2], argv[3], argv[4])
    elif process == '-ipsapply':
      check_input_count(argv, 4)
      ips_apply(argv[2], argv[3], argv[4])
    else: #help
      print_help()
  except (ValueError, IPSError, OSError) as e:
    print("error: " + str(e))
    sys.exit(1)


if __name__ == '__main__':
  main()
