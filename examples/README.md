# gyp_convert

批量转换sdf为pdbq

使用方法：
1.使用此目录下的envrionment.yml安装环境
'''bash
conda env create -f environment.yml
'''

2.激活环境并测试
'''bash
conda activate gyp
python wrap.py --data NPA
python wrap.py --data NPB
python wrap.py --data NPC
'''
三条python命令可以在不同的终端运行。