#! python3

#GUI
import tkinter
#needed for the clipboard event detection
import time
import threading

#listener class that inherits from Thread 
class ClipListener(threading.Thread):
    #overriding Thread constructor
    def __init__(self, pause = .5):
        #from documentation: If the subclass overrides the constructor, it must make sure to invoke the base class constructor (Thread.__init__()) before doing anything else to the thread.
        super().__init__() #calls Thread class constructor first
        
        #initialize parameters 
        self.pause = pause
        self.stopping = False
        
        #initialize event to communicate with main thread 
        self.copyevent = threading.Event()

    #override run method
    def run(self):
        last_value =  tkinter.Tk().clipboard_get() #initialize last_value as 

        #continue until self.stopping = true
        while not self.stopping:
            #grab clip_board value 
            temp_value = tkinter.Tk().clipboard_get()
            #if last value is not equal to the temp_value, then (obviously) a change has occurred
            if temp_value != last_value:
                #set last value equal to current (temp) value and print
                last_value = temp_value
                print("set")
                #set the event if clipboard has changed 
                self.copyevent.set()
            time.sleep(self.pause) #sleep for indicated amount of time (.5 by default)

    #override stop method to work with our paramter 'stopping'
    def stop(self):
        self.stopping = True

#GUI extends Frame, serving as main container for a root window 
class GUI(tkinter.Frame):
    
    #constructor for GUI - intializes with a default height and width if none are given
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
        
        
    
def main():
    #good practice to have a variable to stop the loop
    running = True

    #GUI initialized
    root = tkinter.Tk()
    gui = GUI(root)

    #start thread containing Clipboard Listener 
    listener = ClipListener(.100)
    listener.start()
    

    #loop to keep updating the program without blocking the clipboard checks (since mainloop() is blocking)
    while running:
        #update the gui
        root.update();
        #wait .1 seconds for event to be set to true
        event_set = listener.copyevent.wait(.100)
        #if true then update the label and reset event
        if event_set:
            gui.update_label(root.clipboard_get())
            listener.copyevent.clear()
        
    
#only run this program if it is being used as the main program file
if __name__ == "__main__":
    main()
    

    
    


