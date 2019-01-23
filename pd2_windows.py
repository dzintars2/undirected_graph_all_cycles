#Dzintars Spodris

#main code to start application
import wx
import graph


class PD2Start():

	def __init__(self, *args, **kwargs):
		self.menu()

	#menu
	def menu(self):
		print ('Algorithm')
		print ('1.Choose file')
		print ('0.Exit')
		a=0
		while a == 0:
			izvele = input("[1 or 0]: ")
			if izvele == "1":
				a = 1
				self.runProgram()
			elif izvele == "0":
				quit()
		return 0

	#starting program
	def runProgram(self):
		filePath = self.get_path()

		try:
			if (filePath!=None):
				with open(filePath, 'r') as myfile:
					data = myfile.read()

				data = data.replace("\x20"," ") #aizvietojam 0x20 (Space) 
				data = data.replace("\x09"," ") #aizvietojam 0x09 (tab)
				data = data.replace("\x0d"," ") #aizvietojam 0x0d (newline)
				data = data.replace("\x0a"," ") #aizvietojam 0x0a (newline)

				text = data.split()
				if (len(text)>0):
					n = 0 #total count of nodes
					a = [] #edge starting node
					b = [] #edge end node
					w = [] #edge weight
					x = 1 
					for t in text:
						if (x==1): 
							n = int(t)
						elif (((x-1)%3)==1):
							a.append(int(t))
						elif (((x-1)%3)==2):
							b.append(int(t))
						elif (((x-1)%3)==0):
							w.append(int(t))
						x +=1
					grafs = graph.graph(n, a, b, w)
					grafs = grafs.main()
					print("Edge count: "+str(grafs["k"])+"\nTotal sum: "+str(grafs["w"])+"\n\nFile created")
					self.menu()
				else:
					print("Error")
			else:
				print("\nFile not found\n\n")
				self.menu()
		except:
			print("Cannot read file\n\n\n")
			return 0

	#choose file path
	def get_path(self):
		app = wx.App(None)
		style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
		dialog = wx.FileDialog(None, 'Open', wildcard='', style=style)
		if dialog.ShowModal() == wx.ID_OK:
			path = dialog.GetPath()
		else:
			path = None
		dialog.Destroy()
		return path

if __name__ == '__main__':
	PD2Start()