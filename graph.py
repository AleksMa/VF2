#-*- coding:utf-8 -*-
# AUTHOR:   yaolili
# FILE:     graph.py
# ROLE:     read graph from inputFile
# CREATED:  2015-11-28 20:55:11
# MODIFIED: 2015-12-04 09:43:50

class GraphSet:
    
    def __init__(self, inputFile):   
        self.__graphSet = []
        self.__vertexSet = []
        self.__edgeSet = []
        try:
            with open(inputFile, "r") as fin:
                lineNum = -1
                curVertexSet = {}
                curEdgeSet = {}
                for line in fin:
                    lineList = line.strip().split(" ")
                    if not lineList:
                        print("Class GraphSet __init__() line split error!")
                        exit()
                    #a new graph!
                    if lineList[0] == 't':
                        #write it to graphSet
                        if lineNum > -1:
                            currentGraph = (lineNum, curVertexSet, curEdgeSet)
                            self.__graphSet.append(currentGraph)
                            self.__vertexSet.append(curVertexSet)
                            self.__edgeSet.append(curEdgeSet)
                            #print "Class GraphSet __init__  __graphSet: ", self.__graphSet
                            #print "Class GraphSet __init__  __vertexSet: ", self.__vertexSet
                            #print "Class GraphSet __init__  __edgeSet: ", self.__edgeSet
                        lineNum += 1
                        curVertexSet = {}
                        curEdgeSet = {}
                    elif lineList[0] == 'v':
                        if len(lineList) != 3:
                            print("Class GraphSet __init__() line vertex error!")
                            exit()
                        curVertexSet[int(lineList[1])] = lineList[2]
                    elif lineList[0] == 'e':
                        if len(lineList) != 4:
                            print("Class GraphSet __init__() line edge error!")
                            exit()
                        edgeKey = str(lineList[1]) + ":" + str(lineList[2])
                        curEdgeSet[edgeKey] = lineList[3]
                    else:
                        #empty line!
                        continue           
        except IOError as e:
            print("Class GraphSet __init__() Cannot open Graph file: ", e)
            exit()
            
    
    def graphSet(self):        
        return self.__graphSet
    
    def curVSet(self, offset):
        if offset >= len(self.__vertexSet):
            print("Class GraphSet curVSet() offset out of index!")
            exit()
        
        return self.__vertexSet[offset]
        
        
    def curESet(self, offset):
        if offset >= len(self.__edgeSet):
            print("Class GraphSet curESet() offset out of index!")
            exit()
        
        return self.__edgeSet[offset]
    
      
    def curVESet(self, offset):
    
        if offset >= len(self.__vertexSet):
                print("Class GraphSet curVESet() offset out of index!")
                exit()

        vertexNum = len(self.__vertexSet[offset])
        result = [[] for i in range(vertexNum)]
            
        for key in self.__edgeSet[offset]:
            v1, v2 = key.strip().split(":")
            #print int(v1)
            #print int(v2)
            result[int(v1)].append(key)
            result[int(v2)].append(key)
        return result
    

    def neighbor(self, offset, vertexIndex):
        if offset >= len(self.__vertexSet):
            print("Class GraphSet neighbor() offset out of index!")
            exit()
        
        VESet = self.curVESet(offset)
        aList = VESet[vertexIndex]
        neighborSet = []
        for i in range(len(aList)):
            v1, v2 = aList[i].strip().split(":")            
            if int(v1) != vertexIndex:
                neighborSet.append(int(v1))
            elif int(v2) != vertexIndex:
                neighborSet.append(int(v2))
            else:
                exit()
        return neighborSet
