import tkinter
import re
import os.path

### NOTES

#Frames are important for packing items in the correct places.
#Frames are stacked from top to bottom.TkinterInputs
#Items inside are packed from left to right.

#Each input from create entry row is added is argv to be used later

#easy row based interface class
class eRBI:
	def _init_(HorizontalSize):
	TkinterInputs = {}
	VerticalFrames = 0
	self.HorizontalSize = HorizontalSize


def makeWindow(name):
	Interface = tkinter.Tk()
	Interface.title(name)

#limits the number of characters that can be given in an entry
def characterLimit(entryText, inputSize):
	if len(entryText.get()) > inputSize:
		entryText.set(entryText.get()[:inputSize])

def changeSubmitStatus(pushState,message):
	tkinter.submitButton.pack_forget()
	tkinter.statusMessage.pack_forget()
	tkinter.submitButton['state'] = pushState #not sure why changing button state is different than changing any other properity of any other item in tkinter
	tkinter.statusMessage.config(text=message)
	tkinter.submitButton.pack(side="left")
	tkinter.statusMessage.pack(side="left")

def checkFile():
	if os.path.exists(TkinterInputs['filePath'].get()) == False: #bad path
		changeSubmitStatus("disabled","This file could not be found")
	elif os.path.isdir(TkinterInputs['filePath'].get()) == True: #path leads to a directory
		changeSubmitStatus("disabled","This is not a file")
	elif re.search("\.(d|t|c)sv$",TkinterInputs['filePath'].get()) is None: #path leads to a generic file
		changeSubmitStatus("normal","This file may not contain delimiter seperated values, do you want to continue?")
		tkinter.submitButton.configure(command=lambda *args: makeNewFile())
	else: #path leads to a leads to a .dsv, .tsv, or .csv file
		changeSubmitStatus("normal","File Found")
		tkinter.submitButton.configure(command=lambda *args: makeNewFile())

def createEntryRow(inputName, text):
	frame = tkinter.Frame()
	tkinter.Label(frame,text=text).pack(side="left")

	entryText = tkinter.StringVar()
	TkinterInputs[inputName] = entryText

	tkinter.Entry(frame,width=HorizontalSize,textvariable=entryText).pack(side="left",fill="x")
	entryText.trace("w",lambda *args: checkFile())

	frame.pack(fill="x")
	global VerticalFrames
	VerticalFrames +=1
	return frame

def createLimitedEntryRow(inputName, text, inputSize):
	frame = tkinter.Frame()
	tkinter.Label(frame,text=text).pack(side="left")

	entryText = tkinter.StringVar()
	TkinterInputs[inputName] = entryText

	tkinter.Entry(frame,width=inputSize+2,textvariable=entryText,justify="center").pack(side="left",fill="x")
	entryText.trace("w",lambda *args: characterLimit(entryText,inputSize))

	frame.pack(fill="x")
	global VerticalFrames
	VerticalFrames +=1
	return frame

def createLableRow(text):
	frame = tkinter.Frame()
	tkinter.Label(frame,text=text).pack(side="left")

	frame.pack(fill="x")
	global VerticalFrames
	VerticalFrames +=1
	return frame

def createSubmitRow():
	frame = tkinter.Frame(Interface)
	# *** I am not able to make, set, and pack a frame in a single line, i have to pack it later
	submit = tkinter.Button(frame, text="Submit", state="disabled")
	submit.pack(side="left")
	status = tkinter.Label(frame,text="")
	frame.pack(fill="x")
	global VerticalFrames
	VerticalFrames +=1
	return [submit,status]


	

def startWindow(): #has to go at the end
	Interface.geometry(f"{HorizontalSize}x{VerticalFrames*25}") # widthxheight+x+y
	Interface.mainloop()
