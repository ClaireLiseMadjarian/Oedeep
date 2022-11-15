import os
import subprocess

from os import listdir
from os.path import isfile, join
mypath = r'C:\Users\jeronimo\OneDrive - IMT MINES ALES\Documents\3A\Oedeep\cbr_files'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
subprocess.run('set PATH=%PATH%;C:\Program Files\7-Zip', shell=True)
for file in onlyfiles:
    command = '7z e ".\cbr_files\\' + file + '" -o".\jpg_files" -y'
    print(command)
    #command = '7z e ".\cbr_files\Adventures_Into_Darkness_10__1953_06.Standard___c2c.Cimmerian32_.cbr" -o"..\jpg_files"'
    subprocess.run(
        command,
        shell=True)

print(onlyfiles)
exit()

