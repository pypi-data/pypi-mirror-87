import numpy as np

def angulo_brazo(ShoulderRight_Z_arr,ElbowRight_Z_arr,ShoulderRight_Y_arr,ElbowRight_Y_arr,ShoulderLeft_Z_arr,ElbowLeft_Z_arr,ShoulderLeft_Y_arr,ElbowLeft_Y_arr,WristRight_Z_arr,WristLeft_Z_arr,WristRight_Y_arr,WristLeft_Y_arr):
	  #derecha     
	z1=ShoulderRight_Z_arr-ElbowRight_Z_arr
	y1=ShoulderRight_Y_arr-ElbowRight_Y_arr
	
	z2=WristRight_Z_arr-ElbowRight_Z_arr
	y2=WristRight_Y_arr-ElbowRight_Y_arr
	cos_alpha=(z1*z2 + y1*y2)/ (np.sqrt(z1*z1 + y1*y1) * np.sqrt(z2*z2 + y2*y2))
	list_ang_dcha=np.arccos(cos_alpha)*57.29
	#izquierda
	z1=ShoulderLeft_Z_arr-ElbowLeft_Z_arr
	y1=ShoulderLeft_Y_arr-ElbowLeft_Y_arr
	
	z2=WristLeft_Z_arr-ElbowLeft_Z_arr
	y2=WristLeft_Y_arr-ElbowLeft_Y_arr
	cos_alpha=(z1*z2 + y1*y2)/ (np.sqrt(z1*z1 + y1*y1) * np.sqrt(z2*z2 + y2*y2))
	list_ang_izq=np.arccos(cos_alpha)*57.29
	
	return(list_ang_dcha, list_ang_izq)
	

def angulo_pierna(HipRight_Z_arr,KneeRight_Z_arr,AnkleRight_Z_arr,HipRight_Y_arr,KneeRight_Y_arr,AnkleRight_Y_arr,HipLeft_Z_arr,KneeLeft_Z_arr,AnkleLeft_Z_arr,HipLeft_Y_arr,KneeLeft_Y_arr,AnkleLeft_Y_arr):
	#derecha
	z1=HipRight_Z_arr-KneeRight_Z_arr
	y1=HipRight_Y_arr-KneeRight_Y_arr
	
	z2=AnkleRight_Z_arr-KneeRight_Z_arr
	y2=AnkleRight_Y_arr-KneeRight_Y_arr
	cos_alpha=(z1*z2 + y1*y2)/ (np.sqrt(z1*z1 + y1*y1) * np.sqrt(z2*z2 + y2*y2))
	list_ang_dcha=np.arccos(cos_alpha)*57.29
	#izquierda
	z1=HipLeft_Z_arr-KneeLeft_Z_arr
	y1=HipLeft_Y_arr-KneeLeft_Y_arr
	
	z2=AnkleLeft_Z_arr-KneeLeft_Z_arr
	y2=AnkleLeft_Y_arr-KneeLeft_Y_arr
	cos_alpha=(z1*z2 + y1*y2)/ (np.sqrt(z1*z1 + y1*y1) * np.sqrt(z2*z2 + y2*y2))
	list_ang_izq=np.arccos(cos_alpha)*57.29

	return(list_ang_dcha, list_ang_izq)

	
def ang_pierna_tronco(KneeRight_Z_arr,HipRight_Z_arr,SpineBase_Z_arr,KneeRight_Y_arr,HipRight_Y_arr,SpineBase_Y_arr,KneeLeft_Y_arr,HipLeft_Y_arr,KneeLeft_Z_arr,HipLeft_Z_arr,SpineShoulder_Z_arr,SpineShoulder_Y_arr):
	
	#derecha
	z1=KneeRight_Z_arr-HipRight_Z_arr
	y1=KneeRight_Y_arr-HipRight_Y_arr
	dif_cadera_z=SpineBase_Z_arr-HipRight_Z_arr
	dif_cadera_y=SpineBase_Y_arr-HipRight_Y_arr
	spineshoulder_z=SpineShoulder_Z_arr-dif_cadera_z
	spineshoulder_y=SpineShoulder_Y_arr-dif_cadera_y
	
	z2=spineshoulder_z-HipRight_Z_arr
	y2=spineshoulder_y-HipRight_Y_arr
	
	cos_alpha=(z1*z2 + y1*y2)/ (np.sqrt(z1*z1 + y1*y1) * np.sqrt(z2*z2 + y2*y2))
	list_ang_pdcha=np.arccos(cos_alpha)*57.29
	
	#izquierda
	z1=KneeLeft_Z_arr-HipLeft_Z_arr
	y1=KneeLeft_Y_arr-HipLeft_Y_arr
	dif_cadera_z=SpineBase_Z_arr-HipLeft_Z_arr
	dif_cadera_y=SpineBase_Y_arr-HipLeft_Y_arr
	spineshoulder_z=SpineShoulder_Z_arr-dif_cadera_z
	spineshoulder_y=SpineShoulder_Y_arr-dif_cadera_y
	
	z2=spineshoulder_z-HipLeft_Z_arr
	y2=spineshoulder_y-HipLeft_Y_arr
	
	cos_alpha=(z1*z2 + y1*y2)/ (np.sqrt(z1*z1 + y1*y1) * np.sqrt(z2*z2 + y2*y2))
	list_ang_pizq=np.arccos(cos_alpha)*57.29
	
	return(list_ang_pdcha,list_ang_pizq)

def inclinacion_tronco(SpineShoulder_Z_arr,SpineBase_Z_arr,SpineShoulder_Y_arr,SpineBase_Y_arr):
                
	z=SpineBase_Z_arr-SpineShoulder_Z_arr
	y=SpineShoulder_Y_arr - SpineBase_Y_arr
	list_ang=np.arctan(z/y).round(2)*57.29
	
	return (list_ang)