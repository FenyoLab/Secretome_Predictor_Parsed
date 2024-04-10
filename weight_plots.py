import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Seaborn set aesthetics
# sns.set_theme()

names = ["TOPCONS","Phobius","Predisi","SignalP","Outcyte","DeepSig",'SecretomeP'][:-1]
correct_secreted = [0.933,0.866,0.9333,0.9,0.9,0.8, 0.85][:-1]
correct_nonsecreted = [0.923,0.846,0.795,0.923,0.795,0.948, 0.85][:-1]

x = np.arange(len(names))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots(figsize=(10, 6))
rects1 = ax.bar(x - width/2, correct_secreted, width, label='Secreted', color='dodgerblue', alpha=0.8)
rects2 = ax.bar(x + width/2, correct_nonsecreted, width, label='Nonsecreted', color='salmon', alpha=0.8)

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_xlabel('Algorithms', fontsize=12)
ax.set_ylabel('Accuracy', fontsize=20)
ax.set_title('Accuracy of the different algorithms', fontsize=20, pad=20)
ax.set_xticks(x)
ax.set_xticklabels(names, fontsize=20, rotation=45)
ax.legend()

# To make it more attractive let's add some grid lines
# ax.grid(True)

fig.tight_layout()

# plt.show()
# plt.close()
# weights = [0.1826437941473259,0.1685166498486377,0.1700302724520686,
#            0.179364278506559,0.12739656912209885,0.17204843592330973,0.5][:-1]

weights = [0.16779445567973875, 0.16784865756771655, 0.1680503755071619, 0.1667838137952169, 0.1663413691124428, 0.16318132833772314]
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(x, weights, color='dodgerblue', alpha=0.8)

ax.set_xlabel('Algorithms', fontsize=12)
ax.set_ylabel('Weights', fontsize=20)
ax.set_title('Weights assigned to each algorithm', fontsize=20, pad=20)
ax.set_xticks(x)
ax.set_xticklabels(names, fontsize=20, rotation=45)
# ax.grid(True)

fig.tight_layout()
plt.show()

