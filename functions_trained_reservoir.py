# -*- coding: utf-8 -*-
"""
Created on Tue May  3 17:35:28 2022

@author: smoot
"""

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.animation as animation

import mat73

from scipy import sparse, signal

from reservoirpy.mat_gen import normal

from random import gauss

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
    
#return une liste [x,y] avec les coordonées du chiffre n
def coord_target(n):
    transcription = extract_target()
    return np.concatenate((transcription[n][:,[0]],transcription[n][:,[1]]),axis = 1)
  
#Fonction qui return la data d'entrée voulu
#indS : indice du Sujet (de 1 à 5)
#indU : indide de l'entrée (de 1 à 10)
#indD : indide du chiffre (de 0 à 9)
def cocleogram(S,U,D,data):
    
    subject = 'subject_'+str(int(S))
    utterance = 'utterance_'+str(int(U))
    digit = 'digit_'+str(int(D))
    
    return data[subject][utterance][digit]


#Fonction qui affiche les chiffres d'arrivée 
def affiche_chiffre(n): 
    transcription = extract_target()
    limit = max(np.max(transcription[n]),abs(np.min(transcription[n])))
    fig, ax = plt.subplots()
    ax.plot(coord_target(n)[0],coord_target(n)[1])
    plt.xlim(-limit,limit)
    plt.ylim(-limit,limit)

    
#Fonction qui affiche un cocleogram 
def affiche_cocleo(indS,indU,indD,data,formatage = True):
    
    fig_cocleo,ax_cocleo = plt.subplots() 
    freq = 6*10**3
    T = 1/freq
    
    if formatage == True:
        cocleo = formatage_cocleogram(indS, indU, indD,data)      
    else :
        cocleo = cocleogram(indS,indU,indD,data)
   
    ax_cocleo.set_title("Cocleogram du sujet : {}, entrée : {},chiffre : {} et formaté :{}".format(indS,indU,indD,formatage))
    ax_cocleo.set_xlabel("Timestep")
    ax_cocleo.set_ylabel("Bande de fréquence")
    
    
    ax_cocleo.pcolormesh(cocleo,cmap="jet")
    
    fig_cocleo.show()
    
#formatage des entrées pour faire comme dans l'article
def formatage_cocleogram(indS,indU,indD,data,ampl_ent = 5,T_ent =1/(6*10**3), T_out = 1/(10**3) ):
    
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
    y = len(coord_target(indD))
    return ampl_ent * np.concatenate((cocleo,np.zeros([12,int(y)])),axis=1)


#création de la donnée de sortie z (une fonction en escalier) et formatage de x et y
#Ici pas sur que le pas de temps d'arriver soit à T_out et pas à T_ent mais sinon la durée est la même entre l'entrée et à la sortie.
def target_xyz(indS,indU,indD,data,T_ent =1/(6*10**3), T_out = 1/(10**3)):
    
    #Récupération du cocleogram
    cocleo = cocleogram(indS, indU, indD,data)
    
    bef_sensor = 100e-3 /T_ent
    duree_sensor_epoch = len(cocleo[0])
    duree_transition = 300*10**(-3)
    step_motor_epoch = len(coord_target(indD))  
    
    before_sensor_epoch= np.zeros([int(bef_sensor),1])
    
    sensor_transition_epoch = np.zeros([int(duree_sensor_epoch + (duree_transition)/T_out),1])
    
    z = np.concatenate((before_sensor_epoch,sensor_transition_epoch,np.ones([step_motor_epoch,1])),axis = 0)
    
    x = np.concatenate((before_sensor_epoch,sensor_transition_epoch,coord_target(indD)[:,[0]]))
    
    y = np.concatenate((before_sensor_epoch,sensor_transition_epoch,coord_target(indD)[:,[1]]))
    
    return np.concatenate((x,y,z), axis = 1)


    
def out(xyz,indS,indU,indD):
    
    fig,ax = plt.subplots()
    
    max1 = np.max(np.abs(xyz[:,[0,1]]))
    max2 = np.max(np.abs(coord_target(indD)))
    
    limit = max(max1,max2) + 0.1
    
    for i in range(np.shape(xyz)[0]-1):
        if xyz[i,2] >= 0.5:
            ax.plot([xyz[i,0],xyz[i+1,0]],[xyz[i,1],xyz[i+1,1]],"k")
            
    
    ax.plot(coord_target(indD)[:,[0]],coord_target(indD)[:,[1]],"r--",label="Target")
   
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.legend()
    ax.set_title("Sortie du sujet {}, entrée {} et chiffre {}".format(indS,indU,indD))
    ax.set_xlabel("axe des x")
    ax.set_ylabel("axe des y")
    
    fig.show
    

#Affiche le cocleogram d'entrée, et la sortie
def affiche(xyz,indS,indU,indD,data,states = np.zeros(10),error = np.zeros(10),mode = None,**kwargs):
    
    
    end_sensor_epoch = len(cocleogram(indS,indU,indD,data)[0])
    
    fig = plt.figure(figsize = (14,9))
    fig.suptitle("Prédictions du sujet : {}, entrée : {},chiffre : {} avec une méthode {}".format(indS,indU,indD,mode))
    gs = fig.add_gridspec(2, 3)

    
    #Affichage du cocleogram
    ax_cocleo = fig.add_subplot(gs[0,0])
    cocleo = formatage_cocleogram(indS, indU, indD,data)
    ax_cocleo.pcolormesh(cocleo,cmap="jet")
    ax_cocleo.set_title("Cocleogram du sujet : {}, entrée : {},chiffre : {}".format(indS,indU,indD))
    ax_cocleo.set_xlabel("Timestep")
    ax_cocleo.set_ylabel("Bande de fréquence")
    
    #Affichage de la sortie
    ax_out = fig.add_subplot(gs[0, 1])
    max1 = np.max(np.abs(xyz[:,[0,1]]))
    max2 = np.max(np.abs(coord_target(indD)))
    
    limit = max(max1,max2) + 0.1
    
    for i in range(np.shape(xyz)[0]-1):
        color = "k"
        if xyz[i,2] >= 0.5:
            color = "k"
        else:
            color = "0.8"
        ax_out.plot([xyz[i,0],xyz[i+1,0]],[xyz[i,1],xyz[i+1,1]],color)
            
    
    ax_out.plot(coord_target(indD)[:,[0]],coord_target(indD)[:,[1]],"r--",label="Target")
   
    ax_out.set_xlim(-limit, limit)
    ax_out.set_ylim(-limit, limit)
    ax_out.legend()
    ax_out.set_title("Sortie du sujet {}, entrée {} et chiffre {}".format(indS,indU,indD))
    ax_out.set_xlabel("axe des x")
    ax_out.set_ylabel("axe des y")
    
    #Affiche des états des neurones
    ax_state = fig.add_subplot(gs[1,0:2])
    ax_state.plot(states)
    ax_state.plot([end_sensor_epoch,end_sensor_epoch],[-1,1],"--k")
    ax_state.fill_betweenx([-1,1],[0],[end_sensor_epoch],color="0.95")
    ax_state.text(int(end_sensor_epoch/2),-1,r"sensor epoch")
    ax_state.set_title("Etats des neurones")
    
    #Affiche de l'erreur commise (simple distance euclidienne)
    max_error = np.max(error)
    ax_error = fig.add_subplot(gs[0,2])
    ax_error.plot(error)
    ax_error.plot([end_sensor_epoch,end_sensor_epoch],[0,max_error],"--k")
    ax_error.fill_betweenx([0,max_error],[0],[end_sensor_epoch],color="0.95")
    ax_error.text(0,0,r"sensor epoch")
    ax_error.set_xlabel("Timesteps")
    ax_error.set_ylabel("Distance euclidienne")
    ax_error.set_title("Erreur commise")

    #Affiche des données utilisées
    ax_donnees = fig.add_subplot(gs[1,2])
    limit = len(kwargs.items())
    
    y = 0.1
    
    for cle,value in kwargs.items():
        ax_donnees.text(limit/2 - 1/2,y,str(cle) + "=" + str(value),size =20)
        y = y + 1
    ax_donnees.set_xlim(0, limit)
    ax_donnees.set_ylim(0, limit)
    ax_donnees.set_axis_off()   
    

    fig.show
    
    
#Fonctions qui affiche tout les chiffes pour une entrée et un sujet donné.
def affiche_chiffre(liste_chiffre,indS,indU,data,list_error = [], mode = None,**kwargs):
    
    fig,ax = plt.subplots(4,3,figsize=(16,10))
    fig.suptitle("Prédictions du sujet : {}, entrée : {} et de tout les chiffres avec une méthode {}".format(indS,indU,mode))
    
    
    indD = 0
    
    for row in [0,1,2,3]:
        for col in [0,1,2]:
            ax[row,col] = fig.add_subplot(ax[row,col])
            #Affichage de la sortie
            max1 = np.max(np.abs(liste_chiffre[indD][:,[0,1]]))
            max2 = np.max(np.abs(coord_target(indD)))
    
            limit = max(max1,max2) + 0.1
    
            for i in range(np.shape(liste_chiffre[indD])[0]-1):
                color = "k"
                if liste_chiffre[indD][i,2] >= 0.5:
                    color = "k"
                else : 
                    color = "0.8"
                ax[row,col].plot([liste_chiffre[indD][i,0],liste_chiffre[indD][i+1,0]],[liste_chiffre[indD][i,1],liste_chiffre[indD][i+1,1]],color)
            
            
    
            ax[row,col].plot(coord_target(indD)[:,[0]],coord_target(indD)[:,[1]],"r--",label="Target")
   
            ax[row,col].set_xlim(-limit, limit)
            ax[row,col].set_ylim(-limit, limit)
            ax[row,col].legend()
            ax[row,col].set_title("Chiffre {}".format(indD))
            ax[row,col].set_xlabel("axe des x")
            ax[row,col].set_ylabel("axe des y")
            
            indD = indD + 1
            
            
            if row == 3 and col == 0:
                break
    
    
    #Affiche des données utilisées
    limit = len(kwargs.items())
    
    y = 0.1
    
    for cle,value in kwargs.items():
        ax[3,2].text(limit/2 - 1/2,y,str(cle) + "=" + str(value),size =20)
        y = y + 1
    ax[3,2].set_xlim(0, limit)
    ax[3,2].set_ylim(0, limit)
    ax[3,2].set_axis_off()
    
    fig.show()
    
def etat(reservoir,indS,indU,indD,data,units_nb=20):
    
    X = np.transpose(formatage_cocleogram(indS, indU, indD,data))
    
    states = reservoir.run(X)
    
    return states[:,:units_nb]

def error(xyz,indS,indU,indD,data):
    
    #On utilise la distance euclidienne
    target = target_xyz(indS, indU, indD, data)
    
    taille = len(target)
    
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
        indS = indice_median_entrance[i][0]
        indU = indice_median_entrance[i][1]
        indD = indice_median_entrance[i][2]
        median_entrance_cocleogram.append(np.transpose(cocleogram(indS,indU,indD,data)))
    
    return median_entrance_cocleogram



#Déformation linéaire de l'innate trajectory
def linear_warping(indS,indU,indD,data,innate_trajectory,sujet=[1]):
    
    #Récupération du cocleogram
    cocleo = cocleogram(indS,indU,indD,data)
    
    #Récupération du Timestep du cocleogram pour que l'innate trajectory y soit adaptée
    T = np.shape(cocleo)[1]
    
    #Déformation linéaire
    warping_innate_trajectory = signal.resample(innate_trajectory,T,axis = 0)
    
    return warping_innate_trajectory
    
    
    
    

#Fonction qui anime la sortie. en cours 
def anim_out(xyz): 
    
    x = xyz[:,[0]]
    y = xyz[:,[1]]
    z = xyz[:,[2]]
    
    limit = max(np.abs(np.max(xyz[:,[0,1]])),np.abs(np.min(xyz[:,[0,1]])))
    
    fig1,ax = plt.subplots()
    ax.plot(x,y)
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    
    line, = ax.plot([], [])
    
    fig = plt.figure() # initialise la figure
    line, = plt.plot([], []) 
    plt.xlim(-limit, limit)
    plt.ylim(-limit, limit)
    
    def animate(i): 
        line.set_data(x[i], y[i])
        return line,
    
    ani = animation.FuncAnimation(fig, animate, frames=100, blit=True, interval=20, repeat=False)
    
    plt.show()
    


