#Dzintars Spodris

from collections import defaultdict 

class graph:

	_graph = defaultdict(list)  #graph
	_treeHollow = [] #in home work their are tree hollows :), so treeHollow are also edges )
	_graphArray = [] #graph as array


	#class init
	def __init__(self, n, a, b, w):
		self.n = n 
		self.a = a 
		self.b = b 
		self.w = w 
		self.m = len(a) 
		self._graph.clear()
		self._treeHollow.clear()
		self.constructGraph()


	#making graph
	def constructGraph(self):
		self._graphArray = []
		for n in range(len(self.a)):
			if (self.w[n]<0):
				#if weight less then 0, we dont need it, we select it at this stage
				#we need minimum total sum, so we need them
				self.addTreeHollow([self.a[n], self.b[n]], self.w[n])
			else:
				self.addEdge(self.a[n], self.b[n], self.w[n], (n+1))
		return 0


	#adding edge and creating nodes (if it does not exist)
	def addEdge(self, a, b, w, m): 
		if ([a, b, w] not in self._graphArray and [b, a, w] not in self._graphArray):
			self._graph[a].append({"b": b, "w": w, "m": m}) 
			self._graph[b].append({"b": a, "w": w, "m": m}) 
			self._graphArray.append([a, b, w, m])

	#main function - doing all the tasks
	def main(self):
		self.reduceGraph()
		while True:
			for n in self._graph:
				if(len(self._graph[n])>0):
					cycle = self.findPath(n)
					if (cycle!=0):
						self.addTreeHollow(cycle[1],cycle[2])
						self.removeEdge(cycle[1])
						self.reduceGraph()
			vertictesLeft = 0
			for n in self._graph:
				vertictesLeft = vertictesLeft + len(self._graph[n])
			if (vertictesLeft==0): break
		return self.returnTreeHollowList()
	
	#reducing graph - deleting edges if node has only one edge (there cannot by any cycles)
	def reduceGraph(self):
		removeEdge = []
		while True:
			for n in self._graph:
				if (len(self._graph[n])==1):
					removeEdge = removeEdge + [self._graph[n][0].get("m")] 
			if (len(removeEdge)==0): break	
			for n in self._graph:
				for v in self._graph[n]:
					if (v.get("m") in removeEdge):
						self._graph[n].remove(v)
			removeEdge = []

	#deleting edges
	def removeEdge(self,vert):
		for n in self._graph:
			for v in self._graph[n]:
				if ((vert[0]==n and vert[1]==v.get("b")) or
					(vert[0]==v.get("b") and vert[1]==n)):
					self._graph[n].remove(v)

	#looking for path (using DSF)
	def findPath(self, start, originalStart = 0, path = [], minNode = [], minW = 101):
		path = path + [start]
		if (start == originalStart):
			return [path,minNode,minW]
		if (originalStart == 0): 
			originalStart = start
		for n in self._graph[start]:
			if (n.get("b") not in path or 			
				(n.get("b")==originalStart and len(path)>2)):		
				if (n.get("w")<minW):
					minNode = [start,n.get("b")]
					minW = n.get("w")
				result = self.findPath(n.get("b"),originalStart,path,minNode,minW)
				if result:
					return result
			if (n.get("b") in path and n.get("b")!=path[-1] and n.get("b")!=path[-2]):
				#found another path. So returning it first
				newPath = []
				newPathStarted = 0
				for p in path:
					if (newPathStarted==0 and n.get("b")==p):
						newPathStarted = 1
					if (newPathStarted==1): newPath = newPath + [p]
				newPath = newPath + [n.get("b")]
				minNodeData = self.getMinEdgeInPath(newPath)
				return [newPath,minNodeData[0],minNodeData[1]]

		return 0

	#getting minimum edge in path
	def getMinEdgeInPath(self, path):
		minNode = []
		minW = 101
		pathData = []
		for i in range(0, len(path)-1):
			pathData = pathData + [[path[i], path[i+1]]]
			for g in self._graphArray:
				if (((g[0]==path[i] and g[1]==path[i+1]) or
					(g[1]==path[i] and g[0]==path[i+1])) and
					g[2]<minW):
					minNode = [g[0], g[1]]
					minW = g[2]
		return [minNode, minW] 


	#adding edge in list
	def addTreeHollow(self, nodes, w):
		hollowExist = False
		for h in self._treeHollow: 
			if ((h["a"]==nodes[0] and h["b"]==nodes[1]) or 
				(h["a"]==nodes[1] and h["b"]==nodes[0])):
				hollowExist = True
		if (hollowExist==False):
			self._treeHollow.append({"a": nodes[0], "b": nodes[1], "w": w})
		return 0

	#creating list of edges (file output.txt)
	def returnTreeHollowList(self):
		w = 0
		k = 0
		hollowList = []
		for i in self._treeHollow:
			w += i["w"]
			k += 1
			hollowList.append({"a": i["a"], "b":i["b"]})
		file = open("output.txt","w")
		file.write(str(k)+"\x0a")
		file.write(str(w)+"\x0a")
		for i in self._treeHollow:
			file.write(str(i["a"])+"\x09"+str(i["b"])+"\x0a")
		file.close()
		return ({"k": k, "w": w, "hollowList": hollowList})

