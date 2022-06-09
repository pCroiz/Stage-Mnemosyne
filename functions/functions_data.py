# -*- coding: utf-8 -*-
"""
Created on Mon May 30 19:53:20 2022

@author: smoot
"""


import mat73

import os

import pickle



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

def save_seed(entrance_matrice,trained_matrice,chemin ="experience",**kwargs):
    
    
    seed = {"init":{},'train':{},'params':{}}
    
    name_matrice =["Win","W","Wout"]
    
    for i,j in zip(entrance_matrice,name_matrice):
        seed["init"][j] = i
    
    name_matrice = ["W_train","Wout_train"]
    
    for i,j in zip(trained_matrice,name_matrice):
        seed['train'][j] = i
        
    for cle,value in kwargs.items():
        seed['params'][cle] = value
           
    #Récupération du numéro de la seed
    try :
            fichier = open(chemin + "/number_seed","r") ; fichier.close()
    except :
            crea_text_number_seed(chemin)
            
    
    with open(chemin+"/number_seed","r") as fich:
        all_seed = fich.readlines()
        
        if len(all_seed) == 0:
            all_seed.append(1)
            number_seed = 1
        else:
            for i in range(len(all_seed)):
                all_seed[i] = int(all_seed[i])
                
            number_seed = max(all_seed)+1
            all_seed.append(max(all_seed)+1)
            
        for i in range(len(all_seed)):
            all_seed[i] = str(all_seed[i]) +"\n"
            
    #Réecriture du fichier 
    with open(chemin + "/number_seed","w") as fich:
        fich.writelines(all_seed)
    
    #création d'un fichier vide
    if not os.path.exists(chemin+'/seed'+str(number_seed)):
        os.makedirs(chemin + '/seed'+str(number_seed))
    
    #Création du fichier seed et importation dedans 
    name = chemin + '/seed'+str(number_seed)+'/seed'+str(number_seed)+".pkl"
    with open(name, "wb") as tf:
        pickle.dump(seed,tf)
        
    #Création d'un fichier texte avec les paramètres dedans:
    with open(chemin+'/seed'+str(number_seed)+'/params.txt',"w") as fich:
        for cle,value in kwargs.items():
            fich.write(str(cle)+" = "+str(value)+"\n")

    print("Fichier sauvegardé")
    
    #return le nom ainsi que le nom du fichier
    return name,chemin+'/seed'+str(number_seed)   
    
    
def load_seed(file_name):
    with open(file_name, "rb") as tf:
        seed = pickle.load(tf)

    return seed

    
def crea_text_number_seed(chemin):
    with open(chemin+"/number_seed","w") as fich:
        None

    