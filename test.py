#! python3

#GUI
import tkinter

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

        self.text_list = []
        
        #create the initial labels and return the amount of labels to an object variable
        self.create_labels()
        self.pack_propagate(False) #window will use it's own width and height as parameters instead of child's dimensions
        self.pack()

    #method for creating the labels that hold the clipboard snippets 
    def create_labels(self):
        
        #create an array to hold the label text in
        text_list = []
        
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
                    text_list.append(new_string)

                    #grab next line to be analyzed
                    temp = file.readline()
                    temp = temp.rstrip("\n")

        #add label text to respective labels and pack in
        for string in text_list:
            label = tkinter.Label(self, text = string, bg = "blue")
            label.pack()

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


#returns true if clipboard has changed, false if not 
def check_clipboard(window, recent_value):
    #grab clipboard value 
    temp_value = window.master.clipboard_get()

    if temp_value != recent_value:
        return True

    return False
    
#checks if clipboard has changed after each window update, sets a flag with .after() that recalls the method after each iteration of .mainloop()
def run_listener(window, interval, recent_value):
    
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
    recent_value = root.clipboard_get()

    run_listener(gui, 50, recent_value)

    root.mainloop()
        
    
#only run this program if it is being used as the main program file
if __name__ == "__main__":
    main()
