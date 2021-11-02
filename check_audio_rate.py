import sys
import glob
from pydub.utils import mediainfo

list_files = glob.glob("*.wav")

for f_name in list_files:
    print()
    print("***************************************")
    print(f_name)
    info = mediainfo(f_name)
    print('sample_rate:', info['sample_rate'])
    print('channels:', info['channels'])
    print('bits_per_sample:', info['bits_per_sample'])

