import select
import socket
from threading import Thread

class soclet(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.host = ""
		self.port = 25565
		self.mdp = ""
		self.client_mdp = []
		self.client_co = []
		
	def run(self):
		self.main_co = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.main_co.bind((self.host, self.port))
		self.main_co.listen(5)
		while True:
			asks, wlist, rlist = select.select([self.main_co], [], [], 0)
			for ask in asks:
				client_nom, infos = ask.accept()
				self.client_co.append(client_nom)
				print("[*]Connected to " + str(infos[0]) + "\n")
				
			try:
				ask_mdp, wlist, rlist = select.select(self.client_co, [], [], 0.05)
			except:
				pass
			for asker_mdp in ask_mdp:
				mdp = asker_mdp.recv(9999)
				mdp = mdp.decode()
				if mdp == self.mdp:
					client_co.append(asker_mdp)
					client_co.remove(asker_mdp)
				
			try:
				atts, wlist, rlist = select.select(self.client_co, [], [], 0.05)
			except select.error:
				pass
			else:
				for att in atts:
					print(att)
					print(self.client_co)
					try:
						msg = att.recv(9999)
					except ConnectionResetError:
						pass
					i = 0
					for co in self.client_co:
						try:
							co.send(msg)
						except ConnectionResetError:
							del self.client_co[i]
						except:
							pass
						i = i + 1


print("[*]Server Start\n")
thread1 = soclet()
thread1.start()
