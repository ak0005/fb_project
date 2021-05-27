from tkinter import *
import webbrowser
from tkinter import messagebox

from utils import *


root = Tk()
root.title("GUI")


root.geometry("600x300")


def open_link():
	lst = link_var.get().split('_')
	if len(lst)<2:
		messagebox.showwarning("Warning", "Wrong Id of Post")
	else:
		group_id = lst[0]
		post_id = lst[1]
		webbrowser.get('firefox').open('https://facebook.com/groups/'+group_id+'/permalink/'+post_id)


attributes_options = [
	"reactions",
	"comment_sentiment",
]
order_options=[
	"Lowest to Highest",
	"Highest to Lowest"
]

# datatype of menu text
attributes_var = StringVar()
order_var=StringVar()
post_count_var=StringVar()
link_var=StringVar()
saved_label_var=StringVar()



# initial menu text
attributes_var.set( "        " )
order_var.set( "        " )


attr_label=Label(root,text="Choose a attribute for sorting the posts: ")

# Create Dropdown menu
attributes_dropdown = OptionMenu( root , attributes_var , *attributes_options )

order_label=Label(root,text="Select sort order based on above property: ")

order_dropdown=OptionMenu( root , order_var , *order_options )

count_label=Label(root,text="Enter count of top posts to be retrieved: ")


post_count_entry=Entry(root,textvariable = post_count_var, font=('calibre',10,'normal'))


saved_label=Label(root,text='')


def write_post_ids(df,post_count_str):

	if post_count_str.isnumeric():
		post_count=int(post_count_str)
		if post_count>0:
			with open('ids.txt','w') as fp:
				post_ids=list(df['postId'].iloc[0:post_count])
				fp.write('\n'.join(post_ids))
				saved_label.config(text=post_count_var.get()+' posts saved in ids.txt file')
				# saved_label.config(text=('\n'.join(post_ids)))

def callback(*args):
    # print(f"the variable has changed to '{attributes_var.get()}'")
	# print(type(attributes_var.get()))
	if attributes_var.get() in attributes_options:	
		if order_var.get()=='Lowest to Highest':
			df=Utils.sort_data(attributes_var.get(),False)
			write_post_ids(df,post_count_var.get())
		elif order_var.get()=='Highest to Lowest':
			df=Utils.sort_data(attributes_var.get(),True)
			write_post_ids(df,post_count_var.get())
	# print(df.iloc[1])
	# string=attributes_var.get()+' '+df.iloc[0]['postId']
	# label1.config(text=string)

attributes_var.trace("w",callback)
order_var.trace("w",callback)
post_count_var.trace("w",callback)


link_label=Label(root,text="Enter id of post that you would like to open in browser")


link_entry=Entry(root,textvariable = link_var, font=('calibre',10,'normal'))

open_button=Button(root,text="Open",command=open_link)



attr_label.grid(row=0,column=0)
attributes_dropdown.grid(row=0,column=1)

order_label.grid(row=2,column=0)
order_dropdown.grid(row=2,column=1)

count_label.grid(row=4,column=0)
post_count_entry.grid(row=4,column=1)

saved_label.grid(row=6,column=1)

link_label.grid(row=8,column=0)
link_entry.grid(row=8,column=1)
open_button.grid(row=8,column=2)


root.mainloop()
