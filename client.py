# Version: 1.0
import socket
import threading
from tkinter import *
import tkinter.scrolledtext
from tkinter import simpledialog

HOST = '127.0.0.1'
PORT = 55555

class Client:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        MainWindow = Tk()
        MainWindow.withdraw()

        self.nickname = simpledialog.askstring("Nickname", "Please choose a nickname", parent=MainWindow)

        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        gui_thread.start()

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

    def gui_loop(self):
        self.win = Tk()
        self.win.configure(bg="lightgray")

        self.chat_label  = Label(self.win, text="Chat:", bg="lightgray")
        self.chat_label.pack(pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')

        self.message_label = Label(self.win, text="Message:", bg="lightgray")
        self.message_label.pack(pady=5)

        self.input_area = Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = Button(self.win, text="Send", command=self.write)
        self.send_button.pack(pady=5)

        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()

    def write(self):
        message = f"{self.nickname}: {self.input_area.get('1.0', END)}"
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0', END)
    
    def stop(self):
        self.running = False
        self.win.quit()
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.sock.close()
                break

client = Client(HOST, PORT)