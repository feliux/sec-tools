# -*- coding: utf-8 -*-
import os
import time

if os.name == "nt":
    command = "dir"
else:
    command = "ls -l"

print(os.system(command))
for file in os.listdir("."):
    print(file)

cwd = os.getcwd()
print(cwd)
os.chdir("testing")
print(os.getcwd())
os.chdir(os.pardir)
print(os.getcwd())

os.makedirs("testing/path1/")
fp = open("testing/path1/file", "w")
fp.write("inspector")
fp.close()
print("Folder and file created...")
os.remove("testing/path1/file")
os.removedirs("testing/path1") # Delete empty folders
print("Folder and file deleted...")

os.mkdir("testing2")
os.rmdir("testing2")  # Delete 

file = "os1.py"
st = os.stat(file)
print("stat: ", file)
mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime = st
print("- created:", time.ctime(ctime))
print("- last accessed:", time.ctime(atime))
print("- last modified:", time.ctime(mtime))
print("- Size:", size, "bytes")
print("- owner:", uid, gid)
print("- mode:", oct(mode))
