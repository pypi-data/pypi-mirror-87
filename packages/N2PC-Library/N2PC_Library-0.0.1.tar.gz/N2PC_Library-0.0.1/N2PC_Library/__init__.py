def calculateContraIpsi(contra, ipsi):
    return abs((sum(contra) - sum(ipsi))/sum(contra))


def isN2PC(contra, ipsi):
    if calculateContraIpsi(contra, ipsi) > 10: return "yes" 
    if calculateContraIpsi(contra, ipsi) <= 10: return "no" 

print(isN2PC([0,0,2,1,1,1],[0,0,2,3,3,1]), calculateContraIpsi([0,0,2,1,1,1],[0,0,2,3,3,1]))
