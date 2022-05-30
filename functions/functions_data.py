# -*- coding: utf-8 -*-
"""
Created on Mon May 30 19:53:20 2022

@author: smoot
"""


import mat73

#Extraction des données d'arrivée
def extract_target():
    target_dict = mat73.loadmat('donnees/target.mat')

    OutTarget = target_dict['OutTarget']

    return OutTarget['transcription'] #Les coordonées de chaques chiffres 
    
def extract_data():
#Extraction des données de départ def extract_data():
    subject_1 = mat73.loadmat('donnees/subject_1.mat')
    subject_2 = mat73.loadmat('donnees/subject_2.mat')
    subject_3 = mat73.loadmat('donnees/subject_3.mat')
    subject_4 = mat73.loadmat('donnees/subject_4.mat')
    subject_5 = mat73.loadmat('donnees/subject_5.mat')
    
    data = {"subject_1":subject_1,"subject_2":subject_2,"subject_3":subject_3,"subject_4":subject_4,"subject_5":subject_5}
    
    return data