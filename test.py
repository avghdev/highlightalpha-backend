#! python3

#GUI
import tkinter

#GUI extends Frame, serving as main container for a root window 
class GUI(tkinter.Frame):
    
    #constructor forith a default height and width if none are given
    def __init__(self, master, ht=600, wt=800):

        #uses the parent class' constructor
        super().__init__(master, height=ht, width=wt)
        self.var = tkinter.StringVar()
        self.var.set("No copied text")
        self.pack_propagate(False) #window will use it's own width and height as parameters instead of child's dimensions
        self.pack()
        self.label = tkinter.Label(self, textvariable=self.var)
        self.label.pack()

    #method to update the label
    def update_label(self, newText):
        self.var.set(newText)
        self.label.pack()
        self.master.update()

#returns true if clipboard has changed, false if not 
def check_clipboard(window, recent_value):
    #grab clipboard value 
    temp_value = window.master.clipboard_get()

    if temp_value != recent_value:
        return True

    return False
    
#recursive method that checks if clipboard has changed after each window update 
def run_listener(window, interval, recent_value):
    #if clipboard has changed then update the current value of label
    if check_clipboard(window, recent_value):
        recent_value = window.master.clipboard_get()
        window.update_label(recent_value)
    #will call run_listener again after the window updates in .mainloop()
    window.master.after(interval, run_listener, window, interval, recent_value)



def main():
    #GUI initialized
    root = tkinter.Tk()
    gui = GUI(root)
    recent_value = root.clipboard_get()

    run_listener(gui, 200, recent_value)

    root.mainloop()
        
    
#only run this program if it is being used as the main program file
if __name__ == "__main__":
    main()
    

    
    


