# -*- coding: utf-8-sig -*-
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#%%
# 设置绘图风格
plt. style.use("ggplot")
# 设置中文编码和符号的正常显示
plt.rcParams["font.sans-serif"] = "KaiTi"
plt.rcParams["axes.unicode_minus"] = False

# %%
s_mean = pd.Series()
s_std = pd.Series()
plt.plot(s_mean, color='purple', lw=0.5, ls='-', marker='^', ms=4)
plt.plot(s_mean + s_std, color='green', lw=0.5, ls='-.', marker='o', ms=4)
plt.plot(s_mean - s_std, color='blue', lw=0.5, ls='-.', marker='o', ms=4)
# %%
plt.plot(s_mean, s_std, c='blue')

# %%
x = np.arange(0, 10, 0.1)
y1 = 0.05 * x ** 2
y2 = -1 * y1

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()  # mirror the ax1
ax1.plot(x, y1, 'g-')
ax2.plot(x, y2, 'b-')

ax1.set_xlabel('X data')
ax1.set_ylabel('Y1 data', color='g')
ax2.set_ylabel('Y2 data', color='b')

plt.show()
