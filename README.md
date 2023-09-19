# Keypoint Labelling Tool
  
**Run**

    python main.py


**Save Data**
    [x, y, v] Keypoint labeling data
    x, y is coordinate in image space / v is whether the keypoint is visible in image space

    {
      "Keypoint": [
        {
          "R_x": "90.0",
          "R_y": "109.0",
          "R_v": "1",
          "L_x": "139.0",
          "L_y": "58.0",
          "L_v": "0"
        }, 
        .
        .
        .
      ],
      "Render_On_Off": [
        {
          "R": 1,
          "L": 0
        }
      ]
    }


**Key Event**

    **[**: Index num down
    **]**: Index num up
    **Mouse Left**: Ceate Oval (Keypoint Visible)
    **Mouse Right**: Ceate Oval (Keypoint nonVisible)
    **Mouse Middle / Ctrl + z**: Undo Oval (Apply previous keypoint value)


**Button Event**

    **Save**: Save Label Data as Json
    **Right / Left**: Corresponding foot for labeling
    **Vis_On / Vis_Off**: Whether the foot is displayed in the image