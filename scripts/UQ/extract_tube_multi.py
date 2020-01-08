import argparse
import os
import sys
import time
sys.path.append(os.path.abspath('../..'))
import pandas
import json
import modules.io as io
import modules.vascular_data as sv
import vtk
import numpy as np
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('-config')
args = parser.parse_args()

cfg = io.load_json(args.config)

NPROC    = cfg['nproc']
VTU_LIST = cfg['vtu_list']
VTUS     = open(VTU_LIST,'r').readlines()
VTUS     = [s.replace('\n','') for s in VTUS]

pids = []

for i,vtu in enumerate(VTUS):

    p = subprocess.Popen(['python','extract_tube.py',
    '-config',    args.config,
    '-tube_file', args.tube_file])
    if i % NPROC == 0:
        print("waiting for procs to finish")
        [p.wait() for p in pids]
        pids = []
