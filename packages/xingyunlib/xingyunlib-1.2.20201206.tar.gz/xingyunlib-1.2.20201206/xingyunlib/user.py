import hashlib,pickle

def md5(text):

	return hashlib.md5(text.encode(encoding='UTF-8')).hexdigest()
class user_login:
	def __init__(self,filename=None):
		if filename!=None:
			with open(filename+".pickle","rb") as file:
				c = pickle.load(file)
				# print(c)
				self.name = c[0]
				self.key = c[1]
		else:
			self.key = None
			self.name = None
	def registered(self,name,key,flag=True,filename=None):
		if (self.key != None and self.name != None)and flag:
			return False
		else:
			with open(filename+".pickle","wb") as file:
				fp = [name, md5(key)]
				pickle.dump(fp, file)
				self.key=md5(key)
				self.name=name
			return True
	def login(self,name,key):
		if self.key==md5(key) and self.name==name :
			return True
		elif self.key == None and self.name == None:
			return None
		else:
			return False
	def load(self,filename):
		with open(filename + ".pickle", "rb") as file:
			c = pickle.load(file)
			# print(c)
			self.name = c[0]
			self.key = c[1]





