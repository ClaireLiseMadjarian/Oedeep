import rarfile as rarfile
import os

rarfile.UNRAR_TOOL = r"C:\Users\jeronimo\Downloads\unrarw32.exe"
direct = r"C:\Users\jeronimo\OneDrive - IMT MINES ALES\Documents\3A\Oedeep\cbr_files"


for filename in os.listdir(direct):
    rf = rarfile.RarFile(direct+"/"+filename)
    try:
        rf.extractall()
    except:
        print("Error! "+filename+" cannot be extracted!")

print("--------------------------------------------------")