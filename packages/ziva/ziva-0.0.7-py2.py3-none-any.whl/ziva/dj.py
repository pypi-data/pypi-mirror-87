from binascii import hexlify, unhexlify
from textwrap import wrap

# t = """gÚ´RZ@¶'gÚð\x00RYï¶'gÛ,RZR¶'gÛhRZú¶'gÛ¤RZ~¶'gÛàRZ\x96¶'gÜ\x1cRYü¶'gÜXRZk¶'gÜ\x94RZx¶'gÜÐRZ\x96¶'gÝ\x0cRZÎ¶'gÝHR[1¶'gÝ\x844R[i¶'gÝÀR[\x00¶"""
# print (unhexlify(t))


# with open('data.jda', 'w', encoding='latin1') as f:
#     f.write(t)

def jda_to_dtv(filepath:str):
    with open(filepath, 'r', encoding='iso-8859-2') as f:
        lines = f.readlines()

    header_data = {}
    data = []
    for i, line in enumerate(lines):
        try:
            var = line.split('=')[0].strip()
            val = line.split('=')[1].strip()
            header_data[var] = val
        except IndexError:
            pass

        if line.strip() == '$HEADER END':
            data = lines[i+1:]
            break

    # print (header_data)
    data = "".join(data)
    data = wrap(data, 8)
    print (len(data))
    # print (len(data)/8)
    for i in data:
        print (i)
        # for i in line:
        #     ch.append(i)
    #
    # print (len(ch))
    # print(len(ch)/8)
    # for i in line[0:8]:
        #     print (dec(i))
            # print (unhexlify(i))

