import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def main():
    
    df = pd.read_csv('data/temp_data.csv')
    df.sort_values(by=['Date', 'Element'], inplace=True)
    df['Month-Date'] = df['Date'].apply(lambda s: s[5:])
    
    # Removing all records of 29 Feb
    df = df[df['Month-Date'] != '02-29']
    # Converting Temp to Celcius
    df['Data_Value'] /= 10
    
    df_2015 = df[df['Date'] >= '2015-01-01']
    
    # Min and Max Values per dates of df
    min_data = df[df['Element'] == 'TMIN'].groupby('Month-Date').agg({'Data_Value': np.min})
    max_data = df[df['Element'] == 'TMAX'].groupby('Month-Date').agg({'Data_Value': np.max})
    
    # Min and Max Values per dates of df_2015
    min_2015 = df_2015[df_2015['Element'] == 'TMIN'].groupby('Month-Date').agg({'Data_Value': np.min})
    max_2015 = df_2015[df_2015['Element'] == 'TMAX'].groupby('Month-Date').agg({'Data_Value': np.max})
    
    # Points of overflowing and underflowing the marked area
    under = np.where(min_2015 <= min_data)[0]
    over = np.where(max_2015 >= max_data)[0]
        
    plt.figure()
    
    # Plotting min_data and max_data
    plt.plot(max_data.values, '-', c='lightcoral', label='Max Temperature')
    plt.plot(min_data.values, '-', c='deepskyblue', label='Min Temperature')
    
    # Filling Color
    plt.gca().fill_between(range(len(min_data)), max_data['Data_Value'], min_data['Data_Value'], facecolor='blue', alpha=0.1)   
    
    # Plotting the overflow and underflow points
    plt.scatter(over, max_2015.iloc[over], s=20, marker='o', c= 'maroon', label='Higher that max', zorder=3)
    plt.scatter(under, min_2015.iloc[under], s=20, marker='o', c='midnightblue', label='Lower than min', zorder=3)
    
    # Designing, Legend and Ticks
    plt.title('Temperature of 2015 compared with trend from 2005-2014')
    plt.ylabel('Temperature in $^0C$')
    plt.xticks([0,31,59,90,120,151,181,212,243,273,304,334])
    plt.gca().set_xticklabels(np.array(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']))
    plt.legend(loc=8, frameon=False)
    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    plt.show()
    
if __name__ == '__main__':
    main()
