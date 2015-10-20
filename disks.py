import numpy.random as nr
import math
import time
import matplotlib.pyplot as plt

class Disks:

	def __init__(self, n, r):
		#initialize variables
		self.n = n
		self.r = r
		self.disks = []
		self.clusters = {}
		self.coords = nr.uniform(size=(n, 2))
		
		for i in range(0, n):
			x = self.coords[i, 0]
			y = self.coords[i, 1]
			left = True if x <= r else False
			right = True if x >= 1 - r else False
			self.disks.append({'x': x, 'y': y, 'left': left, 'right': right, 'cluster': 0})

	def findclusters(self):
		for i in range(len(self.coords)-1):
			for j in range(i+1, len(self.coords)):
				if math.sqrt(math.pow(self.coords[i, 0]-self.coords[j, 0],2)+math.pow(self.coords[i, 1]-self.coords[j, 1],2)) < 2*self.r:
					self.addtocluster(i, j)

	def addtocluster(self, i, j):
		if self.disks[i]['cluster'] and self.disks[j]['cluster']:
			if self.disks[i]['cluster'] != self.disks[j]['cluster']:
                    #no need to join clusters if both disks say they belong to the same cluster
				self.joincluster(self.disks[i]['cluster'], self.disks[j]['cluster'])
		elif self.disks[i]['cluster']:
			self.clusters[self.disks[i]['cluster']]['disks'].append(j)
			if self.disks[j]['left']:
				self.clusters[self.disks[i]['cluster']]['left'] = True
			if self.disks[j]['right']:
				self.clusters[self.disks[i]['cluster']]['right'] = True
			self.disks[j]['cluster'] = self.disks[i]['cluster']
		elif self.disks[j]['cluster']:
			self.clusters[self.disks[j]['cluster']]['disks'].append(i)
			if self.disks[i]['left']:
				self.clusters[self.disks[j]['cluster']]['left'] = True
			if self.disks[i]['right']:
				self.clusters[self.disks[j]['cluster']]['right'] = True
			self.disks[i]['cluster'] = self.disks[j]['cluster']
		else:
			timestamp = time.time()
			self.clusters.update({timestamp: {'disks': [i,j], 'left': self.disks[i]['left'] or self.disks[j]['left'], 'right': self.disks[i]['right'] or self.disks[j]['right']}})
			self.disks[i]['cluster'] = self.disks[j]['cluster'] = timestamp

	def joincluster(self, cluster1, cluster2):
		#takes two cluster names (timestamps) as its arguments
		maxcluster = max(cluster1, cluster2)
		mincluster = min(cluster1, cluster2)
		#we arbitrarity choose to keep the cluster with the earliest timestamp
		for disk in self.clusters[maxcluster]['disks']:
			self.disks[disk]['cluster'] = mincluster #update disks in max cluster to belong to min cluster
		self.clusters[mincluster]['disks'].extend(self.clusters[maxcluster]['disks']) #update min cluster to own disks from max cluster
		self.clusters[mincluster].update({'left': self.clusters[mincluster]['left'] or self.clusters[maxcluster]['left'], 'right': self.clusters[mincluster]['right'] or self.clusters[maxcluster]['right']})
		self.clusters.pop(maxcluster, None) #remove cluster from cluster dict

	def whichcluster(self, id):
		if self.disks[id]['cluster']:
			return self.disks[id]['cluster']
		else:
			return 'This disk does not belong to a cluster.'

	def findconnections(self):
		connections = []
		for k, v in self.clusters.iteritems():
			if v['left'] and v['right']:
				connections.append(v)
				print 'Cluster %(cluster)f connects both sides.' %{'cluster': k}
		if not len(connections):
				print 'No clusters connect both sides.'

	def plotdisks(self):
        fig = plt.gcf()
		for i in range(0, len(self.coords)):
                        if self.disks[i]['cluster']:
                                disksinclusters = plt.Circle((self.coords[i,0],self.coords[i,1]),self.r,color='r',alpha=0.6)
                                ax = plt.gca()
                                ax.set_xlim((0,1))
                                ax.set_ylim((0,1))
                                Disks = fig.gca().add_artist(disksinclusters)
                        else:
                                disksnotinclusters = plt.Circle((self.coords[i,0],self.coords[i,1]),self.r,color='b',alpha=0.6)
                                Disks = fig.gca().add_artist(disksnotinclusters)
           
			

		

			


			

