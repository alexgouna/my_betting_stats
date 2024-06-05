from tkinter import *

root = Tk()
root.title("Main!!!")
root.geometry("400x270")

# Create main frames
frame_top = Frame(root, background="blue")
frame_center = Frame(root, background="yellow")
frame_bottom = Frame(root, background="red")

# Pack the main frames
frame_top.pack(side=TOP, fill=BOTH, expand=True)
frame_center.pack(side=TOP, fill=BOTH, expand=True)
frame_bottom.pack(side=TOP, fill=BOTH, expand=True)

# Create center left and right frames inside the center frame
frame_center_left = Frame(frame_center, background="black")
frame_center_right = Frame(frame_center, background="green")

# Pack center left and right frames
frame_center_left.pack(side=LEFT, fill=BOTH, expand=True)
frame_center_right.pack(side=RIGHT, fill=BOTH, expand=True)

# Add label to the center left frame





mainloop()
