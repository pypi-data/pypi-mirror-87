import pandas as pd
import numpy as np
from scipy.signal import savgol_filter
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
import os

def chair_values(SpineShoulder_Y,ShoulderLeft_Y,ShoulderRight_Y, ktime, frame_inc, frame_change, inc_plano, directory, dict_silla, dict_inc, plot=False, save_fig=False):
	if os.path.exists(directory+'/weight.csv') is True:
		silla=pd.read_csv(directory+'/weight.csv')
		silla=silla[silla.columns[0]].tolist()
		silla=savgol_filter(silla,41,8)

		
		def peso_silla(data):
			val=[]
			c=0
			for i in data:
				if i>10 and data[c+5]>10:
					val.append(i)
			counts = np.bincount(val)
			peso_medio=np.argmax(counts)
			if plot==True:
				plt.plot(np.arange(0,len(silla))/80, silla)
				plt.ylabel('Peso / Kg')
				plt.xlabel('tiempo / s')
				plt.grid(True)
				plt.title('Silla Báscula')
				if save_fig==True:
					plt.savefig(directory+'/data_info/silla/total.png')
				else:
					plt.show()
				plt.close()

			dict_silla['Peso / Kg']=int(peso_medio)
			
			return(peso_medio)
			
		peso=peso_silla(silla)
		
		frame_inc_begin=0
		def IncBegin(data):
			maxs=argrelextrema(data, np.greater)[0]
			maxs_fit=[]
			for i in maxs:
				if i<frame_inc*(8/3) and data[i]>20:
					maxs_fit.append(i)
			global frame_inc_begin
			frame_inc_begin=maxs_fit[-1]
			return(frame_inc_begin) 
		
		#global frame_inc_begin
		frame_inc_begin=IncBegin(silla)
		
		
		def Suavidad(lista):
			
			mins=argrelextrema(lista, np.less)[0]
			
			special_mins=[]
			for i in mins:
				if lista[i]<peso*0.6:
					special_mins.append(lista[i])
			mins_fit=[]
			for i in mins:
				if lista[i]<peso*0.9:
					mins_fit.append(lista[i])
		
			if len(special_mins)>0: #si hay algún mínimo especial, la suavidad se reduce a la mitad
				g=0.5
			else:
				g=1
				
			lista2=[]
			for i in mins_fit:
				lista2.append(peso-i)   # Damos mas peso a mayor amplitud del minimo
			if len(lista2)==0:
				s=1
			else:
				if len(lista2)>=11:
					s=0
				else:
					k=sum(lista2)/(peso*(len(lista2))) #Valor <1 proporcional a la amplitud de los minimos
					coef_range=np.linspace(1,1/k,10)
					s=1-k*coef_range[len(lista2)-1] #Suavidad rango [0,1]
			
			dict_inc['Suavidad (S)']=round(s*g,2)
			
		Suavidad(silla[0:frame_inc_begin])
		
		seg_change=ktime[frame_change]
		silla_frame_change=int(seg_change*80)
		
		def Percusion(data):
			p=1-(peso/max(data))
			
			dict_silla['Percusion (P)']=round(p,2)

		Percusion(silla[int(len(silla)/2):])
		
		def Fuerza(silla, frame_inc, peso):
			dist=[]
			a=[]
			b=[]
			c=[]
			for i in np.arange(frame_inc+30, frame_inc+45):
				a.append(SpineShoulder_Y[i])
				b.append(ShoulderRight_Y[i])
				c.append(ShoulderLeft_Y[i])
					
			a=np.nanmean(a)
			b=np.nanmean(b)
			c=np.nanmean(c)
			x=[]
			y=[]
			z=[]
			
			for i in np.arange(0, int(frame_inc_begin*(3/8))):
				x.append(SpineShoulder_Y[i])
				y.append(ShoulderRight_Y[i])
				z.append(ShoulderLeft_Y[i])
			x=np.nanmean(x)
			y=np.nanmean(y)
			z=np.nanmean(z)
			dist=[a-x,b-y,c-z]
		
			dist_med=np.mean(dist)+(np.mean(dist)*np.sin(np.deg2rad(inc_plano)))
			tiempo=(frame_inc/30 - frame_inc_begin/80)
			
			f=(peso*dist_med)/(tiempo*tiempo)
			
			dict_inc['Altura recorrida / m']=round(dist_med,2)
			dict_inc['Fuerza (F) / N']=round(f,2)
			dict_inc['Tiempo / s']=round(tiempo,2)
		
		Fuerza(silla, frame_inc, peso)
		
		def plot_silla_values(silla):
			plt.plot(np.arange(0,silla_frame_change)/80, silla[0:silla_frame_change])
			plt.axvline((frame_inc_begin/80),color='k')
			plt.ylabel('Peso / Kg')
			plt.xlabel('tiempo / s')
			plt.grid(True)
			plt.title('Silla Báscula')
			if save_fig==True:
				plt.savefig(directory+'/data_info/incorporacion/inc.png')
			else:
				plt.show()
			plt.close()
			
			ind=int(frame_sentada*(8/3))
			#print('ind',ind)
			#print(silla[ind:])
			
			#print(np.arange(silla[ind], len(silla[ind:])))
			
			
			#x=(np.arange(silla[ind], len(silla[ind:]))+ind)/80
			#x=(np.arange(len(silla[ind:]))+ind)/80
			#plt.plot(x,silla[ind:])
			
			x=(np.arange(len(silla[silla_frame_change:])))+silla_frame_change
			plt.plot(x/80,silla[silla_frame_change:])
			plt.ylabel('Peso / Kg')
			plt.xlabel('tiempo (aproximado)/ s')
			plt.grid(True)
			plt.title('Silla Báscula')
			if save_fig==True:
				plt.savefig(directory+'/data_info/silla/sent2.png')
			else:
				plt.show()
			plt.close()
		
		if plot==True:
			plot_silla_values(silla)

	else: 
		frame_inc_begin=0
		
	return(frame_inc_begin)