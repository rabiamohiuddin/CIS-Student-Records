# GUI with Tkinter, OOP
# Rabia Mohiuddin
# Winter 2018

import tkinter as tk
import tkinter.messagebox as tkmb
from dialog import Dialog 
import platform
import os

# class AddStudentDialog
class AddStudentDialog(Dialog) : 
    studentVals = {}
    
    def body(self, bFrame):
        ''' Sets up labels and entry boxes using frame provided '''
        tk.Label(bFrame, text="Student ID:").grid(row=0, column=0, sticky='e')     # label for student ID
        tk.Label(bFrame, text="Name:").grid(row=1, column=0, sticky='e')           # label for name
        tk.Label(bFrame, text="Favorite Language: ",).grid(row=2, column=0, sticky='e')   # label for fav lang
        
        self.sID = tk.StringVar()
        tk.Entry(bFrame, textvariable=self.sID, highlightcolor='light blue').grid(row=0, column=1) 
        
        self.name = tk.StringVar()
        tk.Entry(bFrame, textvariable=self.name, highlightcolor='light blue').grid(row=1, column=1) 
        
        self.language = tk.StringVar()
        tk.Entry(bFrame, textvariable=self.language, highlightcolor='light blue').grid(row=2, column=1)         
        
        #       |       col 0        |         col 1      |
        # ----------------------------------------------------
        # row 0 |        Student ID: | |__________________|
        # row 1 |              Name: | |__________________|
        # row 2 | Favorite Language: | |__________________|
        
    def validate(self):
        ''' Validate fields filled and depending on language answered, send a pop up message '''
        if self.sID.get() == "" or self.name.get() == "" or self.language.get() == "":  # all fields need to be filled
            tkmb.showerror("Field(s) blank", "All fields must be completed to continue")
            return False
        
        if not self.sID.get().isdigit() or not len(self.sID.get()) == 3:    # ID is only 3 digits
            tkmb.showerror("Student ID Error", "Student ID must be a three digit number")            
            return False
        
        if self.language.get().lower() != "python":     # check if not python and pop up message
            tkmb.showinfo("Favorite Language", "Too bad your favorite language isn't Python!")
        
        return True     # if all is well, continue
        
    def apply(self):
        ''' Store vals to dictionary '''
        self.studentVals["Student ID"] = self.sID.get()
        self.studentVals["Name"] = self.name.get()
        self.studentVals["Favorite Language"] = self.language.get()
        
        
# class MainWindow
class MainWindow(tk.Tk) :
    
    def __init__(self) :
        ''' Constructor - sets up main window to add students to list and shows current count of students '''
        super().__init__()      # initialize Tk parent class
        self.numStus = tk.IntVar()
        #self.LofStus = []       # if need to save all students
        
        self.title("Lab 3")                     # add title to window   
        self.resizable(True, False)             # horizontal only
        
        Ldesc = tk.Label(self, text="Add a Student").grid(row=0, column=0)           # label for description
        addStu = tk.Button(self, text = "Click to Add", command=lambda:self.addStudent()).grid(row=0, column=1)    # button to add student
              
        Lcount = tk.Label(self, text="Student Count =").grid(row=1, column=0, sticky='es', pady=5)     # current Student count
        Lcountval = tk.Label(self, textvariable=self.numStus, justify='left').grid(row=1, column=1, sticky='ws', pady=5)
        
        LstuList = tk.Label(self, text="Student List").grid(row=0, column=2)           # label for Student Lis        
        s = tk.Scrollbar(self)           # create scrollbar         
        self.lbox = tk.Listbox(self, height=3, yscrollcommand=s.set, width=50)     # shows 3 lines, connects scroll
        self.lbox.grid(row=1, column=2, sticky='nswe', pady=5)
        self.grid_columnconfigure(2, weight=1, minsize=100)  # expands list box is x direction
        # connect scrollbar to listbox
        s.config(command=self.lbox.yview)    # as you scroll it will show with the lbox
        s.grid(row=1,column=3, sticky='nsw', pady=5)  # put scroll bar in the grid        
  
         
        #       |      col 0       |     col 1      |       col 2
        # -----------------------------------------------------------------
        # row 0 |   Add a Student  | |Click to Add| |     Student List
        # row 1 |                  |                ||                    |
        #       |                  |                ||                    |
        # row 2 |                  |                ||____________________|        
        #       |  Student Count = | n 
            
    def addStudent(self):
        ''' instantiates AddStudentDialog object to get data for student and displays in listbox '''
        asd = AddStudentDialog(self).studentVals
        if asd:     # if student data returned
            self.lbox.insert(tk.END, asd)   # inseert student data to end of listbox
            #self.LofStus.append(asd)        # when saving all students
            self.numStus.set(self.numStus.get() + 1)    # set current num of students to current val + 1


def main() :
    win = MainWindow()
    if platform.system() == 'Darwin': 
        tmpl = 'tell application "System Events" to set frontmost of every process whose unix id is %d to true'
        os.system("/usr/bin/osascript -e '%s'" % (tmpl % os.getpid()))
    win.mainloop()

main()
