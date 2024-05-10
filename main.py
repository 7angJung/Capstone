#!/usr/bin/env python
# coding: utf-8

# In[33]:


get_ipython().system('jupyter nbconvert --to script functions.ipynb')
get_ipython().system('pip install nbimporter')


# In[10]:


import nbimporter
from functions import detect_objects, crop_book, text_detection

img_path = "C:\\Users\\peter\\capstone\\camera\\test5.jpg"

crop_book(img_path)

img_left = "C:\\Users\\peter\\capstone\\onePage\\left_half.jpg"
img_right = "C:\\Users\\peter\\capstone\\onePage\\right_half.jpg"

recognized_texts = text_detection(img_left, img_right)

print(recognized_texts)


# In[ ]:




