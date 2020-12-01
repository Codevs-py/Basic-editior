import json
import time as tt
import tkinter as tk
import tkinter.scrolledtext as sc
from tkinter import messagebox, ttk

from PIL import Image, ImageTk

with open("theme.json") as c:
    colors = json.load(c) #color platte for window

#utilities for operating
n = True  #trigger counting
brk = 0  #pauses counting
prev = 1 #stores previous count
sec = 0 #stores no. of secs passed

#<<<<<<<< BUTTONS >>>>>>>>>>>#    
class ToolButtons():
    "button inside tools"
    def __init__(self,parent, imge, i_d, cmd):
        self.img  = ImageTk.PhotoImage(Image.open(imge).resize((40,40))) #resize image
        
        self.bt = tk.Button(parent,text = i_d, image = self.img, bg =colors["tools"]["bg"] ,fg ="white", relief = "flat", width = 40, height = 40, activebackground = colors["tools"]["bg"], command = cmd)
        self.bt.pack(padx =3, pady = 3)
    

#<<<<<<<<<< STATUS BAR >>>>>>>>>>>>>#
class Status():
    '''bottom status bar'''
    def __init__(self):        
        self.wpm = tk.StringVar() #variable to store wpm
        
        self.status = tk.Frame(root, bg = colors["status"]["bg"], height = 10) #display status bar
        self.status.pack(fill ="x", side = "bottom")
        
        self.word_count = tk.Label(self.status, textvariable = self.wpm, bg = colors["status"]["bg"], fg=colors["status"]["fg"])  #display wpm counting
        self.word_count.pack(side = "right", padx=3, pady = 3)  #display "wpm"
        tk.Label(self.status, text = "wpm :", bg = colors["status"]["bg"], fg=colors["status"]["fg"]).pack(side="right")

        self.line_count = tk.StringVar() #variable to count no. of lines
        self.line = tk.Label(self.status, textvariable = self.line_count, fg=colors["status"]["fg"], bg =colors["status"]["bg"])  #display no. of lines
        self.line.pack(side = "right")
        tk.Label(self.status, text="Lines :", fg=colors["status"]["fg"], bg =colors["status"]["bg"]).pack(side ="right")

        self.cur_line = tk.StringVar()  #stores current line info
        self.cur_col = tk.StringVar()  #stores current column info

        self.show_cur_line = tk.Label(self.status, textvariable = self.cur_line, bg = colors["status"]["bg"], fg=colors["status"]["fg"])  #shows current line number
        self.show_cur_line.pack(side = "right")
        tk.Label(self.status, text = "Ln :", bg = colors["status"]["bg"], fg=colors["status"]["fg"]).pack(side = "right")
        
        self.show_cur_col = tk.Label(self.status, textvariable = self.cur_col, bg = colors["status"]["bg"], fg=colors["status"]["fg"])  #shows current column number
        self.show_cur_col.pack(side = "right")
        tk.Label(self.status, text = "Col :", bg = colors["status"]["bg"], fg=colors["status"]["fg"]).pack(side = "right")

        self.reset = tk.Button(self.status, text= "Reset", fg=colors["status"]["fg"], bg =colors["status"]["bg"], relief = "flat",command=self.reset_editor)  #button to reset whole editor
        self.reset.pack(side ="left", padx = 5, pady = 3 )

    #<<<<<<<<GET LOCATION>>>>>>>
    def get_loc(self, event):
        self.position = editor.index("insert").split(".") #gets current position
        self.cur_line.set(self.position[0]) #sets line no.
        self.cur_col.set(self.position[1]) #sets column no.
        return self.position

    #<<<<<RESET EDITOR>>>>>>>>>>>
    def reset_editor(self): #Resets editor
        global sec, brk, editor, n
        self.confirm = messagebox.askyesno("Cofirm Reseting", "Are you to reset whole document?")
        if self.confirm == True:
            self.line_count.set("0")
            sec = 1
            brk = 0
            self.wpm.set("0")
            editor.delete(1.0, "end")
            n = True

    #<<<<< WPM COUNTER >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def count_wpm(self):
        '''counts number of words per minute
        counts number of lines'''
        global editor, brk, n, prev, sec
        if brk < 3:
            a= tt.time()
            sec+=1
            self.total_words = len(editor.get(1.0, "end-1c").split()) #gets number of words
            count = str((self.total_words/sec)*60)[:5]  #counts wpm
            self.wpm.set(count)   #sets value to display
            self.line_count.set(editor.count(1.0, "end", "line"))  #sets number of lines
            if int(self.total_words) == int(prev): #looks for inactivity
                brk+=1

            prev = self.total_words #stores previous number of words

            b=a-tt.time()  #execution time
            root.after(int(1000-b*100), self.count_wpm) #repeats loop
        else:
            n = True
            
    def trigger_wpm(self, event): 
        '''starts count_wpm()'''
        global n, brk
        brk = 0 #starts looking for inactivity again
        if n:
            self.count_wpm() 
        n = False


class Find():
    '''class to find elements'''
    def create(self):
        '''create find gui'''
        destroy_widget() #will destroy widgets in frame
        self.searchvar = tk.StringVar() #varible stores input

        f = tk.Frame(tray, bg = colors["tray"]["bg"])
        tk.Label(f, text = "Find :", bg = colors["tray"]["bg"], fg =colors["tray"]["fg"]).pack(side = "left", anchor = "n", pady = 3)

        self.serach_input = tk.Entry(f, textvariable = self.searchvar) #takes input
        self.serach_input.pack(side = "left", anchor = "n", pady =3)
        f.pack()

        f = tk.Frame(tray, bg = colors["tray"]["bg"])
        self.nxt_bt = tk.Button(f, text= "Next", bg = colors["tray"]["bg"], fg =colors["tray"]["fg"], command =self.next_)
        self.nxt_bt.pack(side = "right", padx = 3, pady =3) #next button

        self.search_bt = tk.Button(f, text= "Search", bg = colors["tray"]["bg"], fg =colors["tray"]["fg"], command = self.search)
        self.search_bt.pack(padx = 3, pady =3, side = "right") #search button

        self.prev_bt = tk.Button(f, text= "Prev", bg = colors["tray"]["bg"], fg =colors["tray"]["fg"], command = self.prev_)
        self.prev_bt.pack(side = "left", padx = 3, pady =3)#previous button
        f.pack()

        self.clear_bt = tk.Button(tray, text= "Clear", bg = colors["tray"]["bg"], fg =colors["tray"]["fg"], command = self.clear)
        self.clear_bt.pack(pady = 3)         
        self.search_hist = ['']

    def search(self):
        '''this searches and highlight search result'''
        if self.searchvar.get() != "":
            self.index = [] #stores index of found results
            editor.tag_delete(self.search_hist[-1]) #deletes recent search result
            self.count = tk.StringVar()  #gets length of word
            
            self.n = "1.0" #iterate index for different part of search
            while True:
                self.find = editor.search(self.searchvar.get(), self.n, stopindex = tk.END, count = self.count) #finds given word
                if self.find == "":
                    break
                    
                self.index.append(self.find) #append search history
                self.n = f"{self.find}+ {self.count.get()}c " #moves to next index
                editor.tag_add(self.searchvar.get(), self.find, self.n) #mark search result
                editor.tag_config(self.searchvar.get(), background = "blue") #highlights search result
            self.search_hist.append(self.searchvar.get())
            editor.focus_set()

    def next_(self):
        '''moves to next result'''
        self.current_position = editor.index("insert")  #gets current position of cursor
        self.get = editor.search(self.searchvar.get(), self.current_position+"+1c",stopindex = tk.END )
        editor.mark_set("insert", self.get) #sets cursor
        editor.see("insert")
        

    def prev_(self):
        '''moves to prev result'''
        
        self.current_position = editor.index("insert")  #gets current position of cursor
        self.get = editor.search(self.searchvar.get(), self.current_position+"-1c",stopindex = 1.0, backwards = True )
        editor.mark_set("insert", self.get)#sets cursor
        editor.see("insert")
               
    def clear(self): #clear searched tags
        editor.tag_delete(self.search_hist[-1])            

class FileMenu():
    '''handle file menu'''    
    def __init__(self):
        self.file_menu = tk.Menu(menu, tearoff = 0, bg = colors["menu"]["bg"], fg = colors["menu"]["fg"])
        self.file_menu.add_command(label = "Open") 
        self.file_menu.add_command(label = "Save") 
        self.file_menu.add_command(label = "Save as")
        menu.add_cascade(menu = self.file_menu, label = "file") 

        
#<<<<<Destroy widget in frame>>>>>>>>
def destroy_widget():
    for widget in tray.winfo_children():
            widget.destroy()
    tray.config(width = 50)

#<<<<<About>>>>>>>>
def abt():
    destroy_widget()
    tk.Label(tray, text = "This editor is made bt Naveen. \n All copyrights are reserved by me 2020", bg=colors["tray"]["bg"], fg = colors["tray"]["fg"] ).pack()


#<<<<<<<<<<< GUi >>>>>>>>>>>>>>>
root = tk.Tk()
root.title("Type Master")
root.state("zoomed")



menu = tk.Menu(root, background = colors["menu"]["bg"])
root.config(menu = menu)

file = FileMenu()

status = Status()  #creates status bar
root.bind("<Key>", status.get_loc)

tool = tk.Frame(root, bg = colors["tools"]["bg"], width = 50) #side menu frame
tool.pack(fill = "y", side = "left")

find_obj = Find() # Find object
find_button = ToolButtons(tool,"find.png", "Find", find_obj.create) #Find button
about_button = ToolButtons(tool, "about.png", "about", abt) #about Button

tray = tk.Frame(root, bg = colors["tray"]["bg"], relief = "ridge", borderwidth =3)  #frame to display selected options 
tray.pack(fill = "y", side = "left")



editor = sc.ScrolledText(root, font = f'{colors["editor"]["font"]}', bg = colors["editor"]["bg"], fg = colors["editor"]["fg"], insertbackground = "light green", insertwidth = 3, relief = "flat", borderwidth = 5)

editor.pack(fill = "both", expand = 1)
editor.bind("<Key>", status.trigger_wpm) 
editor.delete(1.0, "end+1c")

root.mainloop()
