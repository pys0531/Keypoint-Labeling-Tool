import tkinter as tk
from PIL import ImageTk, Image
import math

class tkint():
    def __init__(self,):
        self.app = tk.Tk()
        self.app.title('Keypoint Label Tool')
        self.app_size = [1500, 400]
        self.app.resizable(width=0, height=0) # Don't allow resizing in the x or y direction
        self.app.geometry(f'{self.app_size[0]}x{self.app_size[1]}')

        self.square_canvas_size = 400
        self.square_canvas_center = self.square_canvas_size/2
        self.canvas=tk.Canvas(self.app, width = self.square_canvas_size, height = self.square_canvas_size)

        self.button_size = [15, 7]
        self.button_frame = tk.Frame(self.app, width = 400, height = 400)
        self.button_frame.place(x = 450, y = 150)

        self.str_size = [30, 1]
        self.str_frame = tk.Frame(self.app)
        self.str_frame.place(x = 800, y = 20)
            
        self.Create_Foot_Label()
        self.Create_Vis_Label()
        self.Create_Keypoint_Label()

        self.idx_name = ["Back_Bottom", "Index_Toe", "Back_Top", "Front_Outside", "Front_Inside", "Back_Outside", "Back_Inside", "Middle_Top",
                         "Ankle_Outside", "Ankle_Inside", "Big_Toe", "Middle_Toe", "Fourth_Toe", "Little_Toe"]

        #self.canvas.bind("<MouseWheel>", self.Callback_Zoom_Up)
        #self.canvas.bind("<Button-5>", self.Callback_Zoom_Down)
        #self.zoom_scale = 1.2
        #self.app.geometry(str(self.width)+'x'+str(self.height))
        
        self.Num_Text = None

        
    def Create_Foot_Label(self):
        self.R_Foot_label = tk.Label(self.str_frame, text="Right", fg = "black", width = self.str_size[0], height = self.str_size[1], font=('Helvetica 9 bold'))
        self.R_Foot_label.grid(row=0, column=1)
        self.L_Foot_label = tk.Label(self.str_frame, text="Left", fg = "black", width = self.str_size[0], height = self.str_size[1], font=('Helvetica 9 bold'))
        self.L_Foot_label.grid(row=0, column=2)


    def Create_Vis_Label(self):        
        self.Vis_Name_label = tk.Label(self.str_frame, text="Render_Vis", fg = "black", width = self.str_size[0], height = self.str_size[1])
        self.Vis_Name_label.grid(row=1, column=0)

        self.R_vis_label = tk.Label(self.str_frame, text="None", fg = "black", width = self.str_size[0], height = self.str_size[1])
        self.R_vis_label.grid(row=1, column=1)

        self.L_vis_label = tk.Label(self.str_frame, text="None", fg = "black", width = self.str_size[0], height = self.str_size[1])
        self.L_vis_label.grid(row=1, column=2)        


    def Create_Keypoint_Label(self):
        self.L_keypoint_label = []
        self.R_keypoint_label = []
        self.Name_label = []


    def Create_Save_Button(self, text = "None", command = None):
        self.save_button = tk.Button(self.button_frame, text=text, command = command, width=self.button_size[0], height=self.button_size[1])
        self.save_button.grid(row=0, column=0)

    def Create_Shoes_Toggle_Button(self, text = "None", command = None):
        self.shoes_toggle_button = tk.Button(self.button_frame, text=text, command = command, width=self.button_size[0], height=self.button_size[1])
        self.shoes_toggle_button.grid(row=0, column=1)
        
    def Create_Shoes_Vis_Toggle_Button(self, text = "None", command = None):
        self.shoes_vis_toggle_button = tk.Button(self.button_frame, text=text, command = command, width=self.button_size[0], height=self.button_size[1])
        self.shoes_vis_toggle_button.grid(row=0, column=2)
        
    def Set_Label(self, num_joints, init_value):
        for i in range(num_joints):
            Name_label = tk.Label(self.str_frame, text=str(i)+": "+self.idx_name[i], fg = "#000", width = self.str_size[0], height = self.str_size[1])
            Name_label.grid(row=i+2, column=0)

            R_keypoint_label = tk.Label(self.str_frame, text=str(init_value), fg = "red", width = self.str_size[0], height = self.str_size[1])
            R_keypoint_label.grid(row=i+2, column=1)
            self.R_keypoint_label.append(R_keypoint_label)
            
            L_keypoint_label = tk.Label(self.str_frame, text=str(init_value), fg = "red", width = self.str_size[0], height = self.str_size[1])
            L_keypoint_label.grid(row=i+2, column=2)
            self.L_keypoint_label.append(L_keypoint_label)


            
    def Create_Image(self, img):
        self.img_orig_width = img.width
        self.img_orig_height = img.height
        max_l = max(self.img_orig_width/self.square_canvas_size, self.img_orig_height/self.square_canvas_size)
        self.scale = 1.0
        if max_l > 1.0:
            self.scale = math.ceil(max_l)
            resize_xy = (int(self.img_orig_width/self.scale), int(self.img_orig_height/self.scale))
            img = img.resize(resize_xy)


        self.photo = ImageTk.PhotoImage(img)
        self.img_width = img.width
        self.img_height = img.height
        self.canvas.place(x = (self.square_canvas_center - self.img_width/2.), y = (self.square_canvas_center - self.img_height/2.), width = self.img_width, height = self.img_height)
        self.canvas.create_image(0, 0, image = self.photo, anchor = 'nw')

        self.Create_Num_Text(self.img_width, self.img_height)

    def Create_Num_Text(self, img_width, img_height):
        self.Num_Text = self.canvas.create_text(img_width-35, 10, text= "Idx = 0",fill="green",font=('Helvetica 15 bold'))
        
    def Callback_Zoom_Up(self, event):
        if event.x > self.img_width or event.y > self.img_height:
            return
        
        img = Image.open(self.img_path)
        width = self.img_width / 1.2
        height = self.img_height / 1.2
        
        if event.x - width/2 < 0:
            start_x = 0
        elif event.x + width/2 > self.img_width:
            start_x = self.img_width - width
        else:
            start_x = event.x - width/2

        if event.y - height/2 < 0:
            start_y = 0
        elif event.y - height/2 < self.img_height:
            start_y = self.img_height - height
        else:
            start_y = event.y - height/2

        print("width, height: " , width, height)
        print("start_x, start_y: " , start_x, start_y)
        img = img.crop((start_x, start_y, width, height))
        #img = img.resize((self.img_width, self.img_height))
        self.photo = ImageTk.PhotoImage(img)
        self.canvas.configure(width = self.img_width, height = self.img_height)
        self.img = self.canvas.create_image(self.img_width/2, 0, image = self.photo, anchor = "n")

        #self.photo.resize((int(self.img_width * self.zoom_scale), int(self.img_height * self.zoom_scale)))
        #self.photo.zoom(1.2,1.2)
        #x = self.canvas.canvasx(event.x)
        #y = self.canvas.canvasy(event.y)
        #factor = 1.001 ** event.delta
        #is_shift = event.state & (1 << 0) != 0
        #is_ctrl = event.state & (1 << 2) != 0
        #self.canvas.scale(tk.ALL, x, y, 
        #             factor if not is_shift else 1.0, 
        #             factor if not is_ctrl else 1.0)

    def Callback_Zoom_Down(self, event):
        pass
        #self.canvas.resize((int(self.img_width / self.zoom_scale), int(self.img_height / self.zoom_scale)))
        #x = self.canvas.canvasx(event.x)
        #y = self.canvas.canvasy(event.y)
        #factor = 1.001 ** event.delta
        #is_shift = event.state & (1 << 0) != 0
        #is_ctrl = event.state & (1 << 2) != 0
        #self.canvas.scale(tk.ALL, x, y, 
        #             factor if not is_shift else 1.0, 
        #             factor if not is_ctrl else 1.0)


    def loop(self):
        self.app.mainloop()

