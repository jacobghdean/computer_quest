# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 02:10:04 2021

@author: jacob
"""
import pickle

ls=["Name","Name","Name","Name","Name","Name","Name","Name","Name","Name"]
ls2=[0,0,0,0,0,0,0,0,0,0]

pickle.dump(ls,open("names.p","wb"))
pickle.dump(ls2,open("scores.p","wb"))