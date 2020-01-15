import os

CONFIGS = [
"/home/marsdenlab/projects/seg_regression/scripts/config_segment/0110/extract/wom_rcr_1.json",
"/home/marsdenlab/projects/seg_regression/scripts/config_segment/0110/extract/wom_rcr_2.json",
"/home/marsdenlab/projects/seg_regression/scripts/config_segment/0110/extract/wom_rcr_3.json",
"/home/marsdenlab/projects/seg_regression/scripts/config_segment/0110/extract/wom_rcr_4.json",
]

TUBES = [
'aorta_single',
'aorta_single_2',
'right_iliac_single'
]


print('tubes')

for cfg in CONFIGS:
    for p in TUBES:
        print(cfg, p)
        name = cfg.split('/')[-1].replace('.json','')

        os.system("python extract_tube_new.py -config {} \
        -tube_file ../config_segment/0110/tubes/{}.json \
        -output_fn /media/marsdenlab/Data1/UQ/0110/csv/{}/{}_tube.csv".format(cfg,p,name,p)
        )