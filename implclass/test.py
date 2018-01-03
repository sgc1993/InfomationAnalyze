import sys
BasePath = sys.path[0]
print(sys.path)
import os
print(os.path.sep)

sep = os.path.sep
print(type(sep))
if os.path.exists("..%saa%stest.txt"%(sep,sep)):
    print("success")
file = open("..%sfile%stest.txt"%(sep,sep),'w',encoding='UTF-8')
file.write("success")
print("dad")