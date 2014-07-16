import pandas as pd
import scipy as sp
import matplotlib.pyplot as plt
import statsmodels.formula.api as sm
from matplotlib.ticker import FuncFormatter

def millions(x, pos):
    'The two args are the value and tick position'
    return '$%1.1fM' % (x*1e-6)

formatter = FuncFormatter(millions)

def plot_spending_wins(teams, year):    
    teams_year = teams.xs(year)
    fig, ax = plt.subplots()
    for i in teams_year.index:
        if i == 'OAK':
            ax.scatter(teams_year['salary'][i], teams_year['W'][i], color="#4DDB94", s=200)
            ax.annotate(i, (teams_year['salary'][i], teams_year['W'][i]),
                        bbox=dict(boxstyle="round", color="#4DDB94"),
                        xytext=(-30, 30), textcoords='offset points',
                        arrowprops=dict(arrowstyle="->", connectionstyle="angle,angleA=0,angleB=90,rad=10"))
        elif i == 'NYA':
            ax.scatter(teams_year['salary'][i], teams_year['W'][i], color="#0099FF", s=200)
            ax.annotate(i, (teams_year['salary'][i], teams_year['W'][i]),
                        bbox=dict(boxstyle="round", color="#0099FF"),
                        xytext=(30, -30), textcoords='offset points',
                        arrowprops=dict(arrowstyle="->", connectionstyle="angle,angleA=0,angleB=90,rad=10"))
        elif i == 'BOS':
            ax.scatter(teams_year['salary'][i], teams_year['W'][i], color="#FF6666", s=200)
            ax.annotate(i, (teams_year['salary'][i], teams_year['W'][i]),
                        bbox=dict(boxstyle="round", color="#FF6666"),
                        xytext=(-30, 30), textcoords='offset points',
                        arrowprops=dict(arrowstyle="->", connectionstyle="angle,angleA=0,angleB=90,rad=10"))     
        else:
            ax.scatter(teams_year['salary'][i], teams_year['W'][i], color="grey", s=200)
    ax.xaxis.set_major_formatter(formatter) 
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=15)
    ax.set_xlabel('Salaries', fontsize=20)
    ax.set_ylabel('Number of Wins' , fontsize=20)
    ax.set_title('Salaries - Wins: '+ str(year), fontsize=25, fontweight='bold')
    plt.show()



def main():

	teams = pd.read_csv('../data/Teams.csv')

	teams = teams[teams['yearID'] >= 1985]
	teams = teams[['yearID', 'teamID', 'Rank', 'R', 'RA', 'G', 'W', 'H', 'BB', 'HBP', 'AB', 'SF', 'HR', '2B', '3B']]

	teams = teams.set_index(['yearID', 'teamID'])

	salaries = pd.read_csv('../data/Salaries.csv')

	salaries_by_yearID_teamID = salaries.groupby(['yearID', 'teamID'])['salary'].sum()

	teams = teams.join(salaries_by_yearID_teamID)

	plot_spending_wins(teams, 2001)

	teams['BA'] = teams['H']/teams['AB']
	teams['OBP'] = (teams['H'] + teams['BB'] + teams['HBP']) / (teams['AB'] + teams['BB'] + teams['HBP'] + teams['SF'])
	teams['SLG'] = (teams['H'] + teams['2B'] + (2*teams['3B']) + (3*teams['HR'])) / teams['AB']

	#First Model
	runs_reg_model1 = sm.ols("R~OBP+SLG+BA",teams)
	runs_reg1 = runs_reg_model1.fit()
	#Second Model
	runs_reg_model2 = sm.ols("R~OBP+SLG",teams)
	runs_reg2 = runs_reg_model2.fit()
	#Third Model
	runs_reg_model3 = sm.ols("R~BA",teams)
	runs_reg3 = runs_reg_model3.fit()


	print runs_reg1.summary()
	print runs_reg2.summary()
	print runs_reg3.summary()

if __name__ == '__main__':
	main()








