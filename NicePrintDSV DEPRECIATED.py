import tkinter
import os.path
import pathlib
import re
import ovEasyRowBasedGUI

### NOTES

#Frames are important for packing items in the correct places.
#Frames are stacked from top to bottom.TkinterInputs
#Items inside are packed from left to right.

#Each input from create entry row is added is argv to be used later


### FRONTEND
TkinterInputs = {}
VerticalFrames = 0
HorizontalSize = 750

#limits the number of characters that can be given in an entry
def characterLimit(entryText, inputSize):
	if len(entryText.get()) > inputSize:
		entryText.set(entryText.get()[:inputSize])

def changeSubmitStatus(pushState,message):
	submitButton.pack_forget()
	statusMessage.pack_forget()
	submitButton['state'] = pushState #not sure why changing button state is different than changing any other properity of any other item in tkinter
	statusMessage.config(text=message)
	submitButton.pack(side="left")
	statusMessage.pack(side="left")

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



### BACKEND

def checkFile():
	if os.path.exists(TkinterInputs['filePath'].get()) == False: #bad path
		changeSubmitStatus("disabled","This file could not be found")
	elif os.path.isdir(TkinterInputs['filePath'].get()) == True: #path leads to a directory
		changeSubmitStatus("disabled","This is not a file")
	elif re.search("\.(d|t|c)sv$",TkinterInputs['filePath'].get()) is None: #path leads to a generic file
		changeSubmitStatus("normal","This file may not contain delimiter seperated values, do you want to continue?")
		submitButton.configure(command=lambda *args: makeNewFile())
	else: #path leads to a leads to a .dsv, .tsv, or .csv file
		changeSubmitStatus("normal","File Found")
		submitButton.configure(command=lambda *args: makeNewFile())

#C:\Users\Owen\OneDrive\2 - Employment\Current Work\Helpdesk\DSVs\Call Transfers.dsv
def makeNewFile():
	changeSubmitStatus("disabled","Creating file...")

	#-------------------------------------------------
	#translate dict of tkinter stringvars into dict of strings once file creation process has begun
	#set default arguments when necessary
	inputs = {}
	for item in TkinterInputs.items():
		inputs[item[0]] = item[1].get()

	if inputs["columnDelim"] == "" : inputs["columnDelim"] = "\t"
	if inputs["rowDelim"] == "" : inputs["rowDelim"] = "\r\n"
	if inputs["spacerChar"] == "" : inputs["spacerChar"] = "·"
	#print(f"columndelim{inputs['columnDelim']} rowdelim{inputs['rowDelim']} pagedelim{inputs['pageDelim']},inputs['filePath'])
	#-------------------------------------------------

	#-------------------------------------------------
	#pathlib suggested by sourcery,
	#opening, reading, and closing a file in one (i think)
	origionalFileString = pathlib.Path(inputs['filePath']).read_text()
	#-------------------------------------------------

	#-------------------------------------------------
	#creates a list of every row in the file seperated by the given row delimiter
	listOfRows = re.findall(pattern=f".+?(?={inputs['rowDelim']}|$)", string=origionalFileString, flags=re.MULTILINE)
	
	#creates a 2d array where d1 is rows and d2 is item in row
	#finds the length of the longest row
	listOfRowsOfItems = []
	longestRowLength = 0
	for row in listOfRows:
		rowItems = re.findall(f"(?:(?<=^)|(?<={inputs['columnDelim']})).+?(?=(?:{inputs['columnDelim']}|$))",row)
		length = len(rowItems)
		if(length > longestRowLength): longestRowLength = length
		listOfRowsOfItems.append(rowItems)
	#-------------------------------------------------

	#-------------------------------------------------
	#finds the length of the longest item in each column
	columnLengths = [0]*longestRowLength

	for row in listOfRowsOfItems:
		for item in row:
			if len(row) == 1 : break
			length = len(item)
			index = row.index(item)
			if(length > columnLengths[index]): columnLengths[index] = length
	#-------------------------------------------------

	#-------------------------------------------------
	# create content of new file
	newFileString = ""
	for row in listOfRowsOfItems:
		length = len(row)
		if length == 1: newFileString += f"\n{row[0]}"
		else: 
			for item in row:
				newFileString += item
				if row.index(item)+1 == length: break
				spacingLength = columnLengths[row.index(item)] - len(item)
				for _ in range(spacingLength): newFileString = f"{newFileString}{inputs['spacerChar']}"
		newFileString += "\n"
	#-------------------------------------------------

	#-------------------------------------------------
	#create new file
	num = 0
	newPath = f"{inputs['filePath']}.niceprint.txt"
	while (os.path.exists(newPath)):
		num += 1
		newPath = f"{inputs['filePath']}.niceprint({num}).txt"
	pathlib.Path(newPath).write_text(newFileString)
	#-------------------------------------------------

	changeSubmitStatus("active",f"File Created with path {newPath}")


### ASSEMBLE

Interface = tkinter.Tk()
Interface.title("NicePrintDSV")

createLableRow("This program takes a delimiter seperated value file and will create a copy of it that is nicely formatted for printing pourposes.")

columnFrame = createLimitedEntryRow("columnDelim","Delimiter between columns of data:",2)
tkinter.Label(columnFrame, text=" (\\t unless given)").pack(side="left")

rowFrame = createLimitedEntryRow("rowDelim","Delimiter between rows of data:",2)
tkinter.Label(rowFrame, text=" (\\n unless given)").pack(side="left")

spacerFrame = createLimitedEntryRow("spacerChar","Seperate columns with character",3) 
tkinter.Label(spacerFrame, text=" (· unless given)").pack(side="left")

createLimitedEntryRow("pageDelim","Delimiter for fitting more data per page:",3)

#needs work
createEntryRow("filePath","Enter File Path:")
submitItems = createSubmitRow()
submitButton = submitItems[0]
statusMessage = submitItems[1]

#has to go at the end
Interface.geometry(f"{HorizontalSize}x{VerticalFrames*25}") # widthxheight+x+y
Interface.mainloop()
