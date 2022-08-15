import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_theme(style="whitegrid")

continent = pd.DataFrame([[1,0.169,0.171,0.177,0.266],[0.169,1,0.394,0.549,0.094],
                          [0.171,0.394,	1,0.470,0.109],[0.177,0.549,0.470,1,0.138],[0.266,0.094,0.109,0.138,1]],
                         columns=['Africa','Americas','Asia','Europe','Oceania'],
                        index=['Africa','Americas','Asia','Europe','Oceania'])

sns.lineplot(data=continent, palette="tab10", linewidth=2.5)
plt.show()      #Plot a visual image of the ingredients similarity between each continent