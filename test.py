
### pip install filesystempro
import filesystem as fs
import os
from filesystem import wrapper as wr
from filesystem import storage as st

# p1 = fs.documents
# p2 = "media"
# p3 = "images"

# Combine paths
result = wr.join('home', 'user', 'directory', 'file.txt')
print(result)  # Outputs: 'home/user/directory/file.txt'

# Use the paths parameter
result = wr.join(paths=['home', 'user', 'directory', 'file.txt'])
print(result)  # Outputs: 'home/user/directory/file.txt'

f = wr.get_files
combined = wr.combine(fs.documents)
print(combined)
combined = wr.combine(fs.documents, "media")
print(combined)
combined = wr.combine(fs.documents, "media", "images")
print(combined)
combined = wr.combine(fs.documents, "media", "images", "France")
print(combined)
combined = wr.combine(fs.documents, "media", "images", "France", "1")
print(combined)
combined = wr.combine(fs.documents, "media", "images", "France", "1", "2")
print(combined)
combined = wr.combine(fs.documents, "media", "images", "France", "1", "2", "3")
print(combined)
combined = wr.combine(fs.documents, "media", "images", "France", "1", "2", "3", "4")
print(combined)

combined = wr.combine(paths=["/home/You/Documents", "A", "B", "C"])
print(combined)
combined = wr.combine(fs.documents, "", "media", "images")
print(combined)
combined = wr.combine(fs.documents, "2001", "media", "images")
print(combined)
combined = wr.combine(fs.documents, "subdir\\file.txt")
print(combined)
combined = wr.combine(fs.documents, "2001", "media", "images", "AAA")
print(combined)
combined = wr.combine(fs.documents, "/2001", "/2002")
print(combined)
combined = wr.combine("users/YOU/Documents", "Summer23")
print(combined)

list_dir = [fs.documents, "1", "2", "3"]
combined = wr.combine(paths = list_dir)
print(combined)

print("Arr Func1")
# doc_work = wr.join(paths = [fs.documents, "Work", "shopping.xlsx"])
# print(doc_work)

# print("Func 1")
# var = wr.join(path1 = "System", paths = ["1", "2", "3"])
# print(var)

# print("Func 2")
# var = wr.join(path1 = "System", path2="Ameixa/",paths = ["1", "2", "3"])
# print(var)

# print("Func 3")
# var = wr.join(path1 = "System", path2="Ameixa/", path3="Jose", paths = ["1", "2", "3"])
# print(var)

# print("Func 4")
# var = wr.join(path1 = "System", path2="Ameixa/", path3="Jose", path4="Japao", paths = ["1", "2", "3"])
# print(var)


# Create a file

# bytes_to_mb = st.convert_file_size(obj_file["size"], "mb")
# print(bytes_to_mb)
# bytes_to_gb = st.convert_file_size(obj_file["size"], "MB", True)
# print(bytes_to_gb)
# print(wr.convert_file_size(obj_file["size"]))
# Get attribute values into variables

# Name = ""
# name_and_extension = ""
# size = ""
# abspath = ""
# dir_name = ""
# access = ""
# created = ""
# AAAA = ""
# AAAA = ""
# AAAA = ""

# print("File Name:", obj_file["name_without_extension"])
# print("File Name and Extension:", obj_file["name"])
# print("File Size:", obj_file["size"])
# print("File Absolute Path:", obj_file["abspath"])
# print("File Directory Name:", obj_file["dirname"])
# print("File Access:", obj_file["access"])
# print("File Created:", obj_file["created"])

# Get info from a file