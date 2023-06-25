import os
import shutil
import multiprocessing as mp
import pandas as pd
import argparse
def batch_dock(mol2_path, file):
    file_path = os.path.join(mol2_path, file)
    prex_file = file.replace('.mol2', '')

    os.system('{}/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_ligand4.py -l {} -o {}/{}.pdbqt'.format(autodock_install_path, file_path, pdbqt_path, prex_file))
    os.system('vina --config {0} --ligand {1}/{3}.pdbqt --out {2}/{3}.pdbqt'.format(conf_file, pdbqt_path, out_pdbqt, prex_file))
    os.system("vina_split --input {}/{}.pdbqt".format(out_pdbqt, prex_file))
    os.system('scp -r {0}/{2}_ligand_01.pdbqt {1}/{2}_ligand_01.pdbqt'.format(out_pdbqt, result_pdbqt, prex_file))

    docking_score= open('{0}/{1}_ligand_01.pdbqt'.format(result_pdbqt, prex_file), 'r').readline().split(':')[1].split()[0]
    f = open(mol2_path+'_record.csv','a+')
    f.write('{0}/{1}_ligand_01.pdbqt,{2}\n'.format(result_pdbqt, prex_file, docking_score))
    f.close()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--working_path', required=True, help='we must give this para')
    parser.add_argument('--autodock_install_path', required=True, help='we must give this para')
    parser.add_argument('--conf_file', required=True, help='we must give this para')
    parser.add_argument('--cpus', default=10,type=int)

    args = parser.parse_args()
    return args

## first ,we need to move the dockvina to sdf file path
## second ,the computer should have obabel and autodock & vina
args = parse_args()
cpus = args.cpus
# working_path = '/data/jianping/bokey/web-ocaicm/bokey/PyaiVS/database/work'
# autodock_install_path ='/home/jianping/bokey/MGLTools-1.5.7' #/home/jianping/Programs/Autodock/mgltools/MGLTools-1.5.7
# conf_file = '/home/jianping/Downloads/file/config.conf'
working_path = args.working_path
autodock_install_path =args.autodock_install_path
conf_file = args.conf_file
mol2_path = os.path.join(working_path,'mol2')
pdbqt_path = os.path.join(working_path,'pdbqt')
out_pdbqt = os.path.join(working_path,'out_pdbqt')
result_pdbqt = os.path.join(working_path,'result_pdbqt')
select_pdbqt = os.path.join(working_path,'select_pdbqt')
lscore_mol2 = os.path.join(working_path,'ligand_mol2')


if not os.path.exists(mol2_path):
    os.mkdir(mol2_path)
if not os.path.exists(pdbqt_path):
    os.mkdir(pdbqt_path)
if not os.path.exists(out_pdbqt):
    os.mkdir(out_pdbqt)
if not os.path.exists(result_pdbqt):
    os.mkdir(result_pdbqt)



os.system('obabel *.sdf -O {}/.mol2 -m'.format(mol2_path)) #convert sdf type file to mol2 type file
num = len(os.listdir(mol2_path))
p =mp.Pool(processes=1)
for i in range(num+1):

    file = str(i)+'.mol2'
    p.apply_async(batch_dock, args=(mol2_path,file))
p.close()
p.join()

##sorted
result_dict = {}
for line in open(mol2_path+'_record.csv','r'):
    out_file = line.strip().split(',')[0]
    dock_score = line.strip().split(',')[1]
    result_dict[out_file]=dock_score
sorted_result = list(sorted(result_dict.items(),key=lambda x:float(x[1])))
f = open(mol2_path+'_sort_dock_result.csv','w')
for info in sorted_result:
    f.write('{},{}\n'.format(info[0],str(info[1])))
f.close()





