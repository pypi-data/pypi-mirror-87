import collections
import sys

file1 = sys.argv[1]
file2 = sys.argv[2]

content1 = open(file1, 'r', encoding='cp855').read()
content2 = open(file2, 'r', encoding='cp855').read()

cnt1 = collections.Counter(content1)
cnt2 = collections.Counter(content2)

for key, val in cnt1.items():
    if val != cnt2[key]:
        print (f'Difference key:{repr(key)} file1:{val}, file2:{cnt2[key]}')
