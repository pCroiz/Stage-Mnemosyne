# -*- coding: utf-8 -*-
"""
Created on Tue May  3 17:35:28 2022

@author: smoot
"""

import numpy as np

from scipy import sparse, signal

from reservoirpy.mat_gen import normal

from random import gauss

from tqdm import tqdm

from reservoirpy.nodes import Reservoir


    
#return une liste [x,y] avec les coordonées du chiffre n
def coord_target(n,transcription):
    return np.concatenate((transcription[n][:,[0]],transcription[n][:,[1]]),axis = 1)
  
#Fonction qui return la data d'entrée voulu
#indS : indice du Sujet (de 1 à 5)
#indU : indide de l'entrée (de 1 à 10)
#indD : indide du chiffre (de 0 à 9)
def cocleogram(S,U,D,data,amplitude = True,ampl_ent = 5):
    
    subject = 'subject_'+str(int(S))
    utterance = 'utterance_'+str(int(U))
    digit = 'digit_'+str(int(D))
    
    if amplitude == False :
        return data[subject][utterance][digit]
    else:
        return ampl_ent*data[subject][utterance][digit]

  
#formatage des entrées pour faire comme dans l'article
#Devenu obsolète  
def formatage_cocleogram(indS,indU,indD,data,transcription,T_ent =1/(6*10**3), T_out = 1/(10**3) ):
    
    #Chaque test et entrainement commence 100ms avant la sensor epoch
    #bef_sensor = int(100e-3 /T_ent)
    
    #Récupération du cocleogram
    cocleo = cocleogram(indS,indU,indD,data)
    
    #Rajout de la période avant la sensor epoch
    #cocleo = np.concatenate((np.zeros([12,int(bef_sensor)]),cocleo),axis=1)
    
    #Dans l'article il y a un temps de l'attence qui est ajouté de 300ms
    betw_epoch = (300*10**(-3))/T_out
    cocleo = np.concatenate((cocleo,np.zeros([12,int(betw_epoch)])),axis=1)
    
    #Ensuite, en fonction du chiffre qu'on cherche à afficher on rajoute une durée
    #Qui correspond au temps que met le reservoir à tracer le chiffre
    y = len(coord_target(indD,transcription))
    return np.concatenate((cocleo,np.zeros([12,int(y)])),axis=1)


#création de la donnée de sortie z (une fonction en escalier) et formatage de x et y
#Ici pas sur que le pas de temps d'arriver soit à T_out et pas à T_ent mais sinon la durée est la même entre l'entrée et à la sortie.
def target_xyz(indS,indU,indD,data,transcription,innate = False,T_ent =1/(6*10**3), T_out = 1/(10**3)):
    
    #Récupération du cocleogram
    cocleo = cocleogram(indS, indU, indD,data)
    
    #Récupération du cocléogramme avec un temps maximum
    S,U,D = ind_max_entrance(indD,data)
    max_cocleo = cocleogram(S,U,D,data)
    
    #différence des deux cocléogrammes
    diff = int(abs(np.shape(max_cocleo)[1] - np.shape(cocleo)[1]))
    
    duree_sensor_epoch = len(cocleo[0])
    duree_transition = 300*10**(-3)
    step_motor_epoch = len(coord_target(indD,transcription))  
    
    duree_total = duree_sensor_epoch + (duree_transition)/T_out + step_motor_epoch
    
    sensor_transition_epoch = np.zeros([int(duree_sensor_epoch + (duree_transition)/T_out)+diff,1])
    
    if innate == True:
        x = np.zeros((int(duree_total),3))
    
        return x
    
    z = np.concatenate((sensor_transition_epoch,np.ones([step_motor_epoch,1])),axis = 0)
    
    x = np.concatenate((sensor_transition_epoch,coord_target(indD,transcription)[:,[0]]))
    
    y = np.concatenate((sensor_transition_epoch,coord_target(indD,transcription)[:,[1]]))
    
    return np.concatenate((x,y,z), axis = 1)

    
def etat(reservoir,indS,indU,indD,data,units_nb=20):
    
    X = np.transpose(entrance_cocleogram(indS, indU, indD,data))
    
    states = reservoir.run(X)
    
    return states[:,:units_nb]

def error(xyz,indS,indU,indD,data):
    
    #On utilise la distance euclidienne
    target = target_xyz(indS, indU, indD, data)
    
    taille = len(xyz)
    
    d_euclidienne = np.zeros((taille,1))
    
    for i in range(taille):
        d_euclidienne[i,0] = np.sqrt((xyz[i,0]-target[i,0])**2 + ((xyz[i,1]-target[i,1])**2))
    
    return d_euclidienne
        
    
def W_r(N,*args,**kwargs):
    
    g = 1.6 
    connectivity = 0.2 
    SD = g/np.sqrt(connectivity*N)
    
    W = normal(N,N,loc=0,scale = SD,connectivity = connectivity)
    
    W = W.toarray()
    for k in range(N):
        if W[k,k] != 0:
            W[k,k] = 0
    
    return sparse.csr_matrix(W)
    
    
def W_in(N,M):
    Win = np.zeros((M,N))
    intervalle = int(N/M)

    for k in range(M):
        for i in range(intervalle):
            Win[k,i+k*intervalle] = gauss(0,1)
        
    return np.transpose(Win)

#Fonction qui recherche l'entrée la plus longue
def ind_max_entrance(indD,data,sujet=[1,2,3,4,5]):
    taille = 0
    S,U,D = 0,0,indD

    for indU in range(1,11):
        for indS in sujet:
                
            shape = np.shape(cocleogram(indS, indU, D, data))[1]
                
            if shape > taille :
                taille = shape 
                S,U,D = indS,indU,indD
    return S,U,D

#Fonction qui retourne les cocléogrammes d'entrées
def entrance_cocleogram(indS,indU,indD,data,transcription):

    #définition des périodes d'entrées et de sorties
    T_ent =1/(6*10**3)
    T_out = 1/(10**3)
            
    #Récupération du cocleogramme
    cocleo = cocleogram(indS,indU,indD,data)
    
    #Récupération du cocléogramme avec un temps maximum
    S,U,D = ind_max_entrance(indD,data)
    max_cocleo = cocleogram(S,U,D,data)
    
    #différence des deux cocléogrammes
    diff = int(abs(np.shape(max_cocleo)[1] - np.shape(cocleo)[1]))

    
    #On rajoute le nombre de 0 équivalent à la différence avant la période de transition
    cocleo = np.concatenate((cocleo,np.zeros([12,int(diff)])),axis=1)
    
    #Dans l'article il y a un temps de l'attence qui est ajouté de 300ms
    betw_epoch = (300*10**(-3))/T_out
    cocleo = np.concatenate((cocleo,np.zeros([12,int(betw_epoch)])),axis=1)
    
    #Ensuite, en fonction du chiffre qu'on cherche à afficher on rajoute une durée
    #Qui correspond au temps que met le reservoir à tracer le chiffre
    y = len(coord_target(indD,transcription))
    return np.concatenate((cocleo,np.zeros([12,int(y)])),axis=1)        
                
                
#Fonction qui recherche l'indice du cocleogram avec la taille moyenne pour chaque chiffre
def ind_median_entrance(data,sujet=[1]):
    
    liste_indice_total = []
    for indD in range(10):
        
        total = 0
        nbr = 0
        liste = []
        liste_indice = []
        
        for indU in range(1,11):
            for indS in sujet :
            
                taille = np.shape(cocleogram(indS, indU, indD, data))[1]
                total = total + taille
                nbr = nbr + 1
                liste.append(taille)
                liste_indice.append([str(indS),str(indU),str(indD)])
    

        median = int(total/nbr)
        search = median
        indice = 0
    
        for i in range(len(liste)):
            if abs(median - liste[i]) <= search:
                search = median - liste[i]
                indice = i 
        
        
        liste_indice_total.append(liste_indice[indice])
    return liste_indice_total
            

#Fonction qui retourne le cocleogram de taille moyenne pour chaque chiffre et parmit les sujets choisis dans l'ordre de 0 à 9
def median_cocleogram(data,sujet=[1]):
    
    indice_median_entrance = ind_median_entrance(data,sujet)
    rows,cols = np.shape(indice_median_entrance)
    median_entrance_cocleogram = []
    
    for i in range(rows):
        indS = int(indice_median_entrance[i][0])
        indU = int(indice_median_entrance[i][1])
        indD = int(indice_median_entrance[i][2])
        median_entrance_cocleogram.append(np.transpose(entrance_cocleogram(indS,indU,indD,data)))
    
    return median_entrance_cocleogram



#Déformation linéaire de l'innate trajectory
def linear_warping(indS,indU,indD,data,innate_trajectory):
    
    #Récupération du cocleogram
    cocleo = entrance_cocleogram(indS,indU,indD,data)
    
    #Récupération du Timestep du cocleogram pour que l'innate trajectory y soit adaptée
    T = np.shape(cocleo)[1]
    
    #Déformation linéaire
    warping = signal.resample(innate_trajectory,T,axis = 0)
    
    #Certaines valeurs deviennent supérieur à 1 ou inférieur à -1, on les rabaisse alors à 0.9995 ou -0.9995
    warping[warping > 1] = 0.995
    warping[warping < -1] = -0.995
            
    
    return warping
    