import pandas as pd

vote = pd.read_csv("E:\Voting Systems.csv", sep='\t')
winner = {}

#FPTP    
vote['Rank1'] = vote.apply(lambda x: list(x['Voting Preferences'])[0],axis=1)
winner['FPTP']=vote.groupby(['Rank1']).count().Voter.idxmax()

#Borda Count
vote['Rank2'] = vote.apply(lambda x: list(x['Voting Preferences'])[1],axis=1)
vote['Rank3'] = vote.apply(lambda x: list(x['Voting Preferences'])[2],axis=1)
bcvote = vote.melt(id_vars=['Voting Preferences','Voter'], var_name='ranking', value_name='candidate')[['candidate','ranking']]
bcvote['point'] = bcvote.apply(lambda x: 4-int(list(x['ranking'])[-1]),axis=1)
winner['Borda Count']=bcvote.groupby(['candidate']).sum().point.idxmax()

#AV
remove =[]
while True: 
    vote['AVcandidate'] = vote.apply(lambda x: [c for c in list(x['Voting Preferences']) if c not in remove][0],axis=1)
    if max(vote.groupby(['AVcandidate']).count().Voter)>len(vote)*0.5:
        winner['AV']=vote.groupby(['AVcandidate']).count().Voter.idxmax()
        break
    else:
        remove.append(vote.groupby(['AVcandidate']).count().Voter.idxmin())
        
#Final
final = pd.DataFrame(winner.items(), columns=['Voting System', 'Winner'])    
