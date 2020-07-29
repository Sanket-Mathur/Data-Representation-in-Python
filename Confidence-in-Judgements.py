import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as col
from matplotlib import cm
import scipy.stats as ss
import pandas as pd
import numpy as np

np.random.seed(12345)

df = pd.DataFrame([np.random.normal(32000,200000,3650), 
                   np.random.normal(43000,100000,3650), 
                   np.random.normal(43500,140000,3650), 
                   np.random.normal(48000,70000,3650)], 
                  index=[1992,1993,1994,1995])

df_mean = df.mean(axis=1)
df_std = df.std(axis=1)
n = df.shape[1]

plt.figure(figsize=(6,5))

plt.xticks([1992,1993,1994,1995])
plt.gca().set_xlabel('Years')
plt.gca().set_ylabel('Judgements made each Year')
plt.gca().set_title('Confidence in the Judgements that people made [1992-1995]')

yerr = df_std/np.sqrt(n) * ss.norm.ppf(1-0.05/2)
conf_ints = [ss.norm.interval(0.95, loc=mu, scale=se) for mu, se in zip(df_mean, df_std/np.sqrt(n))]

def compute(y, conf_ints):
    if y < np.min(conf_ints):
        return 1.0
    elif y > np.max(conf_ints):
        return 0.0
    return (np.max(conf_ints) - y)/(np.max(conf_ints) - np.min(conf_ints))

cpick = cm.ScalarMappable(cmap=cm.get_cmap('coolwarm'), norm=col.Normalize(vmin=0, vmax=1.0))
cpick.set_array([])

y = 39500.00
probs = [compute(y, ci) for ci in conf_ints]

plt.bar(df_mean.index, df_mean, width=0.95, yerr=yerr, color=cpick.to_rgba(probs))
plt.axhline(y, color='black')

plt.annotate('y={}'.format('%.2f' % y), [1991.5,50000])

plt.colorbar(cpick)

plt.show()

def onclick(event):
    plt.cla()
    plt.gca().set_xlabel('Years')
    plt.gca().set_ylabel('Judgements made each Year')
    plt.gca().set_title('Confidence in the Judgements that people made [1992-1995]')
    y = event.y * 110
    probs = [compute(y, ci) for ci in conf_ints]
    plt.bar(df_mean.index, df_mean, width=0.95, yerr=yerr, color=cpick.to_rgba(probs))
    plt.axhline(y, color='black')
    plt.annotate('y={}'.format('%.2f' % y), [1991.5,50000])
    plt.show()
    
_ = plt.gcf().canvas.mpl_connect('button_press_event', onclick)
