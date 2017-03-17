from tkinter import *
from threading import Thread
import socket
import sys


class server(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.pseudo="Your_name"
		self.host="Your_ip"
		self.port=25565
	
	def run(self):
		condition = True
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
			chat.insert(END, msg)
			chat.see("end")
	
	def recup_msg(self):
		msg = msg_send.get()
		if msg != '':
			msg = self.pseudo + " > " + msg + "\n"
			self.main_co.send(msg.encode())
			msg_send.delete(0, END)
		

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
menu1.add_command(label="Connect", command=connection)
menu1.add_command(label="Quitter", command=main.quit)
menubar.add_cascade(label="Main", menu=menu1)
main.config(menu=menubar)
#-----------------------------PACK-----------------------------#
scrollbar.pack(side=RIGHT,fill=Y)
chat.pack(side=TOP, padx=5, pady=1)
msg_send.pack(side=LEFT, padx=5, pady=1)
send.pack(side=RIGHT, padx=5, pady=1)

thread1.start()
main.mainloop()
sys.exit(0)
