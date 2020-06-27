# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 13:33:51 2020

@author: mthom
"""


from math import factorial as f
import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame(columns=['x','y'])

for j in range(70, 101, 1):
    prob = 0
    for i in range(90,101):
        prob+=f(100)/f(i)/f(100-i) * (j/100) ** i * (1-j/100) ** (100-i)
    
    df = df.append(pd.DataFrame([[j, prob]], columns=['x','y']))
    

df['y_total'] = 1 - (1-df['y'])**365

fig, ax = plt.subplots(1,1,figsize=(10,5))
#ax.plot(df[(df['x']>=70)&(df['x']<=90)]['x'], df[(df['x']>=70)&(df['x']<=90)]['y_total'], 'b-')
ax.plot(df['x'], df['y'], 'b-')
ax.set_yticklabels('{0:,.0f}%'.format(100*x) for x in ax.get_yticks().tolist())
ax.set_facecolor('lightgray')
ax.set_xlabel('True Shooting %')
ax.set_title('Probability of Success for 1 attempt')
plt.show()

fig, ax = plt.subplots(1,1,figsize=(10,5))
ax.plot(df[df['x']<=85]['x'], df[df['x']<=85]['y_total'], 'b-')
ax.set_yticklabels('{0:,.0f}%'.format(100*x) for x in ax.get_yticks().tolist())
ax.set_facecolor('lightgray')
ax.set_xlabel('True Shooting %')
ax.set_title('Probability of Success for 365 attempts')
plt.show()



true = 0.78
thresh = 0
for i in range(90,101):
    thresh+=f(100)/f(i)/f(100-i) * (true) ** i * (1-true) ** (100-i)


true_df = pd.DataFrame(columns=['total','missed','prob'])
for miss in range(0, 11):
    for total in range(101, 0, -1):
        prob = 0
        if total - miss < 90 :
            for i in range(90-total+miss,101-total):
                prob+=f(100-total)/f(i)/f(100-i-total) * (true) ** i * (1-true) ** (100-i-total)
        else:
            prob = 1
        
        if prob<thresh:
            true_df = true_df.append(pd.DataFrame([[total, miss, prob]], columns=['total','missed','prob']))
            print('total={0}, miss={1}: {2:,.4f}'.format(total, miss, prob))
            break

true_df = true_df.append(pd.DataFrame([[0, 0, 0]], columns=['total','missed','prob']))

fig, ax = plt.subplots(1,1,figsize=(10,5))
ax.bar(true_df['missed'], 100, width=1)
rects = ax.bar(true_df['missed'], true_df['total'], width=1)
ax.set_facecolor('lightgray')
ax.set_xlim([0,10])
ax.set_ylim([0,100])
ax.set_ylabel('Total Shots')
ax.set_xlabel('Number of Misses')
ax.set_title('Threshold to Reset Attempt')
def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        if rect.get_height()>0:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(min(max(0, rect.get_x() + rect.get_width() / 2),9.75), height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

autolabel(rects)

plt.show()