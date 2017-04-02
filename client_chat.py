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
	
	def chat_insert(self, msg):
		interface.chat.configure(state=NORMAL)
		interface.chat.insert(END, msg)
		interface.chat.tag_config("alae", foreground="#FF8000")
		interface.chat.configure(state=DISABLED)
	

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

def Profil():
	#-----------------GRAPHIC INTERFACE---------------------#
	main_profil = Tk()
	ip_label = Label(main_profil, text="Ip Server:")
	ip_entry = Entry(main_profil, width=34)
	pseudo_label = Label(main_profil, text="Pseudo:")
	pseudo_entry = Entry(main_profil, width=34)
	valid_button = Button(main_profil, text="Confirm", command=lambda: confirm_profil("", main_profil, ip_entry.get(), pseudo_entry.get()), width=11)
	cancel_button = Button(main_profil, text="Cancel", command=main_profil.destroy, width=11)
	main_profil.bind("<Return>", lambda eff: confirm_profil(eff, main_profil, ip_entry.get(), pseudo_entry.get()))
	#--------------------------PACK-------------------------#
	ip_label.pack(side=TOP)
	ip_entry.pack(side=TOP, padx=15)
	pseudo_label.pack(side=TOP)
	pseudo_entry.pack(side=TOP, padx=15)
	valid_button.pack(side=RIGHT, padx=15, pady=5)
	cancel_button.pack(side=LEFT, padx=15, pady=5)
	main_profil.mainloop()

def confirm_profil(enter, main_profil, ip, pseudo):
	server.host = ip
	server.pseudo = pseudo
	if server.host!="" and server.pseudo!="":
		main_profil.destroy()

server = Server()
interface = Interface()

Profil()
interface.start()
