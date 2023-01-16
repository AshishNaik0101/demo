import os
import stat
from distutils.dir_util import copy_tree

def model_replace():
    rootdir = r'D:\projects\VWH020Z0\work\dev\SCLX_model'

    for subdir, dirs, files in os.walk(rootdir): #iterate through folders
    for file in files: #iterate through subfolders
        file_name = os.path.join(subdir, file) #join subdirectory and file name
        os.chmod(file_name, stat.S_IWRITE) #remove read permissions 
        os.remove(file_name) #remove the file after removing read permissions

    copy_tree("D:\Jenkins\SCLX_model", "D:\projects\VWH020Z0\work\dev\SCLX_model") #replace synched model with existing model
    print("Replacement Done for Model Path")

model_replace() #function call
