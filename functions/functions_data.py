# -*- coding: utf-8 -*-
"""
Created on Mon May 30 19:53:20 2022

@author: smoot
"""


import mat73

import numpy as np

import os

import pickle

my_dict = { 'Apple': 4, 'Banana': 2, 'Orange': 6, 'Grapes': 11}

with open("myDictionary.pkl", "wb") as tf:
    pickle.dump(my_dict,tf)


#Extraction des données d'arrivée
def extract_target():
    target_dict = mat73.loadmat('C:/Users/smoot/Desktop/Stage Mnemosyne/donnees/target.mat')

    OutTarget = target_dict['OutTarget']

    return OutTarget['transcription'] #Les coordonées de chaques chiffres 
    
def extract_data():
#Extraction des données de départ def extract_data():
    subject_1 = mat73.loadmat('C:/Users/smoot/Desktop/Stage Mnemosyne/donnees/subject_1.mat')
    subject_2 = mat73.loadmat('C:/Users/smoot/Desktop/Stage Mnemosyne/donnees/subject_2.mat')
    subject_3 = mat73.loadmat('C:/Users/smoot/Desktop/Stage Mnemosyne/donnees/subject_3.mat')
    subject_4 = mat73.loadmat('C:/Users/smoot/Desktop/Stage Mnemosyne/donnees/subject_4.mat')
    subject_5 = mat73.loadmat('C:/Users/smoot/Desktop/Stage Mnemosyne/donnees/subject_5.mat')
    
    data = {"subject_1":subject_1,"subject_2":subject_2,"subject_3":subject_3,"subject_4":subject_4,"subject_5":subject_5}
    
    return data

def save_seed(entrance_matrice,trained_matrice,**kwargs):
    
    seed = {"init":{},'train':{},'params':{}}
    
    name_matrice =["Win","W","Wout"]
    
    for i,j in zip(entrance_matrice,name_matrice):
        seed["init"][j] = i
    
    name_matrice = ["W_train","Wout_train"]
    
    for i,j in zip(trained_matrice,name_matrice):
        seed['train'][j] = i
        
    for cle,value in kwargs.items():
        seed['params'][cle] = value
           
    dirPath = r"experience"
    fichier = next(os.walk(dirPath))[2]
    
    if len(fichier) == 0:
        number = [0]
    else :
    
        number = []
    
        for i in fichier:
            i = i[4:]
            i = i[:-4]
        
            number.append(int(i))
        
    number_seed = max(number) + 1
    
    name = 'experience/seed'+str(number_seed)+".pkl"
    
    with open(name, "wb") as tf:
        pickle.dump(seed,tf)

    return name   
    
    
def load_dict(file_name):
    with open(file_name, "rb") as tf:
        seed = pickle.load(tf)

    return seed

    



    