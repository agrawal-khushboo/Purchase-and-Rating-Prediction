import gzip
from collections import defaultdict
def readGz(f):
    for l in gzip.open(f):
        yield eval(l)
data=list(readGz('train.json.gz'))
def popularity(trainingdata,n):
    itemcount=defaultdict(int)
    totalpurchase=0
    for d in trainingdata:
        item= str(d)
        itemcount[item]+=1
        totalpurchase+=1
    mostpopular=[[itemcount[item],item] for item in itemcount]
    mostpopular.sort()
    mostpopular.reverse
    
    popularitem = set()
    count = 0
    for ic, i in mostpopular:
        count += ic
        popularitem.add(i)
        if count > totalpurchase/n: break
    return popularitem
    itemdata=[]
userdata=[]
for d in data:
    itemdata.append(d['itemID'])
    userdata.append(d['reviewerID'])
popularitem=popularity(itemdata,2)
userdict=defaultdict(list) #dict for category user purchased
itemdict=defaultdict(list) # dict for cateogry of item
# categorydict=defaultdict(list) #dict fot item in particular cateogoty
for d in data:
    user= d['reviewerID']
    item= str(d['itemID'])
    category=list(d['categories'])
    for c in category:
        c=str(c)
        if c not in userdict[user]:
            userdict[user].append(c)
        if c not in itemdict[item]:
            itemdict[item].append(c)
#         if item not in categorydict[c]:
#             categorydict[c].append(item)
def intersection(ls1,ls2):
    l3=[value for value in ls1 if value in ls2]
    return l3
    ui=defaultdict(list)
iu=defaultdict(list)
for d in data:
    user=d['reviewerID']
    item=d['itemID']
    if item not in iu[user]:
        iu[user].append(item)
    if user not in ui[item]:
        ui[item].append(user)

def simitem(item1,item2):
    intersect=[]
    union=[]
    intersect=intersection(ui[item1],ui[item2])
    union=list(set().union(ui[item1],ui[item2]))
    sim=len(intersect)/len(union)
    return sim

def predict(user,item):
    pc=0
    p=0
    pj=0
    pi=0
    if item not in itemdata:
        pc=1
    else:
        if user in userdata:
            for ca in itemdict[str(item)]:
                if ca in userdict[str(user)]:
                    pc=1
                    break
        else:
            pc=1

    items=iu[user]
    for i in items:
        sim=simitem(i,item)
        if sim>0:
            pj=1
            break
    p=max(pj,pc)
    p=pj 
    return p
    purchase=open("Assignment1-purchase_prediction.txt",'w')
purchase.write("reviewerID-itemID,prediction\n")
with open('pairs_Purchase.txt') as p:
    for line in p:
        if line.startswith("reviewerID"):
            continue
        user,item=line.strip().split('-')
        purchase.write(user+"-"+item+","+str(predict(user,item))+"\n")
purchase.close()
