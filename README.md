#twistedsymphony's ROM Tool
# 2020-01-11 twistedsymphony solid-orange.com

This tool allows you to separate, combine and modify ROM files from a command line in a number of ways
It requires Python 3.x to be installed.

commands with a size parameter should be specified as an integer followed by an M or a K
for example 16M will specify the correct size for a 27C160 EPROM and 512K will specify the correct size for a 27C512 EPROM

Here are the Available Commands:

#HELP displays the below commands

 -help
 
 
#CONCATENATE two files together:

 -concat [input file A] [input file B] [output file]
 
 
#CONCATENATE two or more files together:


 -multiconcat [output file] [input file 1] [input file 2] [input file n]...
 
#SPLIT a file into smaller pieces of a specified size:

 -split [input file] [size in bits[M][K]] [output file base]
 
 
#TRUNCATE a file to a specified size:

 -trunc [input file] [size in bits[M][K]] [output file]
 
 
#PAD a file to a specified size using 0x00:

 -padz [input file] [size bits[M][K]] [output file]
 
 
#PAD a file to a specified size using 0xFF:

 -padf [input file] [size in bits[M][K]] [output file]
 
 
#CREATE A FILL file to a specified size using 0x00:

 -fillz [size in bits[M][K]] [output file]
 
 
#CREATE A FILL file to a specified size using 0xFF:

 -fillf [size in bits [M][K]] [output file]
 
 
#BYTESWAP a file:

 -byteswap [input file] [output file]
 
 
#WORDSWAP a file:

 -wordswap [input file] [output file]
 
 
#INTERLEAVE two 8-bit files into a one 16-bit file:

 -interleave [input file A] [input file B] [output file]
 
 
#DEINTERLEAVE one 16-bit file into two 8-bit files:

 -deinterleave [input file] [output file A] [output file B]
 
 
#CREATE an IPS patch from a source file and a modified target file:

 -ipscreate [source file] [target file] [output .ips file]
 
 
#APPLY an IPS patch to a source file:

 -ipsapply [source file] [.ips file] [output file]
 
IPS notes: patches use RLE records where they save space, and if the target is smaller
than the source the patch includes the common 3-byte truncation extension after "EOF".
IPS can only address files up to 16MB.


#USING AS A MODULE

ts_rom_tool.py can be imported into another Python script; importing it does not print
anything or run a command. Every operation is available as a function, for example:

 import ts_rom_tool
 ts_rom_tool.ips_create('original.bin', 'modified.bin', 'patch.ips')
 ts_rom_tool.ips_apply('original.bin', 'patch.ips', 'patched.bin')

 # or work on bytes in memory
 patch = ts_rom_tool.make_ips(original_bytes, modified_bytes)
 patched = ts_rom_tool.apply_ips_patch(original_bytes, patch)

 # run any command-line operation from code
 ts_rom_tool.main(['ts_rom_tool.py', '-wordswap', 'in.bin', 'out.bin'])

Invalid sizes raise ValueError and bad IPS files raise ts_rom_tool.IPSError.
