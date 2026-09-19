'''
this module contains the faces for BMO
now it only has 3-4options, but it will surely be expanded in the future. 
1-idle face
2-happy face
3-listening face
4-talking face( v1 and v2) - for mouth movements.
'''
import tkinter as tk
from PIL import Image, ImageTk
import os


class BMOFace:

    def __init__(self):
        self.root = tk.Tk()

        # Remove normal Windows title bar
        self.root.overrideredirect(True)

        # Keep BMO above other windows
        self.root.attributes("-topmost", True)

        # Make white parts of the window transparent
        self.root.config(bg="white")
        self.root.wm_attributes("-transparentcolor", "white")

        # Size of BMO on screen
        self.width = 500
        self.height = 450

        self.root.geometry(
            f"{self.width}x{self.height}+100+100"
        )

        self.label = tk.Label(
            self.root,
            bg="white",
            borderwidth=0
        )

        self.label.pack()
        self.label.bind("<Button-1>", self.start_drag)
        self.label.bind("<B1-Motion>", self.drag)

        self.show_face("bmo-idle-face")

    def show_face(self, face_name):

        base_path = os.path.dirname(os.path.abspath(__file__))

        image_path = os.path.join(
            base_path,
            f"{face_name}.png"
        )

        image = Image.open(image_path)

        image.thumbnail(
            (self.width, self.height),
            Image.Resampling.LANCZOS
        )

        self.photo = ImageTk.PhotoImage(image)

        self.label.config(image=self.photo)

    def start_drag(self, event):
         self.x = event.x
         self.y = event.y

    def drag(self, event):
        new_x = self.root.winfo_x() + event.x - self.x
        new_y = self.root.winfo_y() + event.y - self.y

        self.root.geometry(
            f"+{new_x}+{new_y}"
        )

    def run(self):
        self.root.mainloop()


# bmo = BMOFace()
# bmo.run()

# ******
# NOTE- THIS IS TO TEST whether images showing BMO's emotions can be viewed on laptop screen or not. 
# uncomment last 2 lines and run it to check. dont forget to comment it out to mnake it work in main.py
