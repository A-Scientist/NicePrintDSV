#scales an item to the the numbers of characters inside it (stringVar())
#yikes, i can't resize by character if i only know the size by
#ASK RANDY ABOUT THIS
def item_window_width(text,item):
	textLength = myFont.measure(text)
	print(item.winfo_width())
	print(textLength)

	if item.winfo_width()/8 < textLength:
		item.pack_forget()
		item.pack(side="left",fill="x",ipadx=textLength/2)
