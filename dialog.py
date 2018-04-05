# Dialog window base class
# Rabia Mohiuddin
# Winter 2018

import tkinter as tk
from abc import ABC, abstractmethod     # abstract base class

class Dialog(tk.Toplevel, ABC):    # Multiple inheritance: Dialog gets the attributes of TopLevel and ABC
    """Base Dialog() class
       - Has standard features of a dialog box: 
          - a window with [OK] and [Cancel] buttons
          - [OK] to commit a transaction, [Cancel] to cancel a transaction
       - Derived dialog boxes can be created with a small amount of customization"""

    def __init__(self, master, title=None, **kwargs):    # Q1. what is kwargs and why would this base class want to use it? -> dictionary allows you to specify any keyworded additional options you may want to add to the base class.
        """ set up window with title, body, [OK] and [Cancel] buttons, and controls"""
        
        ABC.__init__(self)
        tk.Toplevel.__init__(self, master, **kwargs)  # self is Dialog, 
                                            # master is window that Dialog is spawned from, which in lab 3 is MainWindow
                                            # master needs to be passed in so that if master closes, then all spawned windows will go away

        self.grab_set()                                 # Make Dialog modal (Dialog grabs all focus, master is not active)
        self.protocol("WM_DELETE_WINDOW", self.cancel)  # Make "X" same as [Cancel] button, cancel is callback function

        self._master = master           # save master window for this Dialog instance
        self.result = None              # result is *public* data that can be accessed outside the class.
                                        # result has the user input that is the result of the dialog with the user
        if title:
            self.title(title)           # Q2. What does this if statement do? -> If the user specifies a title for the window, set the title to what they entered

        self.v = tk.StringVar()         # Provide a generic StringVar v that can be used to store user input data for the transaction
        self.v.set('ERROR: uninitialized data')    # if a derived class wants to use v, it must set v

        bodyFrame = tk.Frame(self)                      # Create empty body frame for derived class to fill
        self.initial_focus = self.body(bodyFrame)       # Call the body() method to populate the window's body.
                                                # The body method will return a widget, and the focus will be on the returned widget.
                                                # Having a focus on a widget means the cursor will be at that widget.
                                                           
        bodyFrame.pack(padx=5, pady=5, fill=tk.BOTH, expand='y')  

        self.buttonbox()                        # create [OK] and [Cancel] buttons as another frame

        if not self.initial_focus:              # if focus is not on a widget, then focus is Dialog 
            self.initial_focus = self
        self.initial_focus.focus_set()          # set the focus
        
        # Q3. Explain where the focus could be. There are 3 possibilities, with a certain precedence: first, second, third
        # List the 3 locations in order. -> widget in body frame, button, dialog window

        self.transient(master)      # Set Dialog to be transient to the master:
                                    # This means: 1. Dialog will minimize if master is minimized 
                                    # 2. Dialog causes no extra icon on taskbar
                                    # 3. Dialog appears on top of master

        self.geometry("+%d+%d" % (master.winfo_rootx()+50, master.winfo_rooty()+50)) # place Dialog window on right and down from master
        self.resizable(False,False) # Don't allow Dialog to be sizeable

        self.wait_window(self)      # Stay open until Dialog is closed by the user
    #
    #=====  methods for appearance and behavior of Dialog  =====
    #
    @abstractmethod
    def body(self, bodyFrame):
        """Create dialog body.  Return widget that should have initial focus."""
        raise NotImplementedError

    def buttonbox(self):
        """Add [Ok] and [Cancel] buttons]"""
        box = tk.Frame(self)

        self.b_ok = tk.Button(box, text="OK", width=10, command=self.ok) 
        self.b_ok.pack(side=tk.LEFT, padx=5, pady=5)
        self.b_cancel = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        self.b_cancel.pack(side=tk.LEFT, padx=5, pady=5)

        if not self.initial_focus:
            self.initial_focus = self.b_cancel

        self.bind("<Return>", self.return_)        # bind() method connects a pressed key event
        self.bind("<Escape>", self.cancel)         # to a method through a callback

        box.pack()
        
    @abstractmethod
    def validate(self):
        """Return True if all dialog options are valid"""
        raise NotImplementedError        

    def ok(self, *args):
        """[Ok] button to commit change"""
        if not self.validate():                     # if not valid
            self.initial_focus.focus_set()          # put focus back to initial focus
            return

        self.apply()                # if everything is valid, then store input data into result
        self.cancel()               # go to close window

    def cancel(self, *args):
        """[Cancel] button to close window"""
        self._master.focus_set()    # set focus back to the master window
        self.destroy()              # close window

    def return_(self, *args):
        """Hitting return will run the button that has focus"""
        if self.focus_get() == self.b_cancel:
            self.cancel()
        elif self.focus_get() == self.b_ok:
            self.ok()

    def apply(self):
        """set result to valid user input data"""
        self.result = self.v.get()   # result defaults to the generic StringVar v variable
                                     # If derived class handles multiple data in a data structure
                                     # then the derive class should override this method so result
                                     # can be a data structure.

# Q4. Name all the callback methods -> ok, cancel, return
