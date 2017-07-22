import sys
import struct

f = open(sys.argv[1], 'rb')

i = 0

def is_all(it, e):
  for a in it:
    if a != e:
      return False
  return True

unused = 0
deleted = 0
dontknow = 0
inuse = 0
isresident = 0

kind = []

while True:
  #print f.read(0x38).encode('hex')
  #print 'next'
  #print f.read(4).encode('hex')
  #break
  b = f.read(4)
  if b.decode('ascii') != 'FILE' or not b:
    print 'izer', i
    print 'unused', unused
    print 'deleted', deleted
    print 'dontknown', dontknow
    print 'inuse', inuse
    print 'kind', kind
    print 'resident', isresident
    break
  print 'tell', f.tell()
  print b.decode('ascii')
  f.seek(f.tell() + (0x16 - 4))
  flag = f.read(2)
  print flag.encode('hex')
  if flag.encode('hex') not in ['0100', '0200']:
    if not flag.encode('hex') in kind:
      kind.append(flag.encode('hex'))
    if flag.encode('hex') == '0000':
      deleted += 1
    else:
      dontknow += 1
  else:
    inuse += 1
  f.seek(f.tell() + (0x38 - (0x16 + 2)))

  attr_type, = struct.unpack('<I', f.read(4))
  attr_length, = struct.unpack('<I', f.read(4))
  attr_resident, = struct.unpack('<B', f.read(1))
  #f.seek(f.tell() + (attr_length - 9))
  print 'ty', hex(attr_type)
  print 'len', hex(attr_length)
  if attr_type == 0xB0:
    print attr_length
    break
  if attr_type == 0x80 and attr_resident == 0:
    isresident += 1
  while attr_type != 0xB0 and attr_type in [0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70, 0x80, 0x90, 0xA0, 0xB0, 0xC0, 0xD0, 0xE0, 0x100]:#0x10 <= attr_type <= 0x100:
    f.seek(f.tell() + (attr_length - 9))
    attr_type, = struct.unpack('<I', f.read(4))
    if attr_type == 0x20:
      attr_length, = struct.unpack('<H', f.read(2))
    else:
      attr_length, = struct.unpack('<I', f.read(4))
    if attr_type == 0xB0:
      print attr_length
      break
    attr_resident, = struct.unpack('<B', f.read(1))
    if attr_type == 0x80 and attr_resident == 0:
      isresident += 1
    print '  ty', hex(attr_type)
    print '  len', attr_length
    print '  res', attr_resident
    print '  tell', f.tell()
    print '  diff', attr_length - 9
    #print 'tell', type(attr_length), attr_length,(attr_length - 9)
    #f.seek(f.tell() + (attr_length - 9))
  print 'attr_typ', hex(attr_type)
  print 'attr_length', hex(attr_length)
  print 'attr_resident', hex(attr_resident)
  #f.seek(f.tell() + (0xF2 - (0x30 + 10)))
  #name = f.read(100)
  #break
  #print len(name.encode('hex'))
  #print [s for s in name.encode('hex')]
  #print is_all(name.encode('hex'), '0')
  #if is_all(name.encode('hex'), '0'):
  #  unused += 1
  #print name.decode('utf-8', 'ignore')
  #f.seek(f.tell() + ((0x1B0) - (0xF2 + 100)))
  #resident = f.read(10)

  #print resident.encode('hex')
#  if not resident.encode('hex') in ['00', '01']:
#    break
  i += 1
  print f.tell() % 1024
  #if i == 2:
  #  break
  f.seek(f.tell() + (1024 - (f.tell() % 1024)))#((0x1B0) + 10)))
