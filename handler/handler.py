import os
import abc
import json
from PIL import ImageTk,Image
import numpy as np

from data_storage import shoes_data


class handler(object):
    def __init__(self, tk):
        __metaclass__ = abc.ABCMeta
        self.tk = tk
        self.num_joints = len(self.tk.idx_name)
        self.init_value = [None, None, None]

        ## Image Path Read
        path = "./data"
        self.img_path = os.path.join(path, "images")
        self.annotation_path = os.path.join(path, "annotations")
        if not os.path.exists(self.annotation_path):
            os.makedirs(self.annotation_path)

        self.file_list = os.listdir(self.img_path)
        self.img_num = 0
        

        ## Keyboard Event
        self.tk.app.bind("<[>", self.Callback_Num_Down)
        self.tk.app.bind("<]>", self.Callback_Num_Up)

        
        ## Mouse Event
        # Keypoint Vis / Create Oval
        self.tk.canvas.bind("<Button-1>", self.Callback_Oval_Visiual) # L
        # Undo Oval
        self.tk.app.bind("<Button-2>", self.Callback_Undo) # M
        self.tk.app.bind("<Control-z>", self.Callback_Undo) # M
        # Keypoint nonVis / Create Oval
        self.tk.canvas.bind("<Button-3>", self.Callback_Oval_NonVisual) # R

        
        ## Button Event
        self.tk.Create_Shoes_Vis_Toggle_Button(text="Vis_On", command = self.shoes_vis_toggle)
        self.tk.Create_Shoes_Toggle_Button(text="Right", command = self.shoes_toggle)
        self.tk.Create_Save_Button(text="Save", command = self.save)
        
        ## Label Create
        self.tk.Set_Label(self.num_joints, self.init_value)
        

    @abc.abstractmethod
    def data_init(self,):
        return
    
    @abc.abstractmethod
    def data_save(self,):
        return
    
    @abc.abstractmethod
    def Callback_Undo(self, event):
        return
        
    @abc.abstractmethod
    def Callback_Oval_Visiual(self, event):
        return
        
    @abc.abstractmethod
    def Callback_Oval_NonVisual(self, event):
        return
        
                
    def Create_Image(self, img): # img_path
        self.tk.Create_Image(img)
        
        
    def Callback_Num_Down(self, event):
        self.num_down()
    
            
    def Callback_Num_Up(self, event):
        self.num_up()
        
        
    def save_state(self, x, y, v):
        self.data.append(self.current_idx, self.data.value[self.current_idx])

        
    def create_oval(self, x, y, orig_x, orig_y, v, i = None, shoes_state = None):
        oval_scale = min(self.tk.img_width , self.tk.img_height)
        oval_width = oval_scale / 90
        
        self.data.circle[self.current_idx] = self.tk.canvas.create_oval( x-oval_width, y-oval_width, x+oval_width, y+oval_width, fill='white', outline = self.color )
        self.data.value[self.current_idx] = [orig_x, orig_y, v]

        
    def num_down(self,):
        if self.current_idx == 0:
            print("더이상 줄일수 없습니다.")
        else:
            self.idx_change(self.current_idx - 1)

        
    def num_up(self):
        if self.current_idx == self.num_joints - 1:
            print("더이상 늘릴수 없습니다.")
        else:
            self.idx_change(self.current_idx + 1)
        
    def idx_change(self, idx):
        self.current_idx = idx
        self.tk.canvas.itemconfig(self.tk.Num_Text, text = "Idx = " + str(idx))
        
        
    def R_data_init(self):
        self.shoes_state = "Right"
        self.data = self.R_data
        self.keypoint_label = self.tk.R_keypoint_label
        self.vis_label = self.tk.R_vis_label
        self.color = 'red'
        self.override_data()
        
    def L_data_init(self):
        self.shoes_state = "Left"
        self.data = self.L_data
        self.keypoint_label = self.tk.L_keypoint_label
        self.vis_label = self.tk.L_vis_label
        self.color = 'green'
        self.override_data()

    def override_data(self):
        for i in range(self.num_joints):
            self.keypoint_label[i]['text'] = str(self.data.value[i])
            if self.data.value[i] == self.init_value or self.data.value[i][2] < self.vis_threshold:
                self.keypoint_label[i]['fg'] = "red"
                self.data.line_color[i] = "red"
            else:
                self.keypoint_label[i]['fg'] = "black"
                self.data.line_color[i] = "black"
                
        self.vis_label['text'] = self.get_vis_state()
        self.tk.shoes_toggle_button.configure(text = self.shoes_state)
        self.tk.shoes_vis_toggle_button.configure(text = self.get_vis_state())
        self.idx_change(0)


    def shoes_toggle(self):
        if self.shoes_state == "Right":
            self.L_data_init()
        elif self.shoes_state == "Left":
            self.R_data_init()
            
    def shoes_vis_toggle(self):
        if self.data.render_vis == 1:
            self.data.render_vis = 0
        elif self.data.render_vis == 0:
            self.data.render_vis = 1
        
        self.vis_label['text'] = self.get_vis_state()
        self.tk.shoes_vis_toggle_button.configure(text = self.get_vis_state())

    def get_vis_state(self):
        return "Vis_On" if self.data.render_vis == 1 else "Vis_Off"