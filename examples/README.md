# gyp_convert

批量转换sdf为pdbq

使用方法:

1.使用此目录下的envrionment.yml安装环境
```bash
conda env create -f environment.yml
```
上述环境在windows下导出，linux推荐通过以下命令安装
```bash
conda create -c conda-forge --name gyp rdkit numpy scipy -y
conda activate gyp -y
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

3.后续如果有自定义的数据集，放在本目录下，进行转换的示例如下：
```bash
python wrap.py --data NPD
python wrap.py --data NPE
python wrap.py --data NPF
```
输出的文件将会分别放置于output_[dataset_name]/output_top1/output_pdbqt下