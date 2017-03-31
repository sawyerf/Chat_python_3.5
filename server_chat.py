#Version 2.0.1


import select
import socket
from threading import Thread

class soclet(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.host = ""
		self.port = 25565
		self.mdp = "5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8"		#password is "password" and is SHA-1
		self.client_mdp = []
		self.client_co = []
		self.pseudo = dict()
		
	def run(self):
		self.main_co = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.main_co.bind((self.host, self.port))
		self.main_co.listen(-1)
		ask_mdp = []
		while True:
			asks, wlist, rlist = select.select([self.main_co], [], [], 0)
			for ask in asks:
				client_nom, infos = ask.accept()
				self.client_mdp.append(client_nom)
				print("[*]Connected to " + str(infos[0]))
				
			try:
				ask_mdp, wlist, rlist = select.select(self.client_mdp, [], [], 0.05)
			except:
				pass
			else:
				for asker_mdp in ask_mdp:
					mdp = ""
					try:
						mdp = asker_mdp.recv(1024)
					except:
						pass
					else:
						if mdp != "":
							mdp = mdp.decode()
							mdp_split = mdp.split(" ")
							if mdp_split[0] == self.mdp:
								self.send_msg(asker_mdp, b"[*]Confirm\n")
								self.send_msg(asker_mdp, b"[*]Welcome To The Server\n")
								self.pseudo[str(asker_mdp)] = mdp_split[1]
								self.client_co.append(asker_mdp)
								self.client_mdp.remove(asker_mdp)
							else:
								self.send_msg(asker_mdp, b"[*]Try Again\n")
					
			try:
				atts, wlist, rlist = select.select(self.client_co, [], [], 0.05)
			except select.error:
				pass
			else:
				for att in atts:
					try:
						msg = att.recv(1024)
						msg = msg.decode()
					except ConnectionResetError:
						pass
					else:
						msg = self.pseudo[str(att)] + " > " + msg
						i = 0
						for co in self.client_co:
							try:
								co.send(msg.encode())
							except ConnectionResetError:
								del self.client_co[i]
							except:
								pass
							i = i + 1

	def send_msg(self, recver, msg_asend):
		try:
			recver.send(msg_asend)
		except:
			pass


print("[*]Server Start\n")
print("Your Ip Is " + socket.gethostbyname(socket.gethostname()))
thread1 = soclet()
thread1.start()
