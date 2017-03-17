import select
import socket
from threading import Thread

class soclet(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.host = ""
		self.port = 25565
		self.mdp = "Your_password"
		self.client_mdp = []
		self.client_co = []
		
	def run(self):
		self.main_co = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.main_co.bind((self.host, self.port))
		self.main_co.listen(5)
		ask_mdp = []
		while True:
			asks, wlist, rlist = select.select([self.main_co], [], [], 0)
			for ask in asks:
				client_nom, infos = ask.accept()
				self.client_mdp.append(client_nom)
				print("[*]Connected to " + str(infos[0]) + "\n")
				
			try:
				ask_mdp, wlist, rlist = select.select(self.client_mdp, [], [], 0.05)
			except:
				pass
			else:
				for asker_mdp in ask_mdp:
					try:
						mdp = asker_mdp.recv(9999)
					except:
						pass
					mdp = mdp.decode()
					if mdp == self.mdp:
						asker_mdp.send(b"[*]Confirm\n")
						asker_mdp.send(b"[*]Welcome To The Server\n")
						self.client_co.append(asker_mdp)
						self.client_mdp.remove(asker_mdp)
					else:
						asker_mdp.send(b"[*]Try Again\n")
				
			try:
				atts, wlist, rlist = select.select(self.client_co, [], [], 0.05)
			except select.error:
				pass
			else:
				for att in atts:
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
