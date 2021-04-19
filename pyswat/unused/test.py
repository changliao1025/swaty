import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter
def pretty_num(x, position):
    print('Yo dawg, I got called')
    return "{:,}".format(x)

fig = plt.figure()
ax1 = plt.subplot(111)

ax1.plot([10,100,1000,10000,100000],[10,100,1000,10000,100000],'ob-')

formatter = FuncFormatter(pretty_num)

# Set the formatter
plt.gca().yaxis.set_major_formatter(formatter)

ax1.set_ylabel('Y axis')
ax1.set_xlabel('X axis')

plt.show()