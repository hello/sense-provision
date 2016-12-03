'''
python normalize unnormalized.wav normalized.wav
or batch mode
find . -name "*.wav" |xargs -I{} python normalize.py {} result/{}```
'''
import sys
from scipy.io import wavfile
import numpy as np

rate,data = wavfile.read(sys.argv[1])
print rate,data.shape


themax = np.max(np.abs(data))

mult = 30000.0 / float(themax)
print mult
data = (data*mult).astype('int16')

wavfile.write(sys.argv[2],rate,data)
