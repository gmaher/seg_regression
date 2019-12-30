import argparse
import os
import sys
import time
import numpy as np

sys.path.append(os.path.abspath('..'))

from modules import io
from modules import vascular_data as sv

parser = argparse.ArgumentParser()
parser.add_argument('-config')

args = parser.parse_args()

cfg = io.load_json(args.config)

GEN_DIRS   = cfg['gen_dirs']
MESH_DIRS  = cfg['mesh_dirs']
MODEL_DIRS = [f+'/models' for f in GEN_DIRS]
NUM_MODELS = cfg['num_models']

SIM_DIR    = cfg['sim_dir']
SIM_NAME   = SIM_DIR.split('/')[-1]


for g,mo in zip(GEN_DIRS,MODEL_DIRS):
    for i in range(NUM_MODELS):
        for me in MESH_DIRS:
            print(i,me)
            me_dir = g+'/'+me+'/'+str(i)

            os.system('rm -r {}'.format(me_dir+'/'+SIM_NAME))
            os.system('cp -r {} {}'.format(SIM_DIR,me_dir))