import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import os
import datetime

def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t, tz=datetime.timezone.utc)

def creation_date(filename):
    t = os.path.getctime(filename)
    return datetime.datetime.fromtimestamp(t, tz=datetime.timezone.utc)
print(Path.cwd())
file_list = sorted(Path.cwd().glob('*'))

fl = []
for f in file_list:
    fl.append(creation_date(f))

print(len(fl))
sl = sorted(fl)
plt.figure()

plt.plot(sl,np.arange(len(sl)), linestyle='-', marker='o')

plt.show()
plt.savefig('afl_timestamp_plot.png')