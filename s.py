#!/usr/bin/python

import sys
from binascii import unhexlify as unhex

lines = []
with open(sys.argv[1], 'r') as f:
  lines = [l.rstrip('\n') for l in f]

labels = {}
instructions = []

adj = 0
# I hate this with a passion
# I've coded myself in a very nasty corner
# AAAAAAAAAAAAAAAAAAAAAAAAAAA
for index in range(0, len(lines)):
  if lines[index] == "":
    adj += 2
    continue
  if lines[index][0] == ":":
    labels[lines[index][1:]] = 2*(index)-adj
    adj += 2
  else:
    instructions.append(lines[index])

def padl(s, l):
  return "0"*(l-len(s))+s

outb = []
for i in range(0, 512):
  outb.append(bytes(unhex('00')))
adj = -510

for x in instructions:
  y = x.split(' ')
  opcode = y[0]
  if opcode[:2] == "LD":
    outb.append(bytes(unhex("6" + opcode[2]),))
    outb.append(bytes(unhex(padl(y[1], 2))))
  elif opcode == "STO":
    if y[1] in labels:
      t ="A"+padl(hex(labels[y[1]]-adj)[2:], 3)
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
      t ="1"+padl(hex(labels[y[1]]-adj)[2:], 3)
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
    towrite = ' '.join(y[j] for j in range(1, len(y)))
    adj += len(towrite)-2
    for i in towrite:
      outb.append(bytes(i, 'ascii'))
  elif opcode == "NOP":
    outb.append(bytes(unhex("00")))
    outb.append(bytes(unhex("E0")))
  elif opcode == "RET":
    outb.append(bytes(unhex("00")))
    outb.append(bytes(unhex("EE")))
  elif opcode == "CAL":
    if y[1] in labels:
      t ="2"+padl(hex(labels[y[1]]-adj)[2:], 3)
      outb.append(bytes(unhex(t[:2]),))
      outb.append(bytes(unhex(t[2:]),))
    else:
      t ="2"+padl(y[1], 3)
      outb.append(bytes(unhex(t[:2]),))
      outb.append(bytes(unhex(t[2:]),))
  elif opcode[3:] == "SKN":
    outb.append(bytes(unhex("3" + opcode[3]),))
    outb.append(bytes(unhex(padl(y[1], 2))))
  elif opcode == "SET":
    t ="8"+ y[1] + y[2] + "0"
    outb.append(bytes(unhex(t[:2]),))
    outb.append(bytes(unhex(t[2:]),))
  elif opcode == "OR":
    t ="8"+ y[1] + y[2] + "1"
    outb.append(bytes(unhex(t[:2]),))
    outb.append(bytes(unhex(t[2:]),))
  elif opcode == "AND":
    t ="8"+ y[1] + y[2] + "2"
    outb.append(bytes(unhex(t[:2]),))
    outb.append(bytes(unhex(t[2:]),))
  elif opcode == "XOR":
    t ="8"+ y[1] + y[2] + "3"
    outb.append(bytes(unhex(t[:2]),))
    outb.append(bytes(unhex(t[2:]),))
  elif opcode == "ADD":
    t ="8"+ y[1] + y[2] + "4"
    outb.append(bytes(unhex(t[:2]),))
    outb.append(bytes(unhex(t[2:]),))
  elif opcode == "SUB":
    t ="8"+ y[1] + y[2] + "5"
    outb.append(bytes(unhex(t[:2]),))
    outb.append(bytes(unhex(t[2:]),))
  elif opcode == "RSH":
    t ="8"+ y[1] + "06"
    outb.append(bytes(unhex(t[:2]),))
    outb.append(bytes(unhex(t[2:]),))
  elif opcode == "SUBC":
    t ="8"+ y[2] + y[1] + "7"
    outb.append(bytes(unhex(t[:2]),))
    outb.append(bytes(unhex(t[2:]),))
  elif opcode == "LSH":
    t ="8"+ y[1] + "0E"
    outb.append(bytes(unhex(t[:2]),))
    outb.append(bytes(unhex(t[2:]),))

with open(sys.argv[2], 'wb') as w:
  for i in outb:
    w.write(i)
