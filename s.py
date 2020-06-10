#!/usr/bin/python

import sys
from binascii import unhexlify as unhex

lines = []
with open(sys.argv[1], 'r') as f:
  lines = [l.rstrip('\n') for l in f]

labels = {}
instructions = []

adj = 0
for index in range(0, len(lines)):
  if lines[index][0] == ":":
    labels[lines[index][1:]] = 2*(index)-adj
    adj += 2
  else:
    instructions.append(lines[index])

outb = []

def padl(s, l):
  return "0"*(l-len(s))+s

for x in instructions:
  y = x.split(' ')
  opcode = y[0]
  if opcode[:2] == "LD":
    outb.append(bytes(unhex("6" + opcode[2]),))
    outb.append(bytes(unhex(padl(y[1], 2))))
  elif opcode == "STO":
    if y[1] in labels:
      t ="A"+padl(hex(labels[y[1]])[2:], 3)
      outb.append(bytes(unhex(t[:2]),))
      outb.append(bytes(unhex(t[2:]),))
    else:
      t ="A"+padl(y[1], 3)
      outb.append(bytes(unhex(t[:2]),))
      outb.append(bytes(unhex(t[2:]),))
  elif opcode[:2] == "AD":
    if opcode[2] == "I":
      outb.append(bytes(unhex("F" + opcode[3])))
      outb.append(bytes(unhex("1E")))
    else:
      outb.append(bytes(unhex("7" + opcode[2]),))
      outb.append(bytes(unhex(padl(y[1], 2))))
  elif opcode == "PRNT":
    outb.append(bytes(unhex("D0")))
    outb.append(bytes(unhex("00")))
  elif opcode == "DUMP":
    outb.append(bytes(unhex("F" + y[1])))
    outb.append(bytes(unhex("55")))
  elif opcode == "LOAD":
    outb.append(bytes(unhex("F" + y[1])))
    outb.append(bytes(unhex("65")))
  elif opcode[:3] == "SKE":
    if len(opcode) == 3:
      pass
    else:
      outb.append(bytes(unhex("3" + opcode[3]),))
      outb.append(bytes(unhex(padl(y[1], 2))))
  elif opcode == "JMP":
    if y[1] in labels:
      t ="1"+padl(hex(labels[y[1]])[2:], 3)
      outb.append(bytes(unhex(t[:2]),))
      outb.append(bytes(unhex(t[2:]),))
    else:
      t ="1"+padl(y[1], 3)
      outb.append(bytes(unhex(t[:2]),))
      outb.append(bytes(unhex(t[2:]),))
  elif opcode == "HLT":
    outb.append(bytes(unhex("00")))
    outb.append(bytes(unhex("00")))
  elif opcode == "DSTR":
    for i in ' '.join(y[j] for j in range(1, len(y))):
      outb.append(bytes(i, 'ascii'))

with open(sys.argv[2], 'wb') as w:
  for i in outb:
    w.write(i)
