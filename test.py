
### pip install filesystempro
import filesystem as fs
from filesystem import wrapper as wr

obj_folder = wr.create_directory(f'{fs.documents}/FolderOBJ')
print(obj_folder)

print("\n")

obj_file = wr.create_file("Shopping.txt", fs.documents, "Gone")
print(obj_file["name"])


# ### Creates a database folder
# db_folder = f'{fs.documents}/database'
# wr.create_directory(db_folder) # If folder already exists, it does nothing

# ### Creates zipfiles folder
# zip_folder = f'{fs.documents}/zipfiles'
# wr.create_directory(zip_folder) # If folder already exists, it does nothing

# ### Gets reference to the folder that will be compressed
# source = db_folder
# ### Sets the destination to the file after compression
# destination = f'{zip_folder}/testfile.zip'

# ### Makes a ".zip" file
# wr.make_zip(source, destination)

# myJoin = wr.join(f'{fs.documents}/', "MinhaPastaEmDocuments")
# doc_folders = wr.list_directories(f'{fs.documents}/')
# download_files = wr.list_files(f'{fs.downloads}/')

# print(myJoin)
# print(doc_folders)
# print(download_files)

# print(wr.combine_path('c:\\temp', 'subdir\\file.txt'))
# print(wr.combine_path('', 'subdir\\file.txt'))
# print(wr.combine_path(fs.documents, fs.desktop))
# print(wr.combine_path(f'{fs.documents}/', f'{fs.desktop}/'))

# print(wr.combine_path('c:\\temp.txt', 'subdir\\file.txt'))
# print(wr.combine_path('c:\\temp.txt', 'subdir\\file.txt'))  # Saída: 'c:\\temp.txt\\subdir\\file.txt'
# print(wr.combine_path(f'{fs.documents}', 'subdir\\file.txt'))

# saved_games = wr.combine_path(f'{fs.documents}', "Saved")
# print(saved_games)
# wr.create_directory(saved_games)

# lib = wr.combine_path(paths=[fs.documents, "Saved", "folder1", "folder2"])
# lib = wr.combine_path(paths=[f'{fs.documents}/', "Saved", "folder1", "folder2"])
# print(lib)
# aaa = wr.combine_path(f'{fs.pictures}', "Path1")
# print(aaa)
# aaa = wr.combine_path(f'{fs.pictures}/', "Path2")
# print(aaa)
# aaa = wr.combine_path(f'{fs.pictures}', "/Path3")
# print(aaa)
# aaa = wr.combine_path(f'{fs.pictures}/', "/Path4")
# print(aaa)

# wr.create_directory(aaa)

# print(lib)






# ### pip install filesystempro
# import filesystem as fs
# from filesystem import wrapper as wr

# ### Creates a database folder
# db_folder = f'{fs.documents}/database'
# wr.create_directory(db_folder) # If folder already exists, it does nothing

# ### Creates zipfiles folder
# zip_folder = f'{fs.documents}/zipfiles'
# wr.create_directory(zip_folder) # If folder already exists, it does nothing

# ### Makes a ".zip" file
# wr.make_zip(source = db_folder, destination = f'{zip_folder}/testfile.zip')










# ### pip install filesystempro
# import filesystem as fs
# from filesystem import wrapper as wr

# ### Creates a database folder
# db_folder = f'{fs.documents}/database'
# wr.create_directory(db_folder) # If folder already exists, it does nothing

# ### Creates zipfiles folder
# zip_folder = f'{fs.documents}/zipfiles'
# wr.create_directory(zip_folder) # If folder already exists, it does nothing

# ### Makes a ".zip" file
# wr.make_zip(db_folder, f'{zip_folder}/testfile.zip')