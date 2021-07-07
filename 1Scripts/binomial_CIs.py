from scipy.optimize import LinearConstraint
from scipy.optimize import Bounds
from scipy.stats import binom
from scipy.optimize import minimize
import numpy as np
import pandas as pd
from statsmodels.stats import proportion

############# C-P Confidence Intervals for D_r ##############

df = pd.read_csv('../4Outputs/csv/data_proc.csv')

alpha = 1-(.9**.5)
for index, row in df.iterrows():
    K_B = row['HOMICIDES_BLACK']
    B = row['BLACK_POPULATION']
    CI_BLACK = proportion.proportion_confint(K_B, B, alpha=alpha, method='beta')

    K_W = row['HOMICIDES_WHITE']
    W = row['WHITE_POPULATION']
    CI_WHITE = proportion.proportion_confint(K_W, W, alpha=alpha, method='beta')

    df.loc[index, 'CI_BLACK_lb'] = CI_BLACK[0]
    df.loc[index, 'CI_BLACK_ub'] = CI_BLACK[1]
    df.loc[index, 'CI_WHITE_lb'] = CI_WHITE[0]
    df.loc[index, 'CI_WHITE_ub'] = CI_WHITE[1]

    if CI_BLACK[0] > CI_WHITE[1] or CI_BLACK[1] < CI_WHITE[0]:
        df.loc[index, 'Test'] = 1
    else:
        df.loc[index, 'Test'] = 0

df.to_csv('../4Outputs/csv/data_proc.csv', index=False)
