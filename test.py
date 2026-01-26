#%matplotlib inline
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('kitcat')

fig, ax = plt.subplots(2, 2)

# Regular plots
ax[0, 0].plot([1, 2], [1, 2])
ax[0, 1].plot([1, 2], [1, 2])
ax[1, 0].plot([1, 2], [1, 2])

# Text-only subplot
ax[1, 1].set_axis_off()
ax[1, 1].text(0.5, 0.5, 'Parameters:\n- param1: value1\n- param2: value2', 
              ha='center', va='center', fontsize=12)

plt.show()
