import numpy as np

b = np.array([1,2,3], np.int16)
c = np.array([5,6,7], np.int16)
a = [b,c]

x = np.int16(0)
for c in a:
    x += c * 0.25


print((x))
