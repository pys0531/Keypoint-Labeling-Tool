import tkinter as tk
from PIL import ImageTk, Image


class tkint():
    def __init__(self,):
        self.app = tk.Tk()
        self.total_width= 800
        self.total_height= 600
        self.pos_x = self.total_width/2
        self.pos_y = self.total_height/2

        self.canvas=tk.Canvas(self.app, width = self.total_width, height = self.total_height) # width= self.width, height= self.height, 
        self.canvas.pack(side='left', fill='both')
        
        self.button_frame = tk.Frame(self.app)
        self.button_frame.pack(side='left', fill='both')
        
        self.frame = tk.Frame(self.app)
        self.frame.pack(side='left', fill='both')
                
        self.label_frame = tk.Frame(self.frame)
        self.label_frame.pack(side='top', fill='both')
            
        self.Create_Foot_Side()
        self.Create_Vis_Label()
        self.Create_Label()

        self.idx_name = ["Back_Bottom", "Index_Toe", "Back_Top", "Front_Outside", "Front_Inside", "Back_Outside", "Back_Inside", "Middle_Top",
                         "Ankle_Outside", "Ankle_Inside", "Big_Toe", "Middle_Toe", "Fourth_Toe", "Little_Toe"]

        #self.canvas.bind("<MouseWheel>", self.Callback_Zoom_Up)
        #self.canvas.bind("<Button-5>", self.Callback_Zoom_Down)
        #self.zoom_scale = 1.2
        #self.app.geometry(str(self.width)+'x'+str(self.height))
        
        self.Num_Text = None


    def Create_Shoes_Toggle_Button(self, text = "None", side = "right", ipadx = 20, padx = 0, ipady = 30, pady = 0, command = None):
        self.shoes_toggle_button = tk.Button(self.button_frame, text=text, command = command, height = 1, width = 4)
        self.shoes_toggle_button.pack(side=side, ipadx=ipadx, ipady=ipady, padx=padx, pady=pady)

    def Create_Save_Button(self, text = "None", side = "right", ipadx = 20, padx = 0, ipady = 30, pady = 0, command = None):
        self.save_button = tk.Button(self.button_frame, text=text, command = command, height = 1, width = 4)
        self.save_button.pack(side=side, ipadx=ipadx, ipady=ipady, padx=padx, pady=pady)
        
    def Create_Shoes_Vis_Toggle_Button(self, text = "None", side = "right", ipadx = 20, padx = 0, ipady = 30, pady = 0, command = None):
        self.shoes_vis_toggle_button = tk.Button(self.button_frame, text=text, command = command, height = 1, width = 4)
        self.shoes_vis_toggle_button.pack(side=side, ipadx=ipadx, ipady=ipady, padx=padx, pady=pady)
        
    def Create_Foot_Side(self):
        label = tk.Label(self.label_frame)
        label.pack(side='top', fill='both')
        
        self.L_Foot_frame_text = tk.Frame(label)
        self.L_Foot_frame_text.pack(side='right', fill='both')
        self.L_Foot_label = tk.Label(self.L_Foot_frame_text, text="Left", fg = "black", width = 35, height = 1, font=('Helvetica 9 bold'))
        self.L_Foot_label.pack()
        
        self.R_Foot_frame_text = tk.Frame(label)
        self.R_Foot_frame_text.pack(side='right', fill='both')
        self.R_Foot_label = tk.Label(self.R_Foot_frame_text, text="Right", fg = "black", width = 35, height = 1, font=('Helvetica 9 bold'))
        self.R_Foot_label.pack()

    def Create_Vis_Label(self):        
        label = tk.Label(self.label_frame)
        label.pack(side='top', fill='both')
        
        self.L_vis_frame_text = tk.Frame(label)
        self.L_vis_frame_text.pack(side='right', fill='both')
        self.L_vis_label = tk.Label(self.L_vis_frame_text, text="None", fg = "black", width = 35, height = 1)
        self.L_vis_label.pack()
        
        self.R_vis_frame_text = tk.Frame(label)
        self.R_vis_frame_text.pack(side='right', fill='both')
        self.R_vis_label = tk.Label(self.R_vis_frame_text, text="None", fg = "black", width = 35, height = 1)
        self.R_vis_label.pack()

        self.Vis_Name_frame_text = tk.Frame(label)
        self.Vis_Name_frame_text.pack(side='right', fill='both')
        self.Vis_Name_label = tk.Label(self.Vis_Name_frame_text, text="Render_Vis", fg = "black", width = 35, height = 1)
        self.Vis_Name_label.pack(side='right', fill='both')
        

    def Create_Label(self):
        self.L_frame_text = tk.Frame(self.frame)
        self.L_frame_text.pack(side='right', fill='both')
        self.L_label = []
        
        self.R_frame_text = tk.Frame(self.frame)
        self.R_frame_text.pack(side='right', fill='both')
        self.R_label = []

        self.Name_frame_text = tk.Frame(self.frame)
        self.Name_frame_text.pack(side='right', fill='both')
        self.Name_label = []
        
    def Set_Label(self, num_joints, init_value):
        for i in range(num_joints):
            R_label = tk.Label(self.R_frame_text, text=str(init_value), fg = "red", width = 35, height = 1)
            R_label.pack()
            self.R_label.append(R_label)
            
            L_label = tk.Label(self.L_frame_text, text=str(init_value), fg = "red", width = 35, height = 1)
            L_label.pack()
            self.L_label.append(L_label)

            Name_label = tk.Label(self.Name_frame_text, text=str(i)+": "+self.idx_name[i], fg = "#000", width = 35, height = 1)
            Name_label.pack()
            
    def Create_Image(self, img):
        self.photo = ImageTk.PhotoImage(img)
        #self.canvas.config(width = 400, height = 200)
        self.img_width = img.width
        self.img_height = img.height
        self.canvas.configure(width = self.img_width, height = self.img_height)
        self.img = self.canvas.create_image(self.img_width/2, 0, image = self.photo, anchor = "n")

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

