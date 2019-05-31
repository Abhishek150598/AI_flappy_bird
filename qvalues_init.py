import json

qvalues = {}

f = open('qvalues.json', 'r')
qvalues = json.load(f)
f.close()

for x in range(0,40):
	for y in range(0,140):
	    for v in range(-12,30):
	    	s=str(x)+'_'+str(y)+'_'+str(v)
	    	if s not in qvalues.keys():
	        	qvalues[s] = [0,0]

f = open('qvalues.json', 'w')
json.dump(qvalues, f)
f.close()