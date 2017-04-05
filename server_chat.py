#Version 2.1.2
vesion = "2.1.2"

import select
import socket
from threading import Thread

class soclet(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.host = ""
		self.port = 25565
		self.mdp = "5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8"		#password is "password" in SHA-1
		self.mdp_modo = "d24fa7248f9f2a4c744f1adc1ff59f3c4002cb16"	#password is "passwordmodo" in SHA-1
		self.client_mdp = []
		self.client_co = []
		self.pseudo = dict()
		self.rang = dict()
		
	def run(self):
		self.main_co = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.main_co.bind((self.host, self.port))
		self.main_co.listen(-1)
		ask_mdp = []
		while True:
			#--------------------ASK CONNECT--------------------------#
			asks, wlist, rlist = select.select([self.main_co], [], [], 0)
			for ask in asks:
				client_nom, infos = ask.accept()
				self.client_mdp.append(client_nom)
				print("[*]Connected to " + str(infos[0]))

			#--------------------PASSWORD-----------------------------#
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
								self.pseudo[asker_mdp] = mdp_split[1]
								self.rang[asker_mdp] = "normal"
								msg = "[*]" + self.pseudo[asker_mdp] + " Is Connected\n"
								self.send_msg_all(msg.encode())
								self.send_msg(asker_mdp, b"[*]Confirm\n")
								self.send_msg(asker_mdp, b"[*]Welcome To The Server\n")
								self.client_co.append(asker_mdp)
								self.client_mdp.remove(asker_mdp)
							elif mdp_split[0] == self.mdp_modo:
								self.pseudo[asker_mdp] = mdp_split[1]
								self.rang[asker_mdp] = "modo"
								msg = "[*]" + self.pseudo[asker_mdp] + " Is Connected\n"
								self.send_msg_all(msg.encode())
								self.send_msg(asker_mdp, b"[*]Confirm\n")
								self.send_msg(asker_mdp, b"[*]Welcome To The Server\n")
								self.client_co.append(asker_mdp)
								self.client_mdp.remove(asker_mdp)
							else:
								self.send_msg(asker_mdp, b"[*]Try Again\n")

			#------------------------MESSAGE--------------------------#
			try:
				atts, wlist, rlist = select.select(self.client_co, [], [], 0.05)
			except select.error:
				pass
			else:
				for att in atts:
					msg=""
					try:
						msg = att.recv(1024)
						msg = msg.decode()
					except ConnectionResetError:
						pass
					except:
						pass
					else:
						if msg != "":
							msg_split = msg.split(" ")
							#--------------COMMANDS---------------#
							if msg_split[0]=="/nick":
								try:
									self.pseudo[att] = msg_split[1]
								except:
									att.send(b"[*]Your New Nickname Dosn't Work")
							elif msg_split[0]=="/version":
								msg = "[*]Version " + version
								att.send(msg.encode())
							elif msg_split[0] == "/who":
								msg = ""
								for co in self.client_co:
									msg = msg + self.pseudo[co] + "/ "
								msg = "[*]Who > " + msg + "\n"
								att.send(msg.encode())
							elif msg_split[0]=="/kick":
								if self.rang[att] == "modo":
									for ps in self.pseudo:
										if self.pseudo[ps]==msg_split[1]:
											msg = "[*]" + self.pseudo[ps] + " Is Kick"
											self.send_msg_all(msg.encode())
											self.client_co.remove(ps)
											del self.pseudo[ps]
											break
								else:
									att.send(b"[*]Your Are Not Modo")

							elif msg_split[0]=="/quit":
								msg = "[*]" + self.pseudo[att] + " Is Disconect"
								self.send_msg_all(msg.encode())
								del self.pseudo[att]
								self.client_co.remove(att)
								print(msg)
							else:
								msg = self.pseudo[att] + " > " + msg + "\n"
								self.send_msg_all(msg.encode())

	def send_msg(self, recver, msg_asend):
		try:
			recver.send(msg_asend)
		except:
			pass

	def send_msg_all(self, msg_all):
		i = 0
		for co in self.client_co:
			try:
				co.send(msg_all)
			except ConnectionResetError:
				msg = "[*]" + self.pseudo[self.client_co[i]] + " Is Disconect"
				del self.client_co[i]
				self.send_msg_all(mdg.encode())
				print(msg)
			except:
				pass
			i = i + 1


print("[*]Server Start\n")
print("Your Ip Is " + socket.gethostbyname(socket.gethostname()))
thread1 = soclet()
thread1.start()
