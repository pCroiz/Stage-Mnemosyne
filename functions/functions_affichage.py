# -*- coding: utf-8 -*-
"""
Created on Mon May 30 19:53:21 2022

@author: smoot
"""

import sys 
sys.path.append("C:\\Users\\smoot\\Desktop\\Stage Mnemosyne\\functions")
import functions_data as d
import functions_cocleogramme as c

import matplotlib.pyplot as plt 

import numpy as np
from numpy.linalg import eig

from random import randint


#Fonction qui affiche les chiffres d'arrivée 
def affiche_one_chiffre(n): 
    transcription = d.extract_target()
    limit = max(np.max(transcription[n]),abs(np.min(transcription[n]))) + 0.1
    fig, ax = plt.subplots()
    ax.plot(c.coord_target(n,transcription)[:,0],c.coord_target(n,transcription)[:,1])
    ax.set_xlabel("Coordonée x")
    ax.set_ylabel("Coordonée y")
    ax.set_title("Tracé du chiffre 9")
    plt.xlim(-limit,limit)
    plt.ylim(-limit,limit)
    
    
    
#Fonction qui affiche un cocleogram 
def affiche_cocleo(indS,indU,indD,data,transcription,biais = 0,formatage = True):
    
    fig_cocleo,ax_cocleo = plt.subplots(figsize =(10,10)) 
    
    freq = 6*10**3
    T = 1/freq
    
    if formatage == True:
        cocleo = c.entrance_cocleogram(indS, indU, indD,data,transcription,biais)      
    else :
        cocleo = c.cocleogram(indS,indU,indD,data)
   
    ax_cocleo.set_title("Cocléogramme du sujet : {}, entrée : {},chiffre : {}".format(indS,indU,indD))
    ax_cocleo.set_xlabel("Timestep")
    ax_cocleo.set_ylabel("Bande de fréquence en Hz")
    
    im = ax_cocleo.pcolormesh(cocleo, cmap="jet",)
    fig_cocleo.colorbar(im, ax=ax_cocleo)

    
    fig_cocleo.show()
    
    
#Affiche la sortie XYZ et le chiffre target  
def out(xyz,indS,indU,indD,transcription):
    
    fig,ax = plt.subplots()
    
    max1 = np.max(np.abs(xyz[:,[0,1]]))
    max2 = np.max(np.abs(c.coord_target(indD,transcription)))
    
    limit = max(max1,max2) + 0.1
    
    for i in range(np.shape(xyz)[0]-1):
        if xyz[i,2] >= 0.5:
            ax.plot([xyz[i,0],xyz[i+1,0]],[xyz[i,1],xyz[i+1,1]],"k")
            
    
    ax.plot(c.coord_target(indD,transcription)[:,[0]],c.coord_target(indD,transcription)[:,[1]],"r--",label="Target")
   
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.legend()
    ax.set_title("Sortie du sujet {}, entrée {} et chiffre {}".format(indS,indU,indD))
    ax.set_xlabel("axe des x")
    ax.set_ylabel("axe des y")
    
    fig.show
    

#Affiche le cocleogram d'entrée, et la sortie
def affiche(xyz,indS,indU,indD,data,transcription,biais = 0,states = [],erreur = [],mode = None,filename = False,**kwargs):
    
    
    end_sensor_epoch = len(c.cocleogram(indS,indU,indD,data)[0])
    
    fig = plt.figure(figsize = (14,9))
    fig.suptitle("Prédictions du sujet : {}, entrée : {},chiffre : {} avec une méthode {}".format(indS,indU,indD,mode))
    gs = fig.add_gridspec(2, 3)

    
    #Affichage du cocleogram
    ax_cocleo = fig.add_subplot(gs[0,0])
    cocleo = c.entrance_cocleogram(indS, indU, indD,data,transcription,biais)
    ax_cocleo.pcolormesh(cocleo,cmap="jet")
    ax_cocleo.set_title("Cocleogram du sujet : {}, entrée : {},chiffre : {}".format(indS,indU,indD))
    ax_cocleo.set_xlabel("Timestep")
    ax_cocleo.set_ylabel("Bande de fréquence")
    
    #Affichage de la sortie
    ax_out = fig.add_subplot(gs[0, 1])
    max1 = np.max(np.abs(xyz[:,[0,1]]))
    max2 = np.max(np.abs(c.coord_target(indD,transcription)))
    
    limit = max(max1,max2) + 0.1
    
    for i in range(np.shape(xyz)[0]-1):
        color = "k"
        if xyz[i,2] >= 0.5:
            color = "k"
        else:
            color = "0.8"
        ax_out.plot([xyz[i,0],xyz[i+1,0]],[xyz[i,1],xyz[i+1,1]],color)
            
    
    ax_out.plot(c.coord_target(indD,transcription)[:,[0]],c.coord_target(indD,transcription)[:,[1]],"r--",label="Target")
   
    ax_out.set_xlim(-limit, limit)
    ax_out.set_ylim(-limit, limit)
    ax_out.legend()
    ax_out.set_title("Sortie du sujet {}, entrée {} et chiffre {}".format(indS,indU,indD))
    ax_out.set_xlabel("axe des x")
    ax_out.set_ylabel("axe des y")
    
    #Affiche des états des neurones
    
    if len(states) != 0:
        ax_state = fig.add_subplot(gs[1,0:2])
        ax_state.plot(states)
        ax_state.plot([end_sensor_epoch,end_sensor_epoch],[-1,1],"--k")
        ax_state.fill_betweenx([-1,1],[0],[end_sensor_epoch],color="0.95")
        ax_state.text(int(end_sensor_epoch/2),-1,r"sensor epoch")
        ax_state.set_title("Etats des neurones")
    
    #Affiche de l'erreur commise (simple distance euclidienne)
    
    if len(erreur) != 0:
        max_error = np.max(erreur)
        ax_error = fig.add_subplot(gs[0,2])
        ax_error.plot(erreur)
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
    
    if filename != False:
        plt.close(fig)
        nom = filename+"/affichage d'un seul chiffre avec indS = " +str(indS)+", indU = " + str(indU) + ", indD = " + str(indD) + ".png"

        fig.savefig(nom)
    else:
        fig.show()
    
    
#Fonctions qui affiche tout les chiffes pour une entrée et un sujet donné.
def affiche_chiffre(liste_chiffre,indS,indU,data,transcription,list_error = [], mode = None,filename = False,**kwargs):
    
    fig,ax = plt.subplots(4,3,figsize=(16,10))
    fig.suptitle("Prédictions du sujet : {}, entrée : {} et de tout les chiffres avec une méthode {}".format(indS,indU,mode))
    
    
    indD = 0
    
    for row in [0,1,2,3]:
        for col in [0,1,2]:
            ax[row,col] = fig.add_subplot(ax[row,col])
            #Affichage de la sortie
            max1 = np.max(np.abs(liste_chiffre[indD][:,[0,1]]))
            max2 = np.max(np.abs(c.coord_target(indD,transcription)))
    
            limit = max(max1,max2) + 0.1
    
            for i in range(np.shape(liste_chiffre[indD])[0]-1):
                color = "k"
                if liste_chiffre[indD][i,2] >= 0.5:
                    color = "k"
                else : 
                    color = "0.8"
                ax[row,col].plot([liste_chiffre[indD][i,0],liste_chiffre[indD][i+1,0]],[liste_chiffre[indD][i,1],liste_chiffre[indD][i+1,1]],color)
            
            
    
            ax[row,col].plot(c.coord_target(indD,transcription)[:,[0]],c.coord_target(indD,transcription)[:,[1]],"r--",label="Target")
   
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
    
    if filename != False:
        plt.close(fig)
        nom = filename+"/affichage de tout les chiffres avec indS = " +str(indS)+", indU = " + str(indU)  + ".png"
        fig.savefig(nom)
        fig.savefig(nom)
    else:
        fig.show()
    
    
#graphe de toutes les valeurs propres    
def eigein_value(W1,name1,W2 = [],name2="",filename = False):
    
    #récupération des valeurs propres
    eigeinvalue_W1, _ = eig(W1)
    
    #Récupération du rayon spectrale
    rs_W1 = np.max(np.abs(eigeinvalue_W1))
    
    #Affichage:
    fig,ax_eigeinvalue = plt.subplots()
    fig.suptitle("Affichage des valeurs propres")

    
    #Affichage du graphique
    X1,Y1 = [],[]
    for i in range(len(eigeinvalue_W1)):
        X1.append(eigeinvalue_W1[i].real)
        Y1.append(eigeinvalue_W1[i].imag)
                
        
    ax_eigeinvalue.scatter(X1,Y1,c = 'r',label=name1 + " et rs = " +str(rs_W1))
    
    if W2 != []:
        eigeinvalue_W2, _ = eig(W2)
        rs_W2 = np.max(np.abs(eigeinvalue_W2))
        X2,Y2 = [],[]
        for i in range(len(eigeinvalue_W2)):
        
            X2.append(eigeinvalue_W2[i].real)
            Y2.append(eigeinvalue_W2[i].imag)

        ax_eigeinvalue.scatter(X2,Y2,c = 'k',label=name2 + " et rs = " +str(rs_W2))
    
    ax_eigeinvalue.set_xlabel("Partie réelle")
    ax_eigeinvalue.set_ylabel("Partie imaginaire")
    ax_eigeinvalue.grid()
    ax_eigeinvalue.legend()
    
    if filename != False:
        plt.close(fig)
        fig.savefig(filename+"/affichage des valeurs propres.png")
    else:
        fig.show()
    
def pre_post_affichage(N,pre_training,pre_training_target,post_training,filename = False):
    
    fig,ax = plt.subplots(figsize=(17,10),nrows = 3,ncols=2)
    
    for i in range(3):
        neuron = randint(1,N-1)
        ax[i,0].plot(pre_training[:,neuron],"b",label = "etat pre-training du neurone " + str(neuron))
        ax[i,0].plot(pre_training_target[:,neuron],'--r',label = "innate trajectories")
        ax[i,0].legend()
        
        ax[i,1].plot(post_training[:,neuron],"b",label = "etat après training du neurone " + str(neuron))
        ax[i,1].plot(pre_training_target[:,neuron],'--r',label = "innate trajectories")
        ax[i,1].legend()
        
    if filename != False:
        plt.close(fig)
        fig.savefig(filename+"/affichage des états avant et après training.png")
    else:
        fig.show()


"""
#permet de générer une figure du rapport de stage;
def fig(data):
    
    indS,indU,indD = 1,1,9
    end_sensor_epoch = len(cocleogram(indS,indU,indD,data)[0])
    cocleo = formatage_cocleogram(indS, indU, indD,data)
    end = len(formatage_cocleogram(indS, indU, indD,data)[0])

    fig = plt.figure(figsize = (14,7))
    fig.suptitle("Données d'entrées")
    gs = fig.add_gridspec(1,2)


    ax_cocleo = fig.add_subplot(gs[0,0])
    ax_cocleo.set_title("Cocleogram du sujet : {}, entrée : {},chiffre : {}".format(indS,indU,indD))
    ax_cocleo.set_xlabel("Timestep")
    ax_cocleo.set_ylabel("Bande de fréquence")
    im = ax_cocleo.pcolormesh(cocleo, cmap="jet",)
    fig.colorbar(im, ax=ax_cocleo)
    
    ax_out = fig.add_subplot(gs[0,1])
    target = target_xyz(indS, indU, indD, data)
    ax_out.plot(target[:,0],"g",label="Coordonées de x")
    ax_out.plot(target[:,1],"r",label="Coordonées de y")
    ax_out.plot(target[:,2],"--b",label="Coordonées de z")
    
    ax_out.plot([0,end_sensor_epoch],[-0.5,-0.5],"k")
    ax_out.text(-10,-0.6,"époque sensorielle")
    
    ax_out.plot([end_sensor_epoch,end_sensor_epoch + 300],[-0.7,-0.7],"k")
    ax_out.text(end_sensor_epoch,-0.8,"transition")
    
    ax_out.plot([end_sensor_epoch + 300,end],[-0.8,-0.8],"k")
    ax_out.text(end_sensor_epoch + 550,-0.9,"époque motrice")

   
    ax_out.legend()
    ax_out.set_title("Variation des différentes coordonées")
    ax_out.set_xlabel("Timesteps")
"""

