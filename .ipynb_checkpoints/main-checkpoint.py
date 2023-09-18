import sys
sys.path.insert(0, 'handler')

from tkint import tkint
#from label_tool import label_tool
from ai_label_tool import ai_label_tool
from inference import infer

from PIL import ImageTk


if __name__ == '__main__':    
    tk = tkint()
    
    ## you can only use labeling 
    # label_tool(tk)
    
    ## If you have .h5 model, you can create pseudo label
    infer = infer()    
    ai_label_tool(tk, infer)
    
    tk.loop()