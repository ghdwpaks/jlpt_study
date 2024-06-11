import copy as c
    
    

friends = ["muzi", "ryan", "frodo", "neo"]
gifts = ["muzi frodo", "muzi frodo", "ryan muzi", "ryan muzi", "ryan muzi", "frodo muzi", "frodo ryan", "neo muzi"]
answer = 0
friends_count = []

history = {}

        

["muzi", "ryan", "frodo", "neo"], 
["muzi frodo", 
    "muzi frodo", 
    "ryan muzi", 
    "ryan muzi", 
    "ryan muzi", 
    "frodo muzi", 
    "frodo ryan", 
    "neo muzi"]
'''

m  r  f  n
m0 m3 m1 m1
r0 r0 r1 r0
f2 f0 f0 f0
n0 n0 n0 n0
'''


gift_net = [{}]*len(friends)
for i in range(len(gift_net)) : 
    for j in friends : 
        gift_net[i][j] = 0
print("gift_net :",gift_net)
    
for i in friends :
    net_count = [0]*friends
    for j in range(len(gifts)) :
        j_s = gifts[j].split(" ")
        
