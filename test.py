#! python3

#GUI
import tkinter
import random

#GUI extends Frame, serving as main container for a root window 
class GUI(tkinter.Frame):
    
    #constructor; use a default height and width if none are given
    def __init__(self, master, ht=600, wt=800):
        #uses the parent class' constructor
        
        super().__init__(master, height=ht, width=wt)
        
        #try to open the file - if doesn't exist then make it and add file end tag
        try:
            open("saved_snippets.txt")
        except:
            with open("saved_snippets.txt","w") as file:
                file.write("{{{fend}}}")

        #List for storing text in labels - Redundant(?)
        self.text_list = []
        
        #variable to store current text in
        self.current_copy = ""

        #frame for labels/buttons
        self.label_frame = tkinter.Frame(self)
        self.create_labels()

        #Pack everything using grid geometry manager
        self.label_frame.grid(row=0)
        self.grid()

        self.master.lift()

    #button callback method
    def callback(self, string):
            #clear current clipboard text
            self.master.clipboard_clear()
            #text to clipboard
            self.master.clipboard_append(string)
            #set text to current clipboard value
            self.current_copy = string

    #method for creating the labels that hold the clipboard snippets 
    def create_labels(self):
        
        #array to hold the label text in
        self.text_list = []
        
        #open files using 'with'
        with open("saved_snippets.txt","r") as file:
            
            #grab first line of text {strip \n if it is there}
            temp = file.readline()
            temp = temp.rstrip("\n")

            #check to see if the line is == to file end tag
            while temp != "{{{fend}}}":

                #check to see if line is == to snippet scan start tag
                if temp == "{{{start}}}":

                    #set first line to the new snippet
                    new_string = file.readline()
                    new_string = new_string.rstrip("\n")

                    #possibile bug could occur here if the file is somehow set up like {{{start}}}{{{end}}}

                    #read next line to be analyzed
                    temp = file.readline()
                    temp = temp.rstrip("\n")

                    #check to see if the next line is the scan stop tag - if not continue loop
                    while temp != "{{{stop}}}":

                        #add line to overall new string 
                        new_string = new_string + "\n" + temp

                        #grab next line 
                        temp = file.readline()
                        temp = temp.rstrip("\n")

                    #add completed snippet to the list of label text
                    self.text_list.append(new_string)

                    #grab next line to be analyzed
                    temp = file.readline()
                    temp = temp.rstrip("\n")

            #variable to keep track of index
            index = 0
            
            #add label text to respective labels and pack in - NEED TO IMPROVE GUI
            for string in self.text_list:
                
                #create label and buttons
                label = tkinter.Label(self.label_frame, text = string, bg = random_color(), anchor="w")
                button = tkinter.Button(self.label_frame, text="copy", command = lambda s=string: self.callback(s)) #lambda creates a function reference so that it will work correctly
                
                #pack them in with the grid manager 
                label.grid(row=index, sticky="w"+"e")
                button.grid(row=index, column=1)
                index += 1
        
#copies parameter 'value' to a file 'saved_snippets'    
def write_to_file(value):
    #save all the lines in the current file
    infile = open('saved_snippets.txt','r').readlines()

    #open file in write mode (deletes current contents)
    with open('saved_snippets.txt','w') as outfile:

        #copy lines over from original except for last line
        for line in infile:
            if line.rstrip("\n") != "{{{fend}}}":
                outfile.write(line)
                
    #add the new values at the end of the file including the fileend tag
    with open("saved_snippets.txt","a") as file:
        file.write("{{{start}}}\n" + value + "\n{{{stop}}}\n")
        file.write("{{{fend}}}")
        
#random color
def random_color():
    #create a function pointer
    r = lambda: random.randint(0,255)
    #return formatted tuple
    return ('#%02X%02X%02X' % (r(), r(), r()))

#returns true if clipboard has changed, false if not 
def check_clipboard(window, recent_value):
    #grab clipboard value 
    temp_value = window.master.clipboard_get()

    if temp_value != recent_value and temp_value != window.current_copy:
        if temp_value != "":
            return True

    return False
    
#checks if clipboard has changed after each window update, sets a flag with .after() that recalls the method after each iteration of .mainloop()
def run_listener(window, interval, recent_value):

    global copy_flag
    
    #if clipboard has changed then update the current value of label
    if check_clipboard(window, recent_value):
        
        #store the root tkinter window
        root = window.master
        
        #grab the new clipboard value
        recent_value = root.clipboard_get()
        
        #write the value to the file
        write_to_file(str(recent_value))

        #destroy the current frame with the old values and make a new frame with the new values
        window.destroy()
        window = GUI(root)
        
    #will call run_listener again after the window updates in .mainloop()
    window.master.after(interval, run_listener, window, interval, recent_value)
    

def main():
    
    #GUI initialized
    root = tkinter.Tk()
    gui = GUI(root)

    #Try/Except for Windows Compatibility
    try:
        recent_value = root.clipboard_get()
    except:
        root.clipboard_append("")
        recent_value = root.clipboard_get()

    run_listener(gui, 50, recent_value)

    root.mainloop()
        
    
#only run this program if it is being used as the main program file
if __name__ == "__main__":
    main()
