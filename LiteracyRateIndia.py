import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

# Importing datasets
data = pd.read_excel('data/DDWCT-0000C-08.xlsx', skiprows=5)
data_SC = pd.read_excel('data/DDW-0000C-08SC.xlsx', skiprows=5)

# Dropping unwanted rows and columns
data.drop(data.index[0], inplace=True)
data_SC.drop(data_SC.index[0], inplace=True)
l = ['Unnamed: 0', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4']
for i in range(11,41): l.append(i)
data.drop(l, axis=1, inplace=True)
data_SC.drop(l, axis=1, inplace=True)

# Renaming Columns
data.columns = ['Ages', 'TotP', 'TotM', 'TotF', 'IllP', 'IllM', 'IllF', 'LitP', 'LitM', 'LitF']
data = data[data.Ages != 'All ages']
data = data[data.Ages != 'Age not stated']
data_SC.columns = ['Ages', 'TotP', 'TotM', 'TotF', 'IllP', 'IllM', 'IllF', 'LitP', 'LitM', 'LitF']
data_SC = data[data.Ages != 'All ages']
data_SC = data[data.Ages != 'Age not stated']

# Combining Rows
data = data.groupby('Ages').sum()
data.loc['7-9'] = data.iloc[0] + data.iloc[1] + data.iloc[2]
data.loc['10-14'] = data.iloc[3] + data.iloc[4] + data.iloc[5] + data.iloc[6] + data.iloc[7]
data.loc['15-19'] = data.iloc[8] + data.iloc[9] + data.iloc[10] + data.iloc[11] + data.iloc[12]
data.drop([7,8,9,10,11,12,13,14,15,16,17,18,19], inplace=True)
data.reset_index(level=0, inplace=True)
data.index = [0,4,5,6,7,8,9,10,11,12,13,14,15,16,1,2,3]
data.sort_index(inplace=True)
data_SC = data_SC.iloc[:27]
data_SC = data_SC.groupby('Ages').sum()
data_SC.loc['7-9'] = data_SC.iloc[0] + data_SC.iloc[1] + data_SC.iloc[2]
data_SC.loc['10-14'] = data_SC.iloc[3] + data_SC.iloc[4] + data_SC.iloc[5] + data_SC.iloc[6] + data_SC.iloc[7]
data_SC.loc['15-19'] = data_SC.iloc[8] + data_SC.iloc[9] + data_SC.iloc[10] + data_SC.iloc[11] + data_SC.iloc[12]
data_SC.drop([7,8,9,10,11,12,13,14,15,16,17,18,19], inplace=True)
data_SC.reset_index(level=0, inplace=True)
data_SC.index = [0,4,5,6,7,8,9,10,11,12,13,14,15,16,1,2,3]
data_SC.sort_index(inplace=True)

# Adding column literatre percentage
data['%LitM'] = (data['LitM'] / data['TotM']) * 100
data['%LitF'] = (data['LitF'] / data['TotF']) * 100
data_SC['%LitM'] = (data_SC['LitM'] / data_SC['TotM']) * 100
data_SC['%LitF'] = (data_SC['LitF'] / data_SC['TotF']) * 100

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex=True, squeeze=True)
ax2.get_shared_y_axes().join(ax1, ax2)
ax3.get_shared_y_axes().join(ax3, ax4)
fig.subplots_adjust(hspace=0.01, wspace=0.01)

# ax1
ax1.bar(data['Ages'], data['%LitM'], width=1.0, color='blue', alpha=0.5)
ax1.bar(data['Ages'], data['%LitF'], width=1.0, color='pink', alpha=0.5)
ax1.set_ylabel('Educated People (%age)')

# ax2
ax2.bar(data_SC['Ages'], data_SC['%LitM'], width=1.0, color='blue', alpha=0.5, label='Male')
ax2.bar(data_SC['Ages'], data_SC['%LitF'], width=1.0, color='pink', alpha=0.5, label='Female')
ax2.legend(loc=1, frameon=False)

# ax3
ax3.plot(data['Ages'], data['TotP'], '-', color='black')
ax3.plot(data['Ages'], data['LitP'], '-', color='green')
ax3.plot(data['Ages'], data['IllP'], '-', color='red')
ax3.set_ylabel('Population (10^7)')
ax3.set_xlabel('Age Group (Urban Population)')

# ax4
ax4.plot(data_SC['Ages'], data_SC['TotP']*100, '-', color='black', label='Total Population')
ax4.plot(data_SC['Ages'], data_SC['LitP']*100, '-', color='green', label='Literate Population')
ax4.plot(data_SC['Ages'], data_SC['IllP']*100, '-', color='red', label='Illiterate Population')
ax4.text(10, 10000000, 'X100')
ax4.legend(loc=1, frameon=False)
ax4.set_xlabel('Age Group (Rural Population)')

ax1.xaxis.set_visible(False)
ax2.xaxis.set_visible(False)
ax2.yaxis.set_visible(False)
ax4.yaxis.set_visible(False)

for x in ax3.get_xticklabels():
    x.set_rotation(90)
for x in ax4.get_xticklabels():
    x.set_rotation(90)

plt.suptitle('Comparision of education level with respect to gender and social status\nIndia Census 2011')
plt.subplots_adjust(bottom=0.2)

plt.show()
