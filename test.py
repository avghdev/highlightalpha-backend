#! python3

#GUI
import tkinter
#needed for the clipboard event detection
import time
import threading

#listener class that inherits from Thread 
class ClipListener(threading.Thread):
    #overriding Thread constructor
    def __init__(self, pause = 5.):
        #from documentation: If the subclass overrides the constructor, it must make sure to invoke the base class constructor (Thread.__init__()) before doing anything else to the thread.
        super().__init__() #calls Thread class constructor first
        #initialize parameters 
        self.pause = pause
        self.stopping = False

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
                print(last_value)
            time.sleep(self.pause) #sleep for indicated amount of time (5. by default)

    #override stop method to work with our paramter 'stopping'
    def stop(self):
        self.stopping = True

def main():
    #good practice to have a variable to stop the loop
    running = True

    #initialize listener and start the new thread
    listener = ClipListener(.500)
    listener.start()
    

main()
        

    
    


