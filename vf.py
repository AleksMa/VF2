import sys
import os
import networkx as nx
from graph import GraphSet
from map import Map

def CreateGraph(filename):
    G = nx.Graph()
    try:
        with open(filename, "r") as fin:
            lineNum = -1
            for line in fin:
                lineList = line.strip().split(" ")
                if not lineList:
                    print("Class GraphSet __init__() line split error!")
                    exit()
                if lineList[0] == 'v':
                    if len(lineList) != 3:
                        print("Class GraphSet __init__() line vertex error!")
                        exit()
                    G.add_node(int(lineList[1]), attr = lineList[2])
                elif lineList[0] == 'e':
                    if len(lineList) != 4:
                        print("Class GraphSet __init__() line edge error!")
                        exit()
                    G.add_edge(int(lineList[1]),int(lineList[2]),weight=int(lineList[3]))
                else:
                    #empty line!
                    continue           
    except(IOError):
        print("Class GraphSet __init__() Cannot open Graph file", filename)
        exit()
    return G

class Vf:

    __origin = None
    __sub = None
     
    def candidate(self, subMNeighbor, gMNeighbor):
        if not (subMNeighbor and gMNeighbor):
            print("Class Vf candidate() arguments value error! subMNeighbor or gMNeighbor is empty!")
            exit()
        if not (isinstance(subMNeighbor, list) and isinstance(gMNeighbor, list)):
            print("Class Vf candidate() arguments type error! type list expected!")
            exit()
        if not all(isinstance(x, int) for x in subMNeighbor):
            print("Class Vf candidate() arguments type error! int in subMNeighbor list expected!")
        if not all(isinstance(x, int) for x in gMNeighbor):
            print("Class Vf candidate() arguments type error! int in gMNeighbor list expected!")        
        
        pairs = []
        for i in range(len(subMNeighbor)):
            for j in range(len(gMNeighbor)):
                string = str(subMNeighbor[i]) + ":" + str(gMNeighbor[j])
                pairs.append(string)
        return pairs

    #type = 0, pre; type = 1, succ    
    def preSucc(self, vertexNeighbor, map, type):
        #vertexNeighbor and map can be empty
        if not (isinstance(vertexNeighbor, list) and isinstance(map, list)):
            print("Class Vf preSucc() arguments type error! vertexNeighbor and map expected list!")
            exit()
        if not (type == 0 or type == 1):
            print("Class Vf preSucc() arguments value error! type expected 0 or 1!")
           
        result = []
        #succ
        if type:
            for vertex in vertexNeighbor:
                if vertex not in map:                   
                    result.append(vertex)
        #pre
        else:
            for vertex in vertexNeighbor:
                if vertex in map:
                    result.append(vertex)
        return result
    
    #type = 0, __sub; type = 1, __origin
    def edgeLabel(self, offset, index1, index2, type):
        '''
        if(int(index1) < int(index2)):
            key = str(index1) + ":" + str(index2)
        else:
            key = str(index2) + ":" + str(index1) 
        '''
        key = str(index1) + ":" + str(index2) 
        if type:
            ESet = self.__origin.curESet(offset)
        else:
            ESet = self.__sub.curESet(offset)
        if key in ESet:
            return ESet[key]
        else:
            return ESet[str(index2) + ":" + str(index1)]
         
    
    def isMatchInV2Succ(self, j, vertex, edge, v2, v2Succ):
        for succ in v2Succ:
            vLabel = self.__origin.curVSet(j)[succ]
            eLabel = self.edgeLabel(j, v2, succ, 1)
            if vLabel == vertex and eLabel == edge:
                return True
        return False
        

    def isMeetRules(self, v1, v2, i, j, result, subMap, gMap, subMNeighbor, gMNeighbor):
        
        '''
        #test usage!
        print "-------------------------------------------"
        print "in isMeetRules() v1: %d, v2: %d" %(v1, v2)
        print "in isMeetRules() result: ", result
        print "in isMeetRules() subMap: ", subMap
        print "in isMeetRules() gMap: ", gMap
        print "in isMeetRules() subMNeighbor: ", subMNeighbor
        print "in isMeetRules() gMNeighbor: ", gMNeighbor
        '''
        
        #compare label of v1 and v2
        subVSet = self.__sub.curVSet(i)
        gVSet = self.__origin.curVSet(j)
        

        if subVSet[v1] != gVSet[v2]:
            #print "vertex label different!"
            return False
            
        #notice, when result is empty, first pair should be added when their vertexLabels are the same!
        if not result:
            return True
        
        
        v1Neighbor = self.__sub.neighbor(i, v1)
        v2Neighbor = self.__origin.neighbor(j, v2)
                
        v1Pre = self.preSucc(v1Neighbor, subMap, 0)
        v1Succ = self.preSucc(v1Neighbor, subMap, 1)
        v2Pre = self.preSucc(v2Neighbor, gMap, 0)
        v2Succ = self.preSucc(v2Neighbor, gMap, 1)

        '''
        #test usage!
        print "in isMeetRules() v1Neighbor: ", v1Neighbor
        print "in isMeetRules() v2Neighbor: ", v2Neighbor        
        print "in isMeetRules() v1Pre: ", v1Pre
        print "in isMeetRules() v2Pre: ", v2Pre
        print "in isMeetRules() v1Succ: ", v1Succ
        print "in isMeetRules() v2Succ: ", v2Succ
        '''

        #3,4 rule
        if(len(v1Pre) > len(v2Pre)):
            #print "len(v1Pre) > len(v2Pre)!"
            return False
                
        for pre in v1Pre:
            if result[pre] not in v2Pre:
                #print "v1Pre not in v2Pre!"
                return False
            if self.edgeLabel(i, v1, pre, 0) != self.edgeLabel(j, v2, result[pre], 1):
                #print "eLabel of v1-pre different with eLabel of v2-result[pre]!"
                return False
           
        '''   
        if(len(v1Succ) > len(v2Succ)):
            #print "len(v1Succ) > len(v2Succ)!"
            return False
                
        for succ in v1Succ:
            vertex = self.__sub.curVSet(i)[succ]
            edge = self.edgeLabel(i, v1, succ, 0)
            if not self.isMatchInV2Succ(j, vertex, edge, v2, v2Succ):
                #print "not self.isMatchInV2Succ()"
                return False
        '''
        
        #5,6 rules
        len1 = len(set(v1Neighbor) & set(subMNeighbor))
        len2 = len(set(v2Neighbor) & set(gMNeighbor))
        if len1 > len2:
            #print "5,6 rules mismatch!"
            return False
            
        #7 rule     
        len1= len(set(self.__sub.curVSet(i).keys()) - set(subMNeighbor) - set(v1Succ))
        len2 = len(set(self.__origin.curVSet(j).keys()) - set(gMNeighbor) - set(v2Succ))
        if len1 > len2:
            #print "7 rule mismatch!"
            return False        
            
        return True
        

    def dfsMatch(self, i, j, result):   
        #print "in dfsMatch() result: ", result
        if not isinstance(result, dict):
            print("Class Vf dfsMatch() arguments type error! result expected dict!")
        
        curMap = Map(result)
        
        '''
        #test usage!
        print "in dfsMatch() curMap.subMap() : ", curMap.subMap()
        print "in dfsMatch() curMap.subMap() length: ", len(curMap.subMap())
        print "in dfsMatch() self.__sub.curVSet(i) : ", self.__sub.curVSet(i)
        print "in dfsMatch() self.__sub.curVSet(i) length: ", len(self.__sub.curVSet(i))
        '''
                
        if curMap.isCovered(self.__sub.curVSet(i)):
            return result
        
 
        subMNeighbor = curMap.neighbor(i, self.__sub, 0, True)
        gMNeighbor = curMap.neighbor(j, self.__origin, 1, True)   
       
        if not (subMNeighbor and gMNeighbor):
            print("Class Vf dfsMatch(), subMNeighbor or gMNeighbor is empty!")
            exit()
        
        subNMNeighbor = curMap.neighbor(i, self.__sub, 0, False)
        gNMNeighbor = curMap.neighbor(j, self.__origin, 1, False)
        #print "in dfsMatch() subNMNeighbor: ", subNMNeighbor
        #print "in dfsMatch() gNMNeighbor: ", gNMNeighbor
        
        #notice, choose one vertex in subGraphNeighbor is ok
        while(len(subNMNeighbor) > 1):
            subNMNeighbor.pop()

        '''    
        #test usage!
        print "Class Vf dfsMatch() curMap.subMap(): ", curMap.subMap()
        print "Class Vf dfsMatch() curMap.gMap(): ", curMap.gMap()
        print "Class Vf dfsMatch() subMNeighbor: ", subMNeighbor
        print "Class Vf dfsMatch() gMNeighbor: ", gMNeighbor
        print "Class Vf dfsMatch() result: ", result
        pairs = self.candidate(subMNeighbor, gMNeighbor)
        print "Class Vf dfsMatch() pairs: ", pairs
        '''
        
        pairs = self.candidate(subNMNeighbor, gNMNeighbor)        
        if not pairs:
            return result
                
        for pair in pairs:        
            v1, v2 = pair.strip().split(":")
            if(self.isMeetRules(int(v1), int(v2), i, j, result, curMap.subMap(), curMap.gMap(), subMNeighbor, gMNeighbor)):
                result[int(v1)] = int(v2)       
                self.dfsMatch(i, j, result)                 
                #notice, it's important to return result when len(result) == len(self.__sub.curVSet(i))
                #otherwise it will continue to pop
                if len(result) == len(self.__sub.curVSet(i)):
                    return result
                result.pop(int(v1))                
        return result
        

    def run(self, f1, f2):
        g1 = CreateGraph(f1)
        g2 = CreateGraph(f2)

        return self.main(g1, g2)

    def main(self, g1, g2):   
        # output = sys.stdout
        '''
        output = sys.stdout
        outputfile=open(f3,'w+')
        sys.stdout=outputfile
        '''

        self.__origin = GraphSet(g1)
        self.__sub = GraphSet(g2)
        
        
        # #test usage!
        # print "in main() subVSet: ", self.__sub.curVSet(0)
        # print "in main() graphVSet: ", self.__origin.curVSet(0)       
        # print "in main() subVESet: ", self.__sub.curVESet(0)
        # print "in main() gVESet: ", self.__origin.curVESet(0)
        
        
        subLen = len(self.__sub.graphSet())
        gLen = len(self.__origin.graphSet())
        
        for i in range(subLen):          
            for j in range(gLen):
                result = {}
                result = self.dfsMatch(i, j, result)                              
                if len(result) == len(self.__sub.curVSet(i)):
                    return result                    
                else:
                    return {}
                    
                

        
    
    
   
# in main() subVESet:  [['0:8', '0:5', '0:6', '0:1'], ['1:3', '1:4', '1:2', '0:1', '1:5', '1:7'], ['1:2'], ['1:3', '3:5'], ['1:4'], ['0:5', '1:5', '5:8', '5:6', '3:5'], ['0:6', '5:6'], ['7:8', '1:7'], ['0:8', '7:8', '5:8']]
# in main() subVESet:  [['0:8', '0:5', '0:6', '0:1'], ['1:3', '1:4', '1:2', '0:1', '1:5', '1:7'], ['1:2'], ['1:3', '3:5'], ['1:4'], ['0:5', '1:5', '5:8', '5:6', '3:5'], ['0:6', '5:6'], ['7:8', '1:7'], ['0:8', '7:8', '5:8']]


