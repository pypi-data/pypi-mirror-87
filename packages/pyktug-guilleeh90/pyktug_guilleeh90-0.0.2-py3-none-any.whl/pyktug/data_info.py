import io
import pandas as pd
import numpy as np
import bson
import heapq
import matplotlib.pyplot as plt
import cv2
from scipy.signal import argrelextrema
import os
import json, codecs
from json2html import *
import sys
from scipy import stats
from numpy.linalg import norm
import time
from scipy import optimize
from scipy.signal import savgol_filter
import inspect
import pyktug.data as data
import pyktug.joint_angles as angles
import pyktug.gait_analysis as gait
import pyktug.gait_speed as speed
import pyktug.tools as tools
import pyktug.phases_tug as phases
import pyktug.smart_chair as chair
import pyktug.dict_to_json as dict_to_json
import pyktug.html_generator as html_gen
import pyktug.plotting as plotting

#DICCIONARIOS PARA EL JSON
def directory(directory):
	dict_marcha={}
	dict_inc={}
	dict_tec={}
	dict_silla={}
	dict_paso={}
	# define the name of the directory to be created
	path = directory+"/data_info"
	path_marcha = directory+"/data_info/marcha"
	path_inc = directory+"/data_info/incorporacion"
	path_silla = directory+"/data_info/silla"
	path_paso = directory+"/data_info/paso"


	try:  
		os.mkdir(path)
	except:pass
	try:
		os.mkdir(path_marcha)
	except:pass
	try:
		os.mkdir(path_inc)
	except:pass
	try:
		os.mkdir(path_silla)
	except:pass
	try:
		os.mkdir(path_paso)
	except:pass
		
	save_fig=True
	save_data=True
	
	bson_list=data.make_bsonlist(directory)
	id_num=data.correct_TrackingId(bson_list)
	exec(inspect.getsource(data.joints)[15:])
	ktime=data.kinect_time(bson_list)
	
	list_ang_piernas=angles.angulo_pierna(HipRight_Z_arr,KneeRight_Z_arr,AnkleRight_Z_arr,HipRight_Y_arr,KneeRight_Y_arr,AnkleRight_Y_arr,HipLeft_Z_arr,
		KneeLeft_Z_arr,AnkleLeft_Z_arr,HipLeft_Y_arr,KneeLeft_Y_arr,AnkleLeft_Y_arr)
	list_ang_pizq=np.asarray(list_ang_piernas[0])
	list_ang_pdcha=np.asarray(list_ang_piernas[1])
	list_ang_piernas_tronco=angles.ang_pierna_tronco(KneeRight_Z_arr,HipRight_Z_arr,SpineBase_Z_arr,KneeRight_Y_arr,HipRight_Y_arr,SpineBase_Y_arr,
		KneeLeft_Y_arr,HipLeft_Y_arr,KneeLeft_Z_arr,HipLeft_Z_arr,SpineShoulder_Z_arr,SpineShoulder_Y_arr)
	list_ang_pizq_col=np.asarray(list_ang_piernas_tronco[0])
	list_ang_pdcha_col=np.asarray(list_ang_piernas_tronco[1])
	list_ang_tronco=angles.inclinacion_tronco(SpineShoulder_Z_arr,SpineBase_Z_arr,SpineShoulder_Y_arr,SpineBase_Y_arr)

	list_ang_brazos=angles.angulo_brazo(ShoulderRight_Z_arr,ElbowRight_Z_arr,ShoulderRight_Y_arr,ElbowRight_Y_arr,ShoulderLeft_Z_arr,ElbowLeft_Z_arr,
		ShoulderLeft_Y_arr,ElbowLeft_Y_arr,WristRight_Z_arr,WristLeft_Z_arr,WristRight_Y_arr,WristLeft_Y_arr)
	list_ang_bizq=np.asarray(list_ang_brazos[0])
	list_ang_bdcho=np.asarray(list_ang_brazos[1])
	
	frame_change=data.frame_change(SpineBase_Z,WristRight_Z,WristLeft_Z)
	frame_inc=data.frame_incorporacion(list_ang_pdcha,list_ang_pizq,list_ang_pdcha_col,list_ang_pizq_col,frame_change)
	frame_sentada=data.frame_sentada(list_ang_pdcha,list_ang_pizq,list_ang_pdcha_col,list_ang_pizq_col,frame_change)
	
	inc_plano=tools.inclinacion_plano(frame_inc, frame_change, Neck_Z, Neck_Y,SpineBase_Z,SpineBase_Y,SpineMid_Z,SpineMid_Y, dict_tec)
	
	
	speed.speed(SpineBase_Z, ktime, frame_inc, frame_change, directory,dict_marcha, plot=True, save_fig=save_fig)
	n_ciclos=gait.steps_info(KneeLeft_Z,KneeRight_Z,AnkleLeft_Z,AnkleRight_Z, frame_inc, frame_change, ktime,dict_marcha)
	'''
	if n_ciclos>7:
		steps=gait.steps_index2(AnkleLeft_Z,AnkleRight_Z, frame_inc, frame_change)
	else:
	'''
	steps=gait.steps_index(KneeLeft_Z,KneeRight_Z,list_ang_pdcha,list_ang_pizq, ktime, frame_change, frame_inc)
	
	steps_izq=steps[0]
	steps_dcha=steps[1]
	print(steps_izq)
	print(steps_dcha)
	if len(steps_izq)==0 or len(steps_dcha)==0:
		steps=gait.steps_index2(AnkleLeft_Z,AnkleRight_Z, frame_inc, frame_change)
		steps_izq=steps[0]
		steps_dcha=steps[1]
		print(steps_izq)
		print(steps_dcha)
	
	try:
		gait.InfoCads(HipLeft_X,HipLeft_Y,HipLeft_Z,HipRight_X,HipRight_Y,HipRight_Z, list_ang_tronco, ktime, steps_izq, steps_dcha, directory, save_fig=save_fig)
		gait.knee_angles_gait(frame_change, list_ang_pdcha,list_ang_pizq, ktime, steps_izq, steps_dcha, directory,dict_paso, save_fig=save_fig)
	except:pass
	
	frame_acomodo=data.Sentada(HipLeft_X,HipRight_X,SpineBase_Z_arr,AnkleLeft_Z,AnkleRight_Z, ktime, frame_change, frame_sentada)[3]
	frame_inc_begin=chair.chair_values(SpineShoulder_Y,ShoulderLeft_Y,ShoulderRight_Y,ktime, frame_inc, frame_change, inc_plano, directory,
		dict_silla, dict_inc, plot=False, save_fig=save_fig)
	try:
		phases.fases_prueba(SpineBase_Z_arr,list_ang_pdcha,list_ang_pizq,ktime,frame_acomodo,frame_sentada,frame_inc, frame_inc_begin,
			directory, save_fig=save_fig)
	except:pass
	
	try:
		plotting.knee_angles(ktime,list_ang_pizq, list_ang_pdcha, frame_inc, frame_change-15,directory, save_fig=save_fig, phase='marcha')
	except:pass
	try:
		plotting.knee_angles(ktime,list_ang_pizq, list_ang_pdcha, 0, frame_inc,directory, save_fig=save_fig, phase='inc')
	except:pass
	try:
		plotting.knee_angles(ktime,list_ang_pizq, list_ang_pdcha, frame_sentada, -1,directory, save_fig=save_fig, phase='sent')
	except:pass
	try:
		plotting.elbow_angles(ktime,list_ang_bizq, list_ang_bdcho, frame_inc, frame_change-15,directory, save_fig=save_fig, phase='marcha')
	except:pass
	try:
		plotting.spine_angles(ktime,list_ang_tronco, frame_inc, frame_change-15,directory, save_fig=save_fig, phase='marcha')
	except:pass
	try:
		plotting.spine_angles(ktime,list_ang_tronco, 0, frame_inc,directory, save_fig=save_fig, phase='inc')
	except:pass
	try:
		plotting.spine_legs_angles(ktime,list_ang_pizq_col, list_ang_pdcha_col, frame_inc, frame_change-15,directory, save_fig=save_fig, phase='marcha')
	except:pass
	try:
		plotting.spine_legs_angles(ktime,list_ang_pizq_col, list_ang_pdcha_col, 0, frame_inc,directory, save_fig=save_fig, phase='inc')
	except:pass
	try:
		plotting.elbow_movement(ktime,ElbowLeft_Z,ElbowRight_Z,SpineMid_Z, frame_inc,frame_change-30, dict_marcha,directory, save_fig=save_fig)
	except:pass
	try:
		plotting.chair_plot(frame_inc, frame_sentada,directory,save_fig=save_fig)
	except:pass
	
	if save_data==True:
		dict_to_json.SaveDictToJson(directory,dict_marcha,dict_inc,dict_tec,dict_silla,dict_paso)
		html_gen.HtmlGenerator(directory)

if __name__ == "__main__":
	a = sys.argv[1]
	start = time.time()
	directory(a)
	end = time.time()
	print("tiempo en ejecutarse ", round(end - start, 4), " segundos")
	'''
    try:
        start = time.time()
        directory(a)
        end = time.time()
        print("tiempo en ejecutarse ", round(end - start, 4), " segundos")
    except BaseException:
         f = open(a+'/data.html','w')
         message = """
         <html>
         <body>
         <h1>Error en el procesado de los datos</h1>
         <h2>Por favor, compruebe que los archivos de información que quiere
         analizar son correctos</h2>
         <h4> Compruebe en primer lugar la ruta de acceso y verifique que el contenido
         del vídeo es el adecuado</h4>
         </body>
         </html>"""
         f.write(message)
         f.close()
         print('Ha ocurrido un error durante el procesado de los datos')
         sys.ext_info()
	'''