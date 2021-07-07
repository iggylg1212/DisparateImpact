import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

################# PREPARE VARS ##########

df = pd.read_csv('../3Data/Agency_Data_MPV_LEOKA_CENSUS.csv')
df['HOMICIDES']= df.apply(lambda x: x['HOMICIDES_ASIAN']+x['HOMICIDES_BLACK']+x['HOMICIDES_HISPANIC']+x['HOMICIDES_NATIVE']+x['HOMICIDES_PACIFIC']+x['HOMICIDES_UNKNOWN']+x['HOMICIDES_WHITE'], axis=1)

vr = pd.read_csv('../3Data/OR19.csv')
vr['FLAG'] = 1
vr['ORI9'] = vr['ORI9'].apply(lambda x: x.replace('\'',''))

df = pd.merge(df, vr, how='left', on=['ORI9'])
df = df[df['FLAG']==1]

df = df[df['BLACK_POPULATION']>0]
data = df[['NAME','STATENAME','HOMICIDES','HOMICIDES_BLACK','HOMICIDES_WHITE','POPULATION','BLACK_POPULATION','WHITE_POPULATION']]
data.to_csv('../4outputs/csv/data_proc.csv', index=False)

df = df[df['HOMICIDES']>0]

df['SHARE_BLACK'] = df.apply(lambda x: x['BLACK_POPULATION']/x['CENSUS_POPULATION'], axis=1)
df['SHARE_BLACK_K'] = df.apply(lambda x: x['HOMICIDES_BLACK']/x['HOMICIDES'], axis=1)
df['RATIO'] = df.apply(lambda x: x['SHARE_BLACK_K']/x['SHARE_BLACK'],axis=1 )
df['log_RATIO'] = df['RATIO'].apply(lambda x: np.log(x))
df['comp_rep'] = df.apply(lambda x: x['SHARE_BLACK_K'] - x['SHARE_BLACK'], axis=1)
df['diff_rate'] = df.apply(lambda x: (x['HOMICIDES_BLACK']*100000/x['BLACK_POPULATION'])-(x['HOMICIDES_WHITE']*100000/x['WHITE_POPULATION']), axis=1)

df['SHARE_WHITE'] = df.apply(lambda x: x['WHITE_POPULATION']/x['CENSUS_POPULATION'], axis=1)
df['SHARE_WHITE_K'] = df.apply(lambda x: x['HOMICIDES_WHITE']/x['HOMICIDES'], axis=1)

df['SHARE_POVERTY'] = df.apply(lambda x: x['BELOW_POVERTY']/x['CENSUS_POPULATION'], axis=1)
df['OFFICERS/1kPOP'] = df.apply(lambda x: x['OFFICERS']/(x['CENSUS_POPULATION']/1000), axis=1)

df['STATENAME'] = df['STATENAME'].apply(lambda x: str(x).title())
df['NAME'] = df['NAME'].apply(lambda x: str(x).title())
df['SHARE_POVERTY'] =  df['SHARE_POVERTY'].apply(lambda x: round(x,3))
df['OFFICERS/1kPOP'] =  df['OFFICERS/1kPOP'].apply(lambda x: round(x,3))
df['SHARE_BLACK'] =  df['SHARE_BLACK'].apply(lambda x: round(x,3))
df['SHARE_BLACK_K'] =  df['SHARE_BLACK_K'].apply(lambda x: round(x,3))
df['SHARE_WHITE'] =  df['SHARE_WHITE'].apply(lambda x: round(x,3))
df['SHARE_WHITE_K'] =  df['SHARE_WHITE_K'].apply(lambda x: round(x,3))
df['RATIO'] =  df['RATIO'].apply(lambda x: round(x,3))
df['log_RATIO'] =  df['log_RATIO'].apply(lambda x: round(x,3))
df['comp_rep'] = df['comp_rep'].apply(lambda x: round(x,3))
df['diff_rate'] = df['diff_rate'].apply(lambda x: round(x,3))

df = df.sort_values(['RATIO'], ascending=[False])

########### Visualizations ###########

# # Counts
# print('PB > 0: '+str(len(df[(df['BLACK_POPULATION']>0)])))
# print('K > 0: '+str(len(df[(df['HOMICIDES']>0)])))
# print('K > 0 & PB > 0: '+str(len(df[(df['HOMICIDES']>0)  & (df['BLACK_POPULATION']>0)])))

# # Scattter Plots
# df.plot.scatter(x='HOMICIDES', y="RATIO")
# plt.show()
# df.plot.scatter(x='POPULATION', y="RATIO")
# plt.show()
# df.plot.scatter(x='HOMICIDES', y="log_RATIO")
# plt.show()
# df.plot.scatter(x='HOMICIDES', y="comp_rep")
# plt.show()
# df.plot.scatter(x='POPULATION', y="comp_rep")
# plt.show()
# df.plot.scatter(x='HOMICIDES', y="diff_rate")
# plt.show()
# df.plot.scatter(x='POPULATION', y="diff_rate")
# plt.show()

# df = df[['NAME','STATENAME','HOMICIDES','HOMICIDES_BLACK','SHARE_BLACK_K','HOMICIDES_WHITE','SHARE_WHITE_K','POPULATION','BLACK_POPULATION','SHARE_BLACK','WHITE_POPULATION','SHARE_WHITE','SHARE_POVERTY','OFFICERS/1kPOP','RATIO','comp_rep','diff_rate']]
# # Descriptive Stats
# round(df.describe(), 2).to_csv('../4Outputs/csv/stats_DR_pop.csv')

# # High-Low Ratio Comparisons
# df = df[df['HOMICIDES']>2]
# highest = df.head(10)
# lowest = df[df['RATIO']>0].tail(10)
# hl = pd.concat([highest,lowest])
# hl.to_csv('../4Outputs/csv/highlow.csv')

# # K_B == 0 vs 1
# df1 = df[df['HOMICIDES']==1]
# # sns.displot(df1, x= "SHARE_BLACK", hue='HOMICIDES_BLACK', kind='kde', cut=0)
# sns.histplot(df1, x= "SHARE_BLACK", hue='HOMICIDES_BLACK', stat='probability', common_norm=False)
# plt.show()
# round(df1[df1['HOMICIDES_BLACK']==0].describe(),2).to_csv('../4Outputs/csv/stats_K1_KB0.csv')
# round(df1[df1['HOMICIDES_BLACK']==1].describe(),2).to_csv('../4Outputs/csv/stats_K1_KB1.csv')
#
# df2 = df1[df1['SHARE_BLACK']<.1]
# round(df2[df2['HOMICIDES_BLACK']==0].describe(),2).to_csv('../4Outputs/csv/stats_K1_KB0_2.csv')
# round(df2[df2['HOMICIDES_BLACK']==1].describe(),2).to_csv('../4Outputs/csv/stats_K1_KB1_2.csv')
