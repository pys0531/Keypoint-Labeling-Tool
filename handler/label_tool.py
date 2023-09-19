import os
import json
from PIL import Image

from handler import handler
from data_storage import shoes_data


class label_tool(handler):
    def __init__(self, tk):
        super(label_tool, self).__init__(tk = tk)

        self.vis_threshold = 0.0
        self.data_init()
        
    def data_init(self,):
        ## Data Create
        self.tk.canvas.delete('all')
        self.R_data = shoes_data(self.num_joints)
        self.L_data = shoes_data(self.num_joints)
        
        ## Data Init
        self.L_data_init()
        self.R_data_init()

        self.img_name = self.file_list[self.img_num]
        self.show_image(self.img_name)
        
    def show_image(self, img_path):
        img = Image.open(os.path.join(self.img_path, img_path))
        self.Create_Image(img)
        
        
    def Callback_Oval_Visiual(self, event):
        self.Callback_Oval_Common(event, 1)

    def Callback_Oval_NonVisual(self, event):
        self.Callback_Oval_Common(event, 0)


    def Callback_Oval_Common(self, event, v):
        x, y = event.x, event.y
        orig_x, orig_y = x * self.tk.scale, y * self.tk.scale

        if not(0 <= x < self.tk.img_width and 0 <= y < self.tk.img_height):
            return

        self.keypoint_label[self.current_idx]['text'] = str([orig_x, orig_y, v])
        self.keypoint_label[self.current_idx]['fg'] = 'black'
        if self.data.value[self.current_idx]:
            self.tk.canvas.delete(self.data.circle[self.current_idx])

        self.save_state(orig_x, orig_y, v)
        self.create_oval(x, y, orig_x, orig_y, v)
        self.num_up()  
        print(orig_x, orig_y, v)

    def Callback_Undo(self, event):
        prev_idx, prev_data = self.data.pop()

        self.idx_change(prev_idx)
        self.tk.canvas.delete(self.data.circle[prev_idx])

        if prev_data == self.init_value:
            self.data.value[self.current_idx] = prev_data
            self.keypoint_label[self.current_idx]['text'] = str(prev_data)
            self.keypoint_label[self.current_idx]['fg'] = "red"
        else:
            self.data.value[self.current_idx] = prev_data
            x, y, v = prev_data[0] / self.tk.scale, prev_data[1] / self.tk.scale, prev_data[2]
            orig_x, orig_y = prev_data[0], prev_data[1]
            self.create_oval(x, y, orig_x, orig_y, v)
            self.keypoint_label[self.current_idx]['text'] = str(prev_data)
            self.keypoint_label[self.current_idx]['fg'] = "black"
            



    def data_save(self,):
        data_dic = {"Keypoint": [{"R_x": None, "R_y": None, "R_v": None, "L_x": None, "L_y": None, "L_v": None} for i in range(self.num_joints)],
                "Render_On_Off": [{"R": self.R_data.render_vis, "L": self.L_data.render_vis}]}
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
