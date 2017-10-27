'''
About: Implementation of Gale Shapley algorithm
'''

mPref = {1:[5,7,1,2,6,8,4,3],
2:[2,3,7,5,4,1,8,6],
3:[8,5,1,4,6,2,3,7],
4:[3,2,7,4,1,6,8,5],
5:[7,2,5,1,3,6,8,4],
6:[1,6,7,5,8,4,2,3],
7:[2,5,7,6,3,4,8,1],
8:[3,8,4,5,7,2,6,1]}

wPref = {1:[5,3,7,6,1,2,8,4],
2:[8,6,3,5,7,2,1,4],
3:[1,5,6,2,4,8,7,3],
4:[8,7,3,2,4,1,5,6],
5:[6,4,7,3,8,1,2,5],
6:[2,8,5,4,6,3,7,1],
7:[7,5,2,1,8,6,4,3],
8:[7,4,1,5,2,3,6,8]}

rejM = [1,2,3,4,5,6,7,8]
tentativeMatches = {i:[] for i in rejM}


def isMatchRemaining(tentativeMatches):
    x = sum([1 for (k,v) in tentativeMatches.items() if len(v) == 0])

    if x > 0:
        return True
    else:
        return False


while isMatchRemaining(tentativeMatches):

    for r in rejM:
        tentativeMatches[mPref[r][0]].append(r)

    rejM = []
    for (k,v) in tentativeMatches.items():
        if len(tentativeMatches[k]) > 1:

            bestPref = None
            for p in wPref[k]:
                
                if p in v:
                    if bestPref is None:
                        bestPref = p
                    if bestPref is not None and bestPref <> p and p in tentativeMatches[k]:
                        mPref[p].remove(k)
                        rejM.append(p)
                        
            tentativeMatches[k] = [bestPref]

print "-------Stable Matching--------"            

print [(v[0],k) for k,v in tentativeMatches.items()]

