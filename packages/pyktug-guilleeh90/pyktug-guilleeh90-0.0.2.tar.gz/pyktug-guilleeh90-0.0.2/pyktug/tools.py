import numpy as np

def inclinacion_plano(frame_inc, frame_change, Neck_Z, Neck_Y,SpineBase_Z,SpineBase_Y,SpineMid_Z,SpineMid_Y, dict_tec):
	#busca la inclinación de la Kinect respecto al plano horizontal (suelo) mediante la variación
	#de la altura de varios puntos del cuerpo cuya altura es cuasiconstante durante la marcha
	x_neck=np.asarray(Neck_Z[frame_inc:frame_change], dtype='int32')
	p = np.polyfit(x_neck, Neck_Y[frame_inc:frame_change], 1)
	y_ajuste_neck = p[0]*x_neck + p[1]

	x_base=np.asarray(SpineBase_Z[frame_inc:frame_change], dtype='int32')
	p = np.polyfit(x_base, SpineBase_Y[frame_inc:frame_change], 1)
	y_ajuste_base = p[0]*x_base + p[1]


	x_mid=np.asarray(SpineMid_Z[frame_inc:frame_change], dtype='int32')
	p = np.polyfit(x_mid, SpineMid_Y[frame_inc:frame_change], 1)
	y_ajuste_mid = p[0]*x_mid + p[1]

	if (y_ajuste_base[0]>y_ajuste_base[-1] and y_ajuste_mid[0]>y_ajuste_mid[-1] and 
	y_ajuste_neck[0]>y_ajuste_neck[-1]):
		angle_neck = np.rad2deg(np.arctan2(y_ajuste_neck[0] - y_ajuste_neck[-1], x_neck[0] - x_neck[-1]))
		angle_base = np.rad2deg(np.arctan2(y_ajuste_base[0] - y_ajuste_base[-1], x_base[0] - x_base[-1]))
		angle_mid = np.rad2deg(np.arctan2(y_ajuste_mid[0] - y_ajuste_mid[-1], x_mid[0] - x_mid[-1]))

		angle=(angle_neck+angle_base+angle_mid)/3
		
		#dict_tec['Inclinacion plano horizontal (descendente) / grados']=round(angle,1)
		
		angle=angle*(-1)
		
	elif (y_ajuste_base[-1]>y_ajuste_base[0] and y_ajuste_mid[-1]>y_ajuste_mid[0] and 
	y_ajuste_neck[-1]>y_ajuste_neck[0]):
		angle_neck = np.rad2deg(np.arctan2(y_ajuste_neck[-1] - y_ajuste_neck[0], x_neck[-1] - x_neck[0]))
		angle_base = np.rad2deg(np.arctan2(y_ajuste_base[-1] - y_ajuste_base[0], x_base[-1] - x_base[0]))
		angle_mid = np.rad2deg(np.arctan2(y_ajuste_mid[-1] - y_ajuste_mid[0], x_mid[-1] - x_mid[0]))

		angle=180-(angle_neck+angle_base+angle_mid)/3
		
		
		#dict_tec['Inclinacion plano horizontal (ascendente) / grados']=round(angle,1)
	else:
		angle=0
		#dict_tec['Inclinacion plano horizontal / grados']=round(angle,1)
	
	dict_tec['Inclinacion plano horizontal / grados']=round(angle,1)

	return(angle)