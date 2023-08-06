import cv2
import numpy as np
import pandas as pd
import bson
from .utils import frame_firstmax_lists
from .joint_angles import angulo_pierna, ang_pierna_tronco

def make_bsonlist(directory):
	#read video duration and frames.bson file which contains all information about the record
	v=cv2.VideoCapture(directory+'/video.mpeg')
	frameCount = int(v.get(cv2.CAP_PROP_FRAME_COUNT))

	bson_list=[]
	c=0
	bson_init = open(directory+'/frames.bson', 'rb')
	bson_r= bson_init.read()
	for i in np.arange(1,1+frameCount):
		bson_read = bson.decode_document(bson_r,c)
		bson_file=bson_read[1]
		c=bson_read[0]
		bson_list.append(bson_file)
	
	return(bson_list)
	

def kinect_time(bson_list):
	#generate a list with the time for each frame begins at t=0s
	real_time=[]
	ref_time=[]
	for i in range(len(bson_list)):
		l=bson_list[i]['RelativeTime'].split(':')
		#print('time',bson_list[i]['RelativeTime'])
		#print('time_split',l)
		real_time.append(float(l[2]))
		ref_time.append(float(l[1]))
	time=[] 
	real_time[0]=real_time[1]
	ref_time[0]=ref_time[1]
	c=0
	for i in real_time:
		time_dif=int(ref_time[c]-ref_time[0])
		time.append(i-real_time[0]+(60*time_dif))
		c+=1
	return(time)

def correct_TrackingId(bson_list):
	#identifies the correct person to evaluate if appears other people in the video.
	#This correct person is the first person that Kinect recognizes
	id_list=[]
	for bson_simple in bson_list:
		for i in bson_simple['BodiesEx']:
			if i['TrackingId']!=0:
				id_list.append(i['TrackingId'])
	return(list(set(id_list)))
    
	
def joints():
	for i in bson_list[7]['BodiesEx'][1]['Joints'].keys():
		for j in ['X','Y','Z']:
			globals()['{}_{}'.format(i,j)]=[]
			for k in bson_list:
				for m in k['BodiesEx']:
					if m['TrackingId']==id_num[0]:
						for joint in m['Joints'].keys():
							if joint==i:
								if m['Joints'][joint]['TrackingState']==2:
									globals()['{}_{}'.format(i,j)].append(m['Joints'][joint]['Position'][j])
								else:
									globals()['{}_{}'.format(i,j)].append(np.nan)
							else:pass
			globals()['{}_{}_arr'.format(i,j)]=np.asarray(globals()['{}_{}'.format(i,j)])
			
#def joints() must be executed as exec(inspect.getsource(data.joints)[15:]) 
#It generates lists and arrays with all positions for each joint. Ej: AnkleLeft_X, AnkleLeft_Y and AnkleLeft_Z
	
def frame_change(SpineBase_Z,WristRight_Z,WristLeft_Z): 
	#This is the frame in which the outward journey ends 
	for i in SpineBase_Z:
		ind=SpineBase_Z.index(i)
		if i<1:
			break
	if np.nanmin(WristRight_Z[:ind]) < np.nanmin(WristLeft_Z[:ind]):
		frame_change=(WristRight_Z.index(np.nanmin(WristRight_Z[:ind])))
	else:
		frame_change=(WristLeft_Z.index(np.nanmin(WristLeft_Z[:ind])))

	return(frame_change)		
	
def frame_incorporacion(list_ang_pdcha,list_ang_pizq,list_ang_pdcha_col,list_ang_pizq_col,frame_change):
	#This is the frame in which the rise ends 
	frame_inc1=frame_firstmax_lists(list_ang_pdcha[0:frame_change],list_ang_pizq[0:frame_change])
	frame_inc2=frame_firstmax_lists(list_ang_pdcha_col[0:frame_change],list_ang_pizq_col[0:frame_change])
	frame_inc=int((frame_inc1+frame_inc2)/2) #FRAME FINAL INCORPORACION
	return(frame_inc)

def frame_sentada(list_ang_pdcha,list_ang_pizq,list_ang_pdcha_col,list_ang_pizq_col,frame_change):
	#This is the frame in which the person begins to sit
	frame_sentada1=frame_firstmax_lists(list_ang_pdcha[:frame_change:-1],list_ang_pizq[:frame_change:-1])
	frame_sentada2=frame_firstmax_lists(list_ang_pdcha_col[:frame_change:-1],list_ang_pizq_col[:frame_change:-1])
	frame_sentada=len(list_ang_pdcha)-int((frame_sentada1+frame_sentada2)/2) #FRAME INICIO SENTADA
	return(frame_sentada)
	
def Sentada(HipLeft_X,HipRight_X,SpineBase_Z_arr,AnkleLeft_Z,AnkleRight_Z, ktime, frame_change, frame_sentada):
	#identifies the phase in which the person begins the turn to sit on the return
	data={'cad_izq':HipLeft_X[frame_change+30:frame_sentada],
		 'cad_dcha':HipRight_X[frame_change+30:frame_sentada]}
	df_cad=pd.DataFrame(data)
	df_cad.columns=['cad_izq','cad_dcha']
	df_cad['dis']=abs(df_cad['cad_izq'])+df_cad['cad_dcha']
	ind_cad=df_cad.loc[df_cad['dis']==np.nanmin(df_cad['dis'])].index
	frame_cad_min=ind_cad+frame_change+30
	frame_cad_min=frame_cad_min.tolist()
	frame_cad_min=int(frame_cad_min[0])
	dif_frames=frame_sentada-frame_cad_min
	frame_acomodo=frame_cad_min-dif_frames
	if SpineBase_Z_arr[frame_cad_min]<3.5:
		c=-1
		for i in SpineBase_Z_arr[frame_change+30:]:
			c+=1
			if i>3.5:
				frame_acomodo=c+frame_change+30
				break
	
	if AnkleLeft_Z[frame_acomodo]<AnkleRight_Z[frame_acomodo]:
		limit_now=AnkleLeft_Z[frame_cad_min]
		w=0
	else:
		limit_now=AnkleRight_Z[frame_cad_min]
		w=1
	duracion=ktime[frame_sentada]-ktime[frame_acomodo] 

	return(limit_now,frame_cad_min,w,frame_acomodo, duracion)

def NumPasosAc(AnkleLeft_X_arr,AnkleRight_X_arr,dict_silla):
	#number of steps in the turn just before starting to sit on the return
	alr=AnkleLeft_X_arr.round(2)
	c=0
	pasos=[]
	for i in alr:
		c+=1
		if c+5<=len(alr) and i == alr[c+4]:
			pasos.append(1)
		else:
			pasos.append(0)		
	arr=AnkleRight_X_arr.round(2)
	c=0
	for i in arr:
		c+=1
		if c+5<len(alr) and i == arr[c+4]:
			pasos.append(1)
		else:
			pasos.append(0)
	num_pasos=0
	c=1
	for i in pasos:
		if i==1 and pasos[c]==0:
			num_pasos+=1		
	if num_pasos<1:
		num_pasos=2
	
	dict_silla['Numero de pasos en el giro']=num_pasos
	return(num_pasos)
	
	
