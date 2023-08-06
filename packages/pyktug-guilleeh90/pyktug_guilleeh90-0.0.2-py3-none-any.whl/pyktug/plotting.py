import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from .utils import Smooth
from scipy.signal import savgol_filter

def knee_angles(ktime,list_ang_pizq, list_ang_pdcha, frame_init, frame_end, directory, save_fig=False, phase='marcha'):
	angizq=Smooth(pd.Series(list_ang_pizq[frame_init:frame_end]).interpolate(method='polynomial', order=2).tolist(),10)
	angdcha=Smooth(pd.Series(list_ang_pdcha[frame_init:frame_end]).interpolate(method='polynomial', order=2).tolist(),10)
	x=ktime[frame_init:frame_end]
	plt.figure(figsize=(16,5))
	plt.plot(x, angizq, label='rodilla_izq')
	plt.plot(x, angdcha, label='rodilla_dcha')
	plt.grid(True)
	plt.legend()
	plt.xlabel('tiempo /s')
	plt.ylabel('Angulo rodilla /deg')
	plt.title('Angulo de las rodillas')
	if save_fig==True:
		if phase=='marcha':
			plt.savefig(directory+'/data_info/marcha/knee_angles.png')
		if phase=='inc':
			plt.savefig(directory+'/data_info/incorporacion/knee_angles.png')
		if phase=='sent':
			plt.savefig(directory+'/data_info/silla/knee_angles.png')
	else:
		plt.show()
	plt.close()

def elbow_angles(ktime,list_ang_bizq, list_ang_bdcho, frame_init, frame_end,directory, save_fig=False, phase='marcha'):
	angizq=Smooth(pd.Series(list_ang_bizq[frame_init:frame_end]).interpolate(method='polynomial', order=2).tolist(),10)
	angdcho=Smooth(pd.Series(list_ang_bdcho[frame_init:frame_end]).interpolate(method='polynomial', order=2).tolist(),10)
	x=ktime[frame_init:frame_end]
	plt.figure(figsize=(16,5))
	plt.plot(x, angizq, label='codo_izq')
	plt.plot(x, angdcho, label='codo_dcho')
	plt.grid(True)
	plt.legend()
	plt.xlabel('tiempo /s')
	plt.ylabel('Angulo codo /deg')
	plt.title('Angulo de los codos')
	if save_fig==True:
		if phase=='marcha':
			plt.savefig(directory+'/data_info/marcha/shoulder_angles.png')
		if phase=='inc':
			plt.savefig(directory+'/data_info/incorporacion/shoulder_angles.png')
		if phase=='sent':
			plt.savefig(directory+'/data_info/silla/shoulder_angles.png')
	else:
		plt.show()
	plt.close()
	
def spine_angles(ktime,list_ang_tronco, frame_init, frame_end, directory,save_fig=False, phase='marcha'):
	ang=Smooth(pd.Series(list_ang_tronco[frame_init:frame_end]).interpolate(method='polynomial', order=2).tolist(),10)
	x=ktime[frame_init:frame_end]
	plt.figure(figsize=(16,5))
	plt.plot(x, ang)
	plt.grid(True)
	plt.xlabel('tiempo /s')
	plt.ylabel('Angulo columna /deg')
	plt.title('Angulo de la columna respecto a la vertical')
	if save_fig==True:
		if phase=='marcha':
			plt.savefig(directory+'/data_info/marcha/spine_angles.png')
		if phase=='inc':
			plt.savefig(directory+'/data_info/incorporacion/spine_angles.png')
		if phase=='sent':
			plt.savefig(directory+'/data_info/silla/spine_angles.png')
	else:
		plt.show()
	plt.close()
	
def spine_legs_angles(ktime,list_ang_pizq_col, list_ang_pdcha_col, frame_init, frame_end,directory, save_fig=False, phase='marcha'):
	angizq=Smooth(pd.Series(list_ang_pizq_col[frame_init:frame_end]).interpolate(method='polynomial', order=2).tolist(),10)
	angdcha=Smooth(pd.Series(list_ang_pdcha_col[frame_init:frame_end]).interpolate(method='polynomial', order=2).tolist(),10)
	x=ktime[frame_init:frame_end]
	plt.figure(figsize=(16,5))
	plt.plot(x, angizq, label='pierna_izq')
	plt.plot(x, angdcha, label='pierna_dcha')
	plt.grid(True)
	plt.legend()
	plt.xlabel('tiempo /s')
	plt.ylabel('Angulo columna-pierna /deg')
	plt.title('Angulo entre la columna y la pierna')
	if save_fig==True:
		if phase=='marcha':
			plt.savefig(directory+'/data_info/marcha/spine_legs_angles.png')
		if phase=='inc':
			plt.savefig(directory+'/data_info/incorporacion/spine_legs_angles.png')
		if phase=='sent':
			plt.savefig(directory+'/data_info/silla/spine_legs_angles.png')
	else:
		plt.show()
	plt.close()
	
def elbow_movement(ktime,ElbowLeft_Z,ElbowRight_Z,SpineMid_Z, frame_init,frame_end, dict_marcha,directory, save_fig=False):
	#elz=Smooth(pd.Series(ElbowLeft_Z[frame_init:frame_end]).interpolate(method='polynomial', order=2).tolist(),10)
	#erz=Smooth(pd.Series(ElbowRight_Z[frame_init:frame_end]).interpolate(method='polynomial', order=2).tolist(),10)
	#smz=Smooth(pd.Series(SpineMid_Z[frame_init:frame_end]).interpolate(method='polynomial', order=2).tolist(),10)
	elz=ElbowLeft_Z[frame_init:frame_end]
	erz=ElbowRight_Z[frame_init:frame_end]
	smz=SpineMid_Z[frame_init:frame_end]
	dif_izq=np.array(elz)-np.array(smz)
	dif_dcho=np.array(erz)-np.array(smz)
	
	dif_izq_abs=abs(dif_izq)
	dif_dcho_abs=abs(dif_dcho)
	
	dict_marcha['Distancia longitudinal media entre codo izquierdo y tronco  / m']=round(np.nanmean(dif_izq_abs),2)
	dict_marcha['Distancia longitudinal maxima entre codo izquierdo y tronco  / m']=round(np.nanmax(dif_izq_abs),2)
	dict_marcha['Distancia longitudinal media entre codo derecho y tronco  / m']=round(np.nanmean(dif_dcho_abs),2)
	dict_marcha['Distancia longitudinal maxima entre codo derecho y tronco  / m']=round(np.nanmax(dif_dcho_abs),2)
	
	plt.figure(figsize=(16,5))
	plt.plot(ktime[frame_init:frame_end],Smooth(dif_izq,6), label='brazo_izq')            
	plt.plot(ktime[frame_init:frame_end],Smooth(dif_dcho,6),label='brazo_dcho')
	plt.ylabel('Distancia entre codo y tronco / m')
	plt.xlabel('tiempo / s')
	plt.grid(True)
	plt.title('Movimiento oscilatorio de los brazos respecto al tronco')
	plt.legend()
	plt.axhline(y=0, color='black', linestyle='-')
	if save_fig==True:
		plt.savefig(directory+'/data_info/marcha/elbow_mov.png')
	else:
		plt.show()
	plt.close()
	
def chair_plot(frame_inc, frame_sentada,directory,save_fig=False):
	if os.path.exists(directory+'/weight.csv') is True:
		silla=pd.read_csv(directory+'/weight.csv')
		silla=silla[silla.columns[0]].tolist()
		silla=savgol_filter(silla,41,8)
		plt.figure(figsize=(16,5))
		plt.plot(silla)
		plt.xlabel('muestras')
		plt.ylabel('Peso /Kg')
		plt.grid(True)
		plt.title('Pesos silla')
		if save_fig==True:
			plt.savefig(directory+'/data_info/silla/chair_complet.png')
		else:
			plt.show()
		plt.close()
		
		ind=int(frame_inc*(8/3))+60
		plt.figure(figsize=(16,5))
		plt.plot(silla[0:ind])
		#plt.axvline(frame_inc_begin/30,color='k')
		plt.ylabel('Peso / Kg')
		plt.xlabel('n')
		plt.grid(True)
		plt.title('Silla Báscula')
		if save_fig==True:
			plt.savefig(directory+'/data_info/silla/chair_inc.png')
		else:
			plt.show()
		plt.close()
		
		ind=int(frame_sentada*(8/3))-60
		plt.figure(figsize=(16,5))
		x=(np.arange(silla[ind], len(silla[ind:]))+ind)/80
		plt.plot(silla[ind:])
		plt.ylabel('Peso / Kg')
		plt.xlabel('n')
		plt.grid(True)
		plt.title('Silla Báscula')
		if save_fig==True:
			plt.savefig(directory+'/data_info/silla/chair_sent.png')
		else:
			plt.show()
		plt.close()