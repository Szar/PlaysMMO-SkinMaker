from PIL import Image as P
from PIL import ImageTk
from Tkinter import *
from functools import partial
import Tkinter, Tkconstants, tkFileDialog, tkMessageBox
import os

class Window:       
	def __init__(self, master): 
		self.views = [
			{"key":"back","name":"Back"},
			{"key":"back_walk1","name":"Back Walking 1"},
			{"key":"back_walk2","name":"Back Walking 2"},
			{"key":"back_jump1","name":"Back Jump 1"},
			{"key":"back_jump2","name":"Back Jump 2"},
			{"key":"front","name":"Front"},
			{"key":"front_walk1","name":"Front Walking 1"},
			{"key":"front_walk2","name":"Front Walking 2"},
			{"key":"front_jump1","name":"Front Jump 1"},
			{"key":"front_jump2","name":"Front Jump 2"},
		]
		self.files = {}
		self.title = "PlaysMMO Skin Maker"
		self.pad = 20
		self.elements = {
			"label":{},
			"button":{},
			"input":{},
		}
		self.initdir = os.path.dirname(os.path.realpath(__file__))
		self.initUI()
		
	def export(self):
		width = 34
		height = 56
		frames = []
		for i in range(0,len(self.views)):
			v = self.views[i]
			frames.append(v)
			if v["key"]=="back_jump2":
				frames.append(self.views[3])
				frames.append(self.views[0])
			if v["key"]=="front_jump2":
				frames.append(self.views[8])
				frames.append(self.views[5])

		s = P.new('RGBA',(width*len(frames),height))
		for i in range(0,len(frames)):
			v = frames[i]
			s.paste(P.open(self.files[v["key"]]),(i*width,0))
		
		sf = tkFileDialog.asksaveasfilename(title = "Save Spritesheet", initialdir = self.initdir, defaultextension=".png", filetypes=[('PNG', ".png")]) 
		s.save(sf,format='png')
		tkMessageBox.showinfo("Export Complete", "Exported spritesheet as "+sf)
	
	def set_text(self,e,t):
		e.delete(0,END)
		e.insert(0,t)
		return

	def filePicker(self, d):
		self.files[d] = tkFileDialog.askopenfilename(title="Select a Sprite File", initialdir = self.initdir, defaultextension=".png", filetypes=[('PNG', ".png")])
		self.initdir = self.files[d]
		self.set_text(self.elements["input"][d], self.files[d])
		Tk().withdraw() 
	
	def initApp(self, n):
		app = Frame(root)
		for i in range(0,n):
			app.rowconfigure(i, weight=1)
		app.grid(row=1, column=1)
		return app

	def initUI(self):
		root.title(self.title)
		app = self.initApp(len(self.views))
		
		for i in range(0,len(self.views)):
			view = self.views[i]
			c = 0
			if i>=len(self.views)/2: c = 4
			row = i
			if i>=len(self.views)/2: row = i-len(self.views)/2
			rowx = row*2
			
			if i==0 or i==len(self.views)/2: pad_top = self.pad
			else: pad_top = self.pad/4

			self.elements["label"][view["key"]] = Label(app, text=view["name"]+" Sprite")
			self.elements["label"][view["key"]].grid(columnspan=3,row=rowx, column=0+c, padx=(self.pad,0), pady=(pad_top,0), sticky="sw")
			self.elements["label"][view["key"]].configure(justify="left")

			self.elements["input"][view["key"]] = Entry(app)
			self.elements["input"][view["key"]].grid(columnspan=2,row=rowx+1, column=0+c, padx=(self.pad,0), pady=0, sticky="nw")

			cmd = partial(self.filePicker, view["key"])
			self.elements["button"][view["key"]] = Button(app, text="Browse", command=cmd, bd = 0, highlightthickness=0) #bg = "", fg = "", activebackground = "", activeforeground = "", font = "",
			self.elements["button"][view["key"]].grid(row=rowx+1, column=2+c, padx=(self.pad/2,self.pad), pady=0, sticky="nw")

			preview = ImageTk.PhotoImage(P.open("includes/"+str(i+1)+".png"))
			panel = Label(app, image=preview)
			panel.image = preview
			panel.place(relheight=.095,relwidth=0.25,relx=0.7,rely=0.03)
			panel.grid(row=rowx+1, column=3+c, padx=(0,self.pad), pady=0, sticky="nw")


		btn = Button(app, text="Export Skin", command=self.export, bd=0, highlightthickness=0)
		btn.grid(row=len(self.views)+1, column=0, padx=self.pad, pady=self.pad, sticky="w")

			
root = Tk()
window=Window(root)
root.mainloop()  