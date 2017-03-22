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

	def run(self):
		condition = True
		profil.join()
		while condition:
			try:
				self.main_co = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				self.main_co.connect((self.host, self.port))
			except ConnectionRefusedError:
				if self.one_error == True:
					chat.insert(END, "[*]No Server\n")
					self.one_error=False
				pass
			except:
				if self.one_error == True:
					chat.insert(END, "[*]Error Server")
					self.one_error = False
				pass
			else:
				chat.insert(END, "[*]Connected To Server\n")
				condition = False
		self.recevoir()
		
	def recevoir(self):
		while True:
			try:
				msg = self.main_co.recv(99999)
			except ConnectionResetError:
				chat.insert(END, "[*]Deconnected To Server\n")
				break
			except ConnectionAbortedError:
				chat.insert(END, "[*]Deconnected To Server\n")
				break
			except:
				pass
			msg = msg.decode()
			if msg == "[*]Confirm\n":
				self.confirm = True
			chat.insert(END, msg)
			chat.see("end")
	
	def recup_msg(self, enter=""):
		msg = msg_send.get()
		if msg != '':
			if self.confirm == True:
				msg = self.pseudo + " > " + msg + "\n"
			else:
				msg = hashlib.sha1(msg.encode()).hexdigest()
				pass
			self.main_co.send(msg.encode())
			msg_send.delete(0, END)
				
	def confirm_profil(self, enter=""):
		self.host = profil.ip_entry.get()
		self.pseudo = profil.pseudo_entry.get()
		if self.host!="" and self.pseudo!="":
			profil.main_profil.destroy()
	
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

def profil_run():
	server = Server()	
	profil = Profil()
	profil.start()
	server.start()

	

server = Server()
profil = Profil()
#------------------------------GRAPHIC INTERFACE-----------------------------#
main = Tk()
chat = Text(main, state=NORMAL)
msg_send = Entry(main, width=92)
send = Button(main, text="Send", command=server.recup_msg, width=10, height=1)
scrollbar = Scrollbar(main, command=chat.yview, cursor="heart")
msg_send.bind("<Return>", server.recup_msg)
#-----------------------------MENUBAR-----------------------------#
menubar = Menu(main)
menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Connect", command=profil_run)
menu1.add_command(label="Quitter", command=main.quit)
menubar.add_cascade(label="Main", menu=menu1)
main.config(menu=menubar)
#-----------------------------PACK-----------------------------#
scrollbar.pack(side=RIGHT,fill=Y)
chat.pack(side=TOP, padx=5, pady=1)
msg_send.pack(side=LEFT, padx=5, pady=1)
send.pack(side=RIGHT, padx=5, pady=1)

profil.start()
server.start()

main.mainloop()
sys.exit(0)
