#Version 2.1.0

from tkinter import *
from threading import Thread
import socket
import sys
import hashlib


class Server(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.pseudo=""
		self.host=""
		self.port=25565
		self.confirm=False
		self.one_error=True
		self.condition=True	

	def run(self):
		profil.join()
		while self.condition:
			try:
				self.main_co = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				self.main_co.connect((self.host, self.port))
				self.main_co.settimeout(0.5)
			except ConnectionRefusedError:
				if self.one_error == True:
					self.chat_insert("[*]No Server\n")
					self.one_error=False
				pass
			except:
				if self.one_error == True:
					self.chat_insert("[*]Error Server\n")
					self.one_error = False
				break
			else:
				self.chat_insert("[*]Connected To Server\n")
				self.recevoir()
				break
		
	def recevoir(self):
		while self.condition:
			msg=""
			try:
				msg = self.main_co.recv(1024)
			except ConnectionResetError:
				self.chat_insert("[*]Deconnected To Server\n")
				break
			except ConnectionAbortedError:
				self.chat_insert("[*]Deconnected To Server\n")
				break
			except BrokenPipeError:
				self.chat_insert("[*]Deconnected To Server\n")
				break
			except:
				pass
			else:
				if msg != "":
					msg = msg.decode()
					if "[*]Confirm\n" in msg:
						self.confirm = True
					self.chat_insert(msg)
					interface.chat.see("end")
		self.main_co.send(b"/quit")
		self.main_co.close()


	def recup_msg(self, enter=""):
		msg = interface.msg_send.get()
		if msg != '':
			if self.confirm == True:
				msg = msg
			else:
				msg = hashlib.sha1(msg.encode()).hexdigest()
				msg = msg + " " + self.pseudo
				pass
			self.main_co.send(msg.encode())
			interface.msg_send.delete(0, END)
				
	def confirm_profil(self, enter=""):
		self.host = profil.ip_entry.get()
		self.pseudo = profil.pseudo_entry.get()
		if self.host!="" and self.pseudo!="":
			profil.main_profil.destroy()
	
	def chat_insert(self, msg):
		interface.chat.configure(state=NORMAL)
		interface.chat.insert(END, msg)
		interface.chat.tag_config("alae", foreground="#FF8000")
		interface.chat.configure(state=DISABLED)
	
class Profil(Thread):
	def __init__(self):
		Thread.__init__(self)
		
	def run(self):
		#-----------------GRAPHIC INTERFACE---------------------#
		self.main_profil = Tk()
		self.ip_label = Label(self.main_profil, text="Ip Server:")
		self.ip_entry = Entry(self.main_profil, width=34)
		self.pseudo_label = Label(self.main_profil, text="Pseudo:")
		self.pseudo_entry = Entry(self.main_profil, width=34)
		self.valid_button = Button(self.main_profil, text="Confirm", command=server.confirm_profil, width=11)
		self.cancel_button = Button(self.main_profil, text="Cancel", command=self.main_profil.quit, width=11)
		self.main_profil.bind("<Return>", server.confirm_profil)
		#--------------------------PACK-------------------------#
		self.ip_label.pack(side=TOP)
		self.ip_entry.pack(side=TOP, padx=15)
		self.pseudo_label.pack(side=TOP)
		self.pseudo_entry.pack(side=TOP, padx=15)
		self.valid_button.pack(side=RIGHT, padx=15, pady=5)
		self.cancel_button.pack(side=LEFT, padx=15, pady=5)
		self.main_profil.mainloop()

class Interface(Thread):
	def __init__(self):
		Thread.__init__(self)

	def run(self):
		#------------------------------GRAPHIC INTERFACE-----------------------------#
		self.main = Tk()
		#self.main.geometry("750x500")
		self.chat = Text(self.main, state=NORMAL)
		self.msg_send = Entry(self.main, width=92)
		self.scrollbar = Scrollbar(self.main, command=self.chat.yview)
		self.msg_send.bind("<Return>", server.recup_msg)
		#-----------------------------MENUBAR-----------------------------#
		self.menubar = Menu(self.main)
		self.menu1 = Menu(self.menubar, tearoff=0)
		self.menu1.add_command(label="Connect", command=self.main.quit)
		self.menu1.add_command(label="Quitter", command=self.main.quit)
		self.menubar.add_cascade(label="Main", menu=self.menu1)
		self.main.config(menu=self.menubar)
		#-----------------------------PACK-----------------------------#
		self.msg_send.pack(side=BOTTOM, padx=5, pady=2, fill=X)
		self.scrollbar.pack(side=RIGHT,fill=Y)
		self.chat.pack(side=TOP, padx=5, pady=2, fill=BOTH, expand=1)
		self.chat.configure(state=DISABLED)

		server.start()
		self.main.mainloop()
		server.condition=False
		sys.exit(0)

	

server = Server()
profil = Profil()
interface = Interface()

profil.start()
profil.join()
interface.start()
