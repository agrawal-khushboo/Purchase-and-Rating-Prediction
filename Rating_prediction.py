import gzip
from collections import defaultdict
def readGz(f):
    for l in gzip.open(f):
        yield eval(l)
data=list(readGz('train.json.gz'))
bu=defaultdict(int)
bi=defaultdict(int)
iu=defaultdict(list)
ui=defaultdict(list)
rui=defaultdict(int)
itemdata=[]
userdata=[]
for d in data:
    item=str(d['itemID'])
    user=str(d['reviewerID'])
    itemdata.append(item)
    userdata.append(user)
    if item not in iu[user]:
        iu[user].append(item)
    if user not in ui[item]:
        ui[item].append(user)
    bu[user]=0
    bi[item]=0
    rui[user,item]=int(d['rating'])
    
def alpha():
    a=0
    for d in data:
        user=str(d['reviewerID'])
        item=str(d['itemID'])
        a+=(rui[user,item]-(bu[user]+bi[item]))
    a=a/len(data)
    return a


def buser(lam): 
    for user in iu:
        bu[user]=0
        for item in iu[user]:
            bu[user]=bu[user]+(rui[user,item]-(a+bi[item]))
        bu[user]=bu[user]/(lam+len(iu[user]))
    return bu
    
def bitem(lam): 
    for item in ui:
        bi[item]=0
        for user in ui[item]:
            bi[item]=bi[item]+(rui[user,item]-(a+bu[user]))
        bi[item]=bi[item]/(lam+len(ui[item]))
    return bi
    for i in range(1):
        a=alpha()
        bu=buser(6.4)
        bi=bitem(6.4)
        
        
        
def ratingpredict(user,item):
    user=str(user)
    item=str(item)
    r=a+bu[user]+bi[item]
    return r
    
    rating=open("Assignment-rating_prediction.txt",'w')
rating.write("reviewerID-itemID,prediction\n")
with open('pairs_Rating.txt') as purchase:
    for line in purchase:
        if line.startswith("reviewerID"):
            continue
        user,item=line.strip().split('-')
        rating.write(user+"-"+item+","+str(ratingpredict(user,item))+"\n")
rating.close()
