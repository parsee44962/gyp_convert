import glob
import os
import json
import subprocess
from tqdm import tqdm
import shutil
import argparse
from rdkit import Chem
from rdkit.Chem import AllChem


def update_json(source, path, output=None):
    with open(source, "+r") as f:
        json_str = f.read()
        json_obj = json.loads(json_str)
        json_obj["source"] = path
        if output != None:
            json_obj["output_folder"] = output
        new_json_str = json.dumps(json_obj)
        f.seek(0)
        f.write(new_json_str)
        f.truncate()


def run_gyp(source):
    cmd = ["python", "../run_gypsum_dl.py", "-j", source]
    subprocess.run(cmd, timeout=10 * 60)


def after_process(i, state):
    print(i + "\t" + state)
    with open("run.log", "a") as f:
        f.write(f"{os.path.basename(i).split('.')[0]}" + "\t" + state + "\n")


def run_pdbqt(path, output_path):
    shutil.copy("../../rdkit2pdbqt.py", ".")
    cmd = ["python", "rdkit2pdbqt.py", "-l", path]

    with open(
        os.path.join(output_path, os.path.basename(path).split(".")[0] + ".pdbqt"), "w"
    ) as f:
        subprocess.run(cmd, stdout=f)


parser = argparse.ArgumentParser()
parser.add_argument("--data", type=str, help="data path")
args = parser.parse_args()
path = str(args.data)


output_path = "output" + f"_{path}"
source = os.path.join(path, "t.json")
shutil.copy("t.json", source)
update_json(source, None, output=output_path)


try:
    os.mkdir(output_path)
except:
    pass

dataset = glob.glob(os.path.join(path, "*.sdf"))

##Gyp 2d -> 3d
for i in tqdm(dataset):
    update_json(source, i)
    try:
        os.mkdir(os.path.join(path, os.path.basename(path) + "_jumped"))
        os.mkdir(os.path.join(path, os.path.basename(path) + "_C"))
    except:
        pass
    try:
        run_gyp(source)
    except KeyboardInterrupt:
        print("Exit the program(y) or Jump out of this loop(anything else)\n")
        if input() == "y":
            exit()
        else:
            after_process(i, "Jumped")
            shutil.move(
                i,
                os.path.join(
                    os.path.join(path, os.path.basename(path) + "_jumped"),
                    os.path.basename(i),
                ),
            )
            continue
    except subprocess.TimeoutExpired:
        print("Timeout!")
        after_process(i, "Timeout!")
        shutil.move(
            i,
            os.path.join(
                os.path.join(path, os.path.basename(path) + "_jumped"),
                os.path.basename(i),
            ),
        )
        continue
    except:
        after_process(i, "Convert Error")
        continue
    else:
        after_process(i, "Completed")
        shutil.move(
            i,
            os.path.join(
                os.path.join(path, os.path.basename(path) + "_C"), os.path.basename(i)
            ),
        )


## Caculate energy and only take no.1
os.chdir(output_path)
new_sdf = glob.glob("*.sdf")
try:
    os.mkdir("output_top1")
except:
    pass

for filename in tqdm(new_sdf):
    if filename == "gypsum_dl_params.sdf":
        continue
    try:
        suppl = Chem.SDMolSupplier(filename)
    except:
        with open("run.log", "a") as f:
            f.write(filename + "\t" + "can not read this mol" + "\n")
        continue

    ##caculate
    energies = {}
    for i, mol in enumerate(suppl):
        if mol is not None:
            try:
                mol = Chem.AddHs(mol)
                pro = Chem.rdForceFieldHelpers.MMFFGetMoleculeProperties(mol)
                ff = AllChem.MMFFGetMoleculeForceField(mol, pro)
                energies[i] = ff.CalcEnergy()
            except:
                with open("run.log", "a") as f:
                    f.write(filename + "\t" + "can not caculate energy" + "\n")
                continue

    sorted_energies = sorted(energies.items(), key=lambda x: x[1])
    mol = suppl[sorted_energies[0][0]]
    Chem.MolToMolFile(mol, filename.split(".")[0].split("__")[0] + "_top1.sdf")

for i in glob.glob("*_top1.sdf"):
    shutil.move(i, os.path.join("output_top1", os.path.basename(i)))


##Convert to pdbqt
os.chdir("output_top1")
try:
    os.mkdir("output_pdbqt")
except:
    pass
new_sdf = glob.glob("*.sdf")
for i in tqdm(new_sdf):
    try:
        run_pdbqt(i, "output_pdbqt")
    except:
        with open("run.log", "a") as f:
            f.write(filename + "\t" + "can not convert to pdbqt" + "\n")
        continue
