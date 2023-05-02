import os
import shutil
import glob

output_dir = [x for x in os.listdir('.') if os.path.isdir(x) and 'output_' in x]

try:
    os.mkdir("output")
except:
    pass

for i in output_dir:
    for j in glob.glob(os.path.join(i,"output_top1","output_pdbqt","*__input_top1.pdbqt")):
        os.rename(j,os.path.join(i,"output_top","output_pdbqt",os.path.basename(j).split("__")[0]+"_gyp.pdbqt"))
    for j in glob.glob(os.path.join(i,"output_top1","output_pdbqt","*_gyp.pdbqt")):
        shutil.move(j,os.path.join("output",os.path.basename(j)))
        