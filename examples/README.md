# gyp_convert

批量转换sdf为pdbq

使用方法:

1.使用此目录下的envrionment.yml安装环境
```bash
conda env create -f environment.yml
```
上述环境在windows下导出，linux推荐通过以下命令安装
```bash
conda create -c conda-forge --name gyp rdkit numpy scipy mpi4py -y
conda install tqdm
```

2.激活环境并测试
```bash
conda activate gyp
python wrap.py --data NPA
python wrap.py --data NPB
python wrap.py --data NPC
```
三条python命令可以在不同的终端运行。