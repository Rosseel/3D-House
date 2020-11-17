import os
import zipfile


def unzip():
    for folder, dirs, files in os.walk("/home/techpriest/Desktop/becode/SpaceEYE/DSM", topdown=False):
        for name in files:
            print(name)
            if name.endswith(".zip"):
                # print(os.path.join(folder, name))
                # unzip to folder and delete the zip file
                os.chdir(folder)
                print("folder",folder)
                print("name",name)
                zip_file = zipfile.ZipFile(os.path.join(folder, name))
                zip_file.extractall()
                zip_file.close()
                os.remove(os.path.join(folder, name))


