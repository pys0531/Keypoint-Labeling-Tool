import os
import json
from PIL import Image
import numpy as np

from handler import handler
from data_storage import shoes_data

class ai_label_tool(handler):
    def __init__(self, tk, infer):
        super(ai_label_tool, self).__init__(tk = tk)
        
        self.vis_threshold = 0.3
        self.render_vis_threshold = 0.3
        ###############################################################################
        ## Tflite Idx Name #      
        self.tf_idx_name = ["Big_Toe", "Index_Toe", "Middle_Toe", "Fourth_Toe", "Little_Toe", "Front_Inside", "Front_Outside", "Back_Inside", "Back_Outside", "Back_Bottom",
                            "Middle_Top", "Ankle_Inside", "Ankle_Outside"]#, "Back_Top"]

        ###############################################################################
        self.infer = infer
        self.data_init()
        
    def data_init(self,):
        self.tk.canvas.delete('all')
        self.R_data = shoes_data(self.num_joints)
        self.L_data = shoes_data(self.num_joints)
        
        ###############################################################################
        ## Ai Compute Init
        self.img_name = self.file_list[self.img_num]
        self.inference(self.img_name)
        

        ###############################################################################

        
        
        ###############################################################################
        ## Configure
        self.L_data_init()
        self.ai_label_set()
        self.R_data_init()
        self.ai_label_set()
        self.idx_change(0)
        ###############################################################################

        
    def ai_label_set(self):
        for i in range(14):
            self.idx_change(i)
            self.create_oval(self.data.value[i][0], self.data.value[i][1], self.data.value[i][2])
        

    def inference(self, img_path):
        img = Image.open(os.path.join(self.img_path, img_path))
        
        landmarks, rendervis, renderOnOff = self.infer.run(img)
        landmarks = landmarks.reshape([2,-1,2])
        rendervis = rendervis.reshape([-1,2,1])
        
        width = img.width if img.width > img.height else img.height
        
        landmarks[0,:,:] = landmarks[0,:,:] / 224 * width
        landmarks[1,:,:] = landmarks[1,:,:] / 224 * width

        self.R_landmarks = np.concatenate((landmarks[1,:,:], rendervis[:,1]), 1)
        self.L_landmarks = np.concatenate((landmarks[0,:,:], rendervis[:,0]), 1)
        
        self.R_renderOnOff = renderOnOff[1]
        self.L_renderOnOff = renderOnOff[0]
        self.R_landmarks = self.joint_switch(self.R_landmarks).round(4).tolist()
        self.L_landmarks = self.joint_switch(self.L_landmarks).round(4).tolist()
        
        for i in range(self.num_joints):
            self.R_data.value[i] = self.R_landmarks[i] 
            self.L_data.value[i] = self.L_landmarks[i] 
        self.R_data.render_vis = 1 if self.R_renderOnOff > self.render_vis_threshold else 0
        self.L_data.render_vis = 1 if self.L_renderOnOff > self.render_vis_threshold else 0
        
        self.Create_Image(img)
        

    def joint_switch(self, src_joint):
        src_name = self.tf_idx_name
        dst_name = self.tk.idx_name
        src_joint_num = len(src_name)
        dst_joint_num = len(dst_name)

        new_joint = np.zeros(((dst_joint_num,) + src_joint.shape[1:]))
        for src_idx in range(len(src_name)):
            name = src_name[src_idx]
            if name in dst_name:
                dst_idx = dst_name.index(name)
                new_joint[dst_idx] = src_joint[src_idx]

        return new_joint
    
    
    def Callback_Oval_Visiual(self, event):
        x, y = event.x, event.y
        if not(0 <= x < self.tk.img_width and 0 <= y < self.tk.img_height):
            return
            
        self.label[self.current_idx]['text'] = str([x, y, 1])
        self.label[self.current_idx]['fg'] = self.data.line_color[self.current_idx]
        if self.data.value[self.current_idx]:
            self.tk.canvas.delete(self.data.circle[self.current_idx])

        self.save_state(x, y, 1)
        self.create_oval(x, y, 1)
        self.num_up()
        print(x, y, 1)

    def Callback_Oval_NonVisual(self, event):
        x, y = event.x, event.y
        if not(0 <= x < self.tk.img_width and 0 <= y < self.tk.img_height):
            return

        self.label[self.current_idx]['text'] = str([x, y, 0])
        self.label[self.current_idx]['fg'] = self.data.line_color[self.current_idx]
        if self.data.value[self.current_idx]:
            self.tk.canvas.delete(self.data.circle[self.current_idx])

        self.save_state(x, y, 0)
        self.create_oval(x, y, 0)
        self.num_up()  
        print(x, y, 0)
        

    def Callback_Undo(self, event):
        prev_idx, prev_data = self.data.pop()
        
        self.idx_change(prev_idx)
        self.tk.canvas.delete(self.data.circle[prev_idx])
        
        if prev_data == self.init_value:
            self.data.value[self.current_idx] = prev_data
            self.label[self.current_idx]['text'] = str(prev_data)
            self.label[self.current_idx]['fg'] = "red"
        else:
            self.data.value[self.current_idx] = prev_data
            self.create_oval(prev_data[0], prev_data[1], prev_data[2])
            self.label[self.current_idx]['text'] = str(prev_data)
            self.label[self.current_idx]['fg'] = self.data.line_color[self.current_idx]


    def data_save(self,):
        data_dic = {"Keypoint": [{"R_x": None, "R_y": None, "R_v": None, "L_x": None, "L_y": None, "L_v": None} for i in range(self.num_joints)],
                "Render_On_Off": [{"R: ": self.R_data.render_vis, "L": self.L_data.render_vis}]}
        for i, (R, L) in enumerate(zip(self.R_data.value.values(), self.L_data.value.values())):
            data_dic["Keypoint"][i]["R_x"] = str(R[0])
            data_dic["Keypoint"][i]["R_y"] = str(R[1])
            data_dic["Keypoint"][i]["R_v"] = str(R[2])
            data_dic["Keypoint"][i]["L_x"] = str(L[0])
            data_dic["Keypoint"][i]["L_y"] = str(L[1])
            data_dic["Keypoint"][i]["L_v"] = str(L[2])

        with open(os.path.join(self.annotation_path, self.img_name.split(".")[0]+".json"), 'w') as outfile:
            json.dump(data_dic, outfile)
            
            
    def save(self):
        self.data_save()
        self.img_num += 1
        self.data_init()
