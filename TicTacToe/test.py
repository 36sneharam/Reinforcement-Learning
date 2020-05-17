import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
x = [1,1,2,2,2,2,3,3,3,3]
x = pd.Series(x, name="x variable")
ax = sns.distplot(x)
plt.show()