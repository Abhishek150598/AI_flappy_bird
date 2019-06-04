import matplotlib.pyplot as plt
import json

f = open('bot_scores.json', 'r')
scores = json.load(f)
f.close()

k=500
start = 0
l = []
for i in range(start,len(scores['scores'])-k):
    sum = 0.0
    for j in range(0,k):
        sum += scores['scores'][i+j]
    
    l.append(sum/k)

plt.xlabel("Iterations")
plt.ylabel("Scores")
plt.plot([x for x in range(start+1, len(scores['scores'])+1)],scores['scores'][start:],'b.', linewidth=0.001)    
plt.plot([x for x in range(start+k, len(scores['scores']))],l,'r', linewidth=1.5, label = 'Average of last 500 iterations')
plt.legend()
plt.show()