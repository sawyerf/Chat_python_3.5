from tkinter import *
from threading import Thread
import socket
import sys


class server(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.pseudo=""
		self.host=""
		self.port=25565
		self.confirm=False
	
	def run(self):
		
		condition = True
		thread2.join()
		
		while condition:
			try:
				self.main_co = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				self.main_co.connect((self.host, self.port))
			except ConnectionRefusedError:
				chat.insert(END, "[*]No Server\n")
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
			msg = msg.decode()
			if msg == "[*]Confirm\n":
				self.confirm = True
			chat.insert(END, msg)
			chat.see("end")
	
	def recup_msg(self):
		msg = msg_send.get()
		if msg != '':
			if self.confirm == True:
				msg = self.pseudo + " > " + msg + "\n"
			else:
				pass
			self.main_co.send(msg.encode())
			msg_send.delete(0, END)
			
			
	def confirm_profil(self):
		self.host = thread2.ip_entry.get()
		self.pseudo = thread2.pseudo_entry.get()
		if self.host!="" and self.pseudo!="":
			thread2.main_profil.quit()
	
class profil(Thread):	
	def __init__(self):
		Thread.__init__(self)
		
	def run(self):
		#-----------------GRAPHIC INTERFACE---------------------#
		self.main_profil = Tk()
		self.ip_label = Label(self.main_profil, text="Ip Server:")
		self.ip_entry = Entry(self.main_profil, width=34)
		self.pseudo_label = Label(self.main_profil, text="Pseudo:")
		self.pseudo_entry = Entry(self.main_profil, width=34)
		self.valid_button = Button(self.main_profil, text="Confirm", command=thread1.confirm_profil)
		self.cancel_button = Button(self.main_profil, text="Cancel", command=self.main_profil.quit)
		#--------------------------PACK-------------------------#
		self.ip_label.pack(side=TOP)
		self.ip_entry.pack(side=TOP, padx=15)
		self.pseudo_label.pack(side=TOP)
		self.pseudo_entry.pack(side=TOP, padx=15)
		self.valid_button.pack(side=RIGHT, padx=15, pady=5)
		self.cancel_button.pack(side=LEFT, padx=15, pady=5)
		self.main_profil.mainloop()

thread1 = server()
#------------------------------GRAPHIC INTERFACE-----------------------------#
main = Tk()
chat = Text(main)
msg_send = Entry(main, width = 90)
send = Button(main, text="Send", command=thread1.recup_msg)
scrollbar = Scrollbar(main, command=chat.yview, cursor="heart")
#-----------------------------MENUBAR-----------------------------#
menubar = Menu(main)
menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Connect", command=main.quit)
menu1.add_command(label="Quitter", command=main.quit)
menubar.add_cascade(label="Main", menu=menu1)
main.config(menu=menubar)
#-----------------------------PACK-----------------------------#
scrollbar.pack(side=RIGHT,fill=Y)
chat.pack(side=TOP, padx=5, pady=1)
msg_send.pack(side=LEFT, padx=5, pady=1)
send.pack(side=RIGHT, padx=5, pady=1)

thread2 = profil()
thread2.start()
thread1.start()

main.mainloop()
sys.exit(0)