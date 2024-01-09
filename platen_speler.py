import struct
from binascii import  hexlify

outpdir="./audio_platen_spelertje/"
r=open('platen_spelertje.bin','rb').read()
nr_blocks=struct.unpack("I",r[8:12])[0]
print(nr_blocks)
ptrs=[]
conf=[]
lenblock=[]
p=16
for block in range(nr_blocks):
    conf.append(struct.unpack("H",r[p:p+2])[0])
    p+=2
    ptrs.append(struct.unpack("I",r[p:p+4])[0])
    p+=6
    k=0
for i in range(len(conf)):
    print("%04X %08X"%(conf[i],ptrs[i]))
    print("%08X"%(ptrs[i]-k))
    lenblock.append(ptrs[i]-k)
    k=ptrs[i]
lenblock.append(len(r)-ptrs[len(conf)-1])

for i in range(len(conf)):
    with open(outpdir+'snd_%06x.bin'%ptrs[i],'wb') as f:
        f.write(r[ptrs[i]:ptrs[i]+lenblock[i+1]])


for i,ptr in enumerate(ptrs):
    print(hexlify(r[ptr-10:ptr]),"%08x %08x"%(ptrs[i],lenblock[i+1]),' '.join(["%02X"%i for i in r[ptr:ptr+20]]))
