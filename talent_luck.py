import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


PCT_TALENT= list(np.linspace(1, 0.95, 10))
PARTICIPANT_NUMBERS= 12000
REQUIRED_PARTICIPANTS= 10
MONTE_CARLO=1000


print(f"The error rate of this simulation is: {(1/math.sqrt(MONTE_CARLO))*100}%")


def raw_talent_luck(
	set_seed: bool= None, 
	seed: int= None
	):
	
	if set_seed is True:
		np.random.seed(seed)
	else:
		pass
	
	raw_talent= np.random.uniform(0, 100, PARTICIPANT_NUMBERS)
	raw_luck= np.random.uniform(0, 100, PARTICIPANT_NUMBERS)

	return raw_talent, raw_luck



def adj_talent_luck(
	talent: float = None,
	luck: float= None,
	pct_talent: float = None,
	pct_luck: float = None,
	):
	
	adj_talent= talent * pct_talent
	adj_luck= luck * pct_luck

	return adj_talent, adj_luck


sliding_mean_talent= []
for talent_contribution in PCT_TALENT:
	PCT_LUCK= 1 - talent_contribution
	monte_carlo_talent=[]
	for _ in range(MONTE_CARLO):

		raw_talent, raw_luck = raw_talent_luck(set_seed= False, seed= 10)		
		adj_talent, adj_luck = adj_talent_luck(talent=raw_talent, luck= raw_luck, pct_talent= talent_contribution, pct_luck= PCT_LUCK)

		df= pd.DataFrame(
			data={
			"id": range(PARTICIPANT_NUMBERS),
			"adj_talent": adj_talent,
			"adj_luck": adj_luck,
			"total_chance": [x + y for x, y in zip(adj_talent, adj_luck)]
			})

		top_total_chance= df.nlargest(n=REQUIRED_PARTICIPANTS, columns="total_chance")["id"].values.tolist()
		top_adj_talent= df.nlargest(n=REQUIRED_PARTICIPANTS, columns="adj_talent")["id"].values.tolist()

		talent_overlap= len(set(top_total_chance).intersection(top_adj_talent))
		monte_carlo_talent.append(talent_overlap)

	sliding_mean_talent.append(np.mean(monte_carlo_talent))



print(PCT_TALENT)
print(sliding_mean_talent)


#Plotting the data
talent= pd.Series(data= sliding_mean_talent, index= PCT_TALENT)

plt.rcParams['axes.spines.left'] = False
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.bottom'] = False
plt.rcParams['xtick.bottom'] = False
plt.rcParams['ytick.left'] = False


plt.plot(talent, color="tab:orange", linewidth=1, marker="o", markersize=6, ls="--", markeredgecolor="w", markeredgewidth=1.3)
plt.gca().invert_xaxis()
plt.xlabel("% talent Contribution")
plt.ylabel(F"Participant selected out of {REQUIRED_PARTICIPANTS}")


for x,y in zip(talent.index, talent.values):

    label = "{:.2f}".format(y)

    plt.annotate(label, 
                 (x,y), 
                 textcoords="offset points", 
                 xytext=(0,10), 
                 ha='center') 

plt.tight_layout()
plt.show()