import tkinter
import os.path
import re


### FRONTEND

interface = tkinter.Tk()
interface.title("NicePrintDSV")
interface.geometry("700x150+0+0") # widthxheight+x+y
argv = []

#Makes a new place to display and enter information
#each new input gets added to argv
#frame is important for plesently packed formatting
def entryRow(lable, inputSize):
	frame = tkinter.Frame()
	entryText = tkinter.StringVar()
	argv.append(entryText) 
	tkinter.Label(frame,text=lable).pack(side="left")
	if inputSize <= 0: #don't include a entry
		Input = tkinter.Label(frame)
	elif inputSize < 4: #an entry with given limited characters
		Input = tkinter.Entry(frame,width=inputSize+2,textvariable=entryText,justify="center")
		entryText.trace("w",lambda *args: characterLimit(entryText,inputSize))
	else: #an entry with no limit but a given visable size
		Input = tkinter.Entry(frame,width=inputSize,textvariable=entryText)
		#I wanted to make it so that an input size of 0 makes the input as long
		# as the text inside and -1 makes it as long as the window can provide, 
		# but those are not going to happen now, i can't figure it out, 
		# now 0 is 2, -1 is 1, -2 is 0, and idk what less would end up being
	entryText.trace("w",lambda *args: changeStatus(0))
	Input.pack(side="left",fill="x")
	frame.pack(fill="x")
	return frame

#limits the number of characters in an entry
def characterLimit(entryText, inputSize):
	if len(entryText.get()) > inputSize:
		entryText.set(entryText.get()[:inputSize])

#changes the status message and force button depending on the status
def changeStatus(status):
	statusMessage.pack_forget()
	forceSubmit.pack_forget()
	if status == 0:
		statusMessage.config(text="")
	elif status == 1: 
		statusMessage.config(text="This file could not be found")
	elif status == 2: 
		statusMessage.config(text="This file may not contain delimiter seperated values, do you want to continue?")
		forceSubmit.pack(side="left")
	elif status == 3:
		statusMessage.config(text="Creating file...")
	statusMessage.pack(side="left")

#creates a row of submission items and returns an array of items that can be changed depending on the submission status
def submitRow():
	Frame = tkinter.Frame(interface)
	print(tkinter.Button(Frame, text="Submit", command=CheckFile).pack(side="left"))
	status = tkinter.Label(Frame,text="")
	forceSubmit = tkinter.Button(Frame,text="Create File Anyway",command=makeNewFile(argv[3]))
	Frame.pack(fill="x")
	print(forceSubmit)
	return [status,forceSubmit]



### BACKEND
def CheckFile():

	#unpack items that may change
	changeStatus(0)

	#checks if filepath is correct
	filePath = argv[3].get()
	if os.path.exists(filePath) != True: 
		changeStatus(1)
	#elif if it does not have an extention:
		#statusMessage.config(text="This is not a file")
		#statusMessage.pack(side="left")
	#if the extention of filePath != .csv or .tsv or .dsv: 
		#statusMessage.config(text="This file may not contain delimiter seperated values, do you want to continue?")
		#statusMessage.pack(side="left")
		forceSubmit.pack(side="left")
		
	else: makeNewFile(filePath)


#work in progress
def makeNewFile(filePath):
	columnDelim = argv[0].get()
	rowDelim = argv[1].get()
	if rowDelim == "" : rowDelim = "\n"
	pageDelim = argv[2].get()
	#print(columnDelim,rowDelim,pageDelim,filePath)
	#origionalFile = open(filePath, "r")
	#resultingFile = open(filePath, "w")
	#read through file






### INITATION

entryRow("This program takes a delimiter seperated value file and will create a copy of it that is nicely formatted for printing pourposes.",-2)
entryRow("Delimiter between columns of data:",1)
rowFrame = entryRow("Delimiter between rows of data:",1)
tkinter.Label(rowFrame, text=" (\\n unless given)").pack(side="left")
entryRow("Delimiter for fitting more data per page:",3)
entryRow("Enter File Path:",100)
submitItems = submitRow()
statusMessage = submitItems[0]
forceSubmit = submitItems[1]

###issue with 


#has to go at the end
interface.mainloop()