import pandas as pd
import numpy as np
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
from .utils import SinglePoint, Smooth, mean_std


def steps_index(KneeLeft_Z,KneeRight_Z,list_ang_pdcha,list_ang_pizq, ktime, frame_change, frame_inc):
	#busca los frames en los que empieza y termina cada paso con cada pierna
	#lo hace utilizando primero la distancia de cada rodilla a la cámara
	#y después la forma del ángulo de la rodilla
	n=2
	slice_= lambda A, n=n: [A[i:i+n] for i in range(0, len(A), n)]

	ci=pd.Series(KneeLeft_Z).interpolate(method='polynomial', order=2).tolist()
	cd=pd.Series(KneeRight_Z).interpolate(method='polynomial', order=2).tolist()
	ci=np.asarray(ci)
	cd=np.asarray(cd)
	ktime_arr=np.asarray(ktime)
	s_list_ang_pdcha=Smooth(pd.Series(list_ang_pdcha[:frame_change]).interpolate(method='polynomial', order=2).tolist(),10)
	s_list_ang_pizq=Smooth(pd.Series(list_ang_pizq[:frame_change]).interpolate(method='polynomial', order=2).tolist(),10)
	
	first_nan_izq=np.where(np.isnan(np.array(s_list_ang_pizq)))[0][0]
	first_nan_dcha=np.where(np.isnan(np.array(s_list_ang_pdcha)))[0][0]

	idx_total = np.argwhere(np.diff(np.sign(cd - ci))).flatten()
	idx=[]
	for i in idx_total:
		if i>frame_inc-15 and i<frame_change:
			idx.append(i)
			

	idx_slice1=slice_(idx)
	idx_slice2=slice_(idx[1:])

	idx_slice1=[i for i in idx_slice1 if len(i)>1]
	idx_slice2=[i for i in idx_slice2 if len(i)>1]

	idx_slice1_fit=[i for i in idx_slice1 if i[1]-i[0]>2]
	idx_slice2_fit=[i for i in idx_slice2 if i[1]-i[0]>2]

	idx1=[j for i in idx_slice1_fit for j in i]
	idx2=[j for i in idx_slice2_fit for j in i]
	idx=np.sort(idx1+idx2)
	idx=SinglePoint(idx)

	sign_first_leg=np.mean(cd[idx_slice1_fit[0][0]+1:idx_slice1_fit[0][1]]-ci[idx_slice1_fit[0][0]+1:idx_slice1_fit[0][1]])
	if sign_first_leg<0:
		pierna_izq=[idx_slice1_fit,s_list_ang_pizq]
		pierna_dcha=[idx_slice2_fit,s_list_ang_pdcha]
	else:
		pierna_izq=[idx_slice2_fit,s_list_ang_pizq]
		pierna_dcha=[idx_slice1_fit,s_list_ang_pdcha]

	pierna_izq[0]=[i for i in pierna_izq[0] if i[0]<first_nan_izq ]
	pierna_dcha[0]=[i for i in pierna_dcha[0] if i[0]<first_nan_dcha ]
	
	value_max_idx_slice_izq=[]
	ind_max_idx_slice_izq=[]
	value_max_idx_slice_dcha=[]
	ind_max_idx_slice_dcha=[]
	for i in pierna_izq[0]:
		if len(i)>1 and i[1]-i[0]>2:
			l=pierna_izq[1][i[0]:i[1]]
			val=np.nanmax(l)
			m=argrelextrema(np.array(l),np.greater)[0]
			l2=[l[i] for i in m]
			#if len(l2)==0 and i==pierna_izq[0][-1]:
			if i==pierna_izq[0][-1]:
				if len(l2)==0:
					l2=[j for j in l if 160<j<=180]
				else:
					l2=[j for j in l2 if 160<j<=180]
			try:
				val2=l2[0]
				if np.isnan(val)==False:
					value_max_idx_slice_izq.append(val2)
					ind_max_idx_slice_izq.append(list(l).index(val2)+i[0])
			except:pass
			
	for i in pierna_dcha[0]:
		if len(i)>1 and i[1]-i[0]>2:
			l=pierna_dcha[1][i[0]:i[1]]
			val=np.nanmax(l)
			m=argrelextrema(np.array(l),np.greater)[0]
			l2=[l[i] for i in m]
			#if len(l2)==0 and i==pierna_dcha[0][-1]:
			#	l2=[j for j in l if 160<j<=180]
			if i==pierna_dcha[0][-1]:
				if len(l2)==0:
					l2=[j for j in l if 160<j<=180]
				else:
					l2=[j for j in l2 if 160<j<=180]
			try:
				val2=np.nanmax(l2)
				if np.isnan(val)==False:
					value_max_idx_slice_dcha.append(val2)
					ind_max_idx_slice_dcha.append(list(l).index(val2)+i[0])
			except:pass
	
	n=2
	slice_2= lambda A, n=n: [A[i:i+n] for i in range(0, len(A), 1) if len(A[i:i+n])==2]
	steps_izq=slice_2(ind_max_idx_slice_izq)
	steps_dcha=slice_2(ind_max_idx_slice_dcha)
	
	return(steps_izq, steps_dcha)

'''
def steps_info(AnkleLeft_Z,AnkleRight_Z, frame_change,steps_izq, steps_dcha, ktime,dict_marcha):
	steps_izq_times=[ktime[i[1]]-ktime[i[0]] for i in steps_izq]
	steps_dcha_times=[ktime[i[1]]-ktime[i[0]] for i in steps_dcha]
	mean_time_steps_izq=np.nanmean(steps_izq_times)
	mean_time_steps_dcha=np.nanmean(steps_dcha_times)
	
	ankly=Smooth(pd.Series(AnkleLeft_Z[:frame_change]).interpolate(method='polynomial', order=2).tolist(),10)
	ankry=Smooth(pd.Series(AnkleRight_Z[:frame_change]).interpolate(method='polynomial', order=2).tolist(),10)
	steps_izq_len=[ankly[i[0]]-ankly[i[1]] for i in steps_izq]
	steps_dcha_len=[ankry[i[0]]-ankry[i[1]] for i in steps_dcha]
	mean_len_steps_izq=np.nanmean(steps_izq_len)
	mean_len_steps_dcha=np.nanmean(steps_dcha_len)
	
	cadencia=(len(steps_izq)+len(steps_dcha))/((mean_time_steps_izq*len(steps_izq) + mean_time_steps_dcha*len(steps_dcha))/60)
	dict_marcha['Numero pasos pierna izquierda']= len(steps_izq)*2
	dict_marcha['Numero pasos pierna derecha']= len(steps_dcha)*2
	dict_marcha['Tiempo medio zancada izquierda  /s']= round(mean_time_steps_izq,2)
	dict_marcha['Tiempo medio zancada derecha  /s']= round(mean_time_steps_dcha,2)
	dict_marcha['Distancia media zancada izquierda  /m']= round(mean_len_steps_izq,2)
	dict_marcha['Distancia media zancada derecha  /m']= round(mean_len_steps_dcha,2)
	dict_marcha['Cadencia estimada de la marcha  / pasos/min']= int(cadencia)*2
		
	return(len(steps_izq),len(steps_dcha),mean_time_steps_izq,mean_time_steps_dcha,mean_len_steps_izq,mean_len_steps_dcha)
'''
def steps_info(KneeLeft_Z,KneeRight_Z,AnkleLeft_Z,AnkleRight_Z, frame_inc, frame_change, ktime,dict_marcha):
	n=2
	slice_2= lambda A, n=n: [A[i:i+n] for i in range(0, len(A), 1) if len(A[i:i+n])==2]
	slice_= lambda A, n=n: [A[i:i+n] for i in range(0, len(A), n)]
	ci=pd.Series(KneeLeft_Z).interpolate(method='polynomial', order=2).tolist()
	cd=pd.Series(KneeRight_Z).interpolate(method='polynomial', order=2).tolist()
	ci=np.asarray(ci)
	cd=np.asarray(cd)
	ktime_arr=np.asarray(ktime)
	idx_total = np.argwhere(np.diff(np.sign(cd - ci))).flatten()
	idx=[]
	for i in idx_total:
		if i>frame_inc-15 and i<frame_change:
			idx.append(i)
	idx_slice1=slice_(idx)
	idx_slice2=slice_(idx[1:])
	idx_slice1_fit=[i for i in idx_slice1 if (len(i)>1 and i[1]-i[0]>2)]
	idx_slice2_fit=[i for i in idx_slice2 if (len(i)>1 and i[1]-i[0]>2)]
	idx1=[j for i in idx_slice1_fit for j in i]
	idx2=[j for i in idx_slice2_fit for j in i]
	idx=np.sort(idx1+idx2)
	idx=SinglePoint(idx)
	
	sign_first_leg=np.mean(cd[idx_slice1_fit[0][0]+1:idx_slice1_fit[0][1]]-ci[idx_slice1_fit[0][0]+1:idx_slice1_fit[0][1]])
	if sign_first_leg<0:
		first_leg='dcha'
	else:
		first_leg='izq'
	
	if first_leg=='izq':
		idx_stride_izq=[i for n,i in enumerate(idx) if n%2==0]
		idx_stride_dcha=[i for n,i in enumerate(idx) if n%2!=0]
	else:
		idx_stride_dcha=[i for n,i in enumerate(idx) if n%2==0]
		idx_stride_izq=[i for n,i in enumerate(idx) if n%2!=0]
		
		
	idx_stride_izq_slice=slice_2(idx_stride_izq)
	idx_stride_dcha_slice=slice_2(idx_stride_dcha)
	times_izq=[ktime[i[1]]-ktime[i[0]] for i in idx_stride_izq_slice]
	times_dcha=[ktime[i[1]]-ktime[i[0]] for i in idx_stride_dcha_slice]
	len_izq=[AnkleLeft_Z[i[0]]-AnkleLeft_Z[i[1]] for i in idx_stride_izq_slice]
	len_dcha=[AnkleRight_Z[i[0]]-AnkleRight_Z[i[1]] for i in idx_stride_izq_slice]
	
	n_ciclos=(len(idx_stride_izq_slice)+len(idx_stride_dcha_slice))
	
	cadencia=(n_ciclos*2)/((np.mean([np.nanmean(times_dcha),np.nanmean(times_izq)])*(2*n_ciclos))/60)
	
	
	dict_marcha['Numero zancadas/ciclos pierna izquierda']= len(idx_stride_izq_slice)
	dict_marcha['Numero zancadas/ciclos pierna derecha']= len(idx_stride_dcha_slice)
	dict_marcha['Tiempo medio zancada/ciclo pierna izquierda  /s']= round(np.nanmean(times_izq),2)
	dict_marcha['Tiempo medio zancada/ciclo pierna derecha  /s']= round(np.nanmean(times_dcha),2)
	dict_marcha['Distancia media zancada/ciclo pierna izquierda  /m']= round(np.nanmean(len_izq),2)
	dict_marcha['Distancia media zancada/ciclo pierna derecha  /m']= round(np.nanmean(len_dcha),2)
	dict_marcha['Cadencia estimada de la marcha  / pasos/min']= int(cadencia)*2
	
	return(n_ciclos)
	
def steps_index2(AnkleLeft_Z,AnkleRight_Z, frame_inc, frame_change):
	n=2
	slice_= lambda A, n=n: [A[i:i+n] for i in range(0, len(A), n)]
	slice_2= lambda A, n=n: [A[i:i+n] for i in range(0, len(A), 1) if len(A[i:i+n])==2]
	ankly=np.array(Smooth(pd.Series(AnkleLeft_Z[:frame_change]).interpolate(method='polynomial', order=2).tolist(),6))
	ankry=np.array(Smooth(pd.Series(AnkleRight_Z[:frame_change]).interpolate(method='polynomial', order=2).tolist(),6))
	l=ankly[frame_inc:]-ankry[frame_inc:]
	maxs=argrelextrema(l,np.greater)[0]
	mins=argrelextrema(l,np.less)[0]
	maxs_values=[l[i] for i in maxs]
	if maxs_values[-1]<0.9*np.nanmean(maxs_values):
		maxs=maxs[:-1]
	maxs=[i+frame_inc for i in maxs]
	mins=[i+frame_inc for i in mins]
	maxs=slice_2(maxs)
	mins=slice_2(mins)
	maxs=[i for i in maxs if len(i)>1]
	mins=[i for i in mins if len(i)>1]
	steps_izq=maxs
	steps_dcha=mins
	
	return(steps_izq, steps_dcha)
	
	
	
def knee_angles_gait(frame_change,list_ang_pdcha,list_ang_pizq, ktime, steps_izq, steps_dcha, directory, dict_paso, save_fig=False):
	s_list_ang_pdcha=Smooth(pd.Series(list_ang_pdcha[:frame_change]).interpolate(method='polynomial', order=2).tolist(),10)
	s_list_ang_pizq=Smooth(pd.Series(list_ang_pizq[:frame_change]).interpolate(method='polynomial', order=2).tolist(),10)
	s_list_ang_pdcha_invert=np.abs(180-np.array(s_list_ang_pdcha))
	s_list_ang_pizq_invert=np.abs(180-np.array(s_list_ang_pizq))

	
	steps_1=[]
	x_list_int_izq=[]
	for step in steps_izq:
		data=s_list_ang_pizq_invert[step[0]:step[1]]
		x=np.linspace(0,100,len(ktime[step[0]:step[1]]))
		x_int=[int(i) for i in x]
		x_list_int_izq.append(x_int)
		steps_1.append(data)

	
	steps_2=[]
	x_list_int_dcha=[]
	for step in steps_dcha:
		data=s_list_ang_pdcha_invert[step[0]:step[1]]
		x=np.linspace(0,100,len(ktime[step[0]:step[1]]))
		x_int=[int(i) for i in x]
		x_list_int_dcha.append(x_int)
		steps_2.append(data)

	x=np.arange(101)
	pierna_dcha=mean_std(x_list_int_dcha, steps_2)
	pierna_izq=mean_std(x_list_int_izq, steps_1)
	
	fig, axs = plt.subplots(1, 2, figsize=(14,3))
	fig.suptitle('Ángulos de la Rodilla \n', fontsize=14)
	axs[0].plot(x, pierna_dcha[0],label='Rodilla_dcha')
	axs[0].fill_between(x,pierna_dcha[0]-pierna_dcha[1], pierna_dcha[0]+pierna_dcha[1], alpha=0.1, color='blue')
	axs[0].grid(True)
	axs[1].plot(x, pierna_izq[0],label='Rodilla_izq')
	axs[1].grid(True)
	axs[1].fill_between(x,pierna_izq[0]-pierna_izq[1], pierna_izq[0]+pierna_izq[1], alpha=0.1, color='blue')
	axs[1].legend()
	axs[0].legend()
	axs[0].set_xlabel('\n% Ciclo Pierna DERECHA (n={})'.format(len(steps_dcha)), fontsize=14)
	axs[1].set_xlabel('\n% Ciclo Pierna IZQUIERDA (n={})'.format(len(steps_izq)), fontsize=14)
	axs[1].set_ylabel('Ángulo rodilla /deg')
	axs[0].set_ylabel('Ángulo rodilla /deg')
	if save_fig==True:
		plt.savefig(directory+'/data_info/paso/knee_angles_gait.png',bbox_inches = 'tight')
	else:
		plt.show()
	plt.close()
	max_angle_izq=np.nanmax(pierna_izq[0])
	max_angle_dcha=np.nanmax(pierna_dcha[0])
	
	dict_paso['Angulo flexion rodilla izquierda /deg']= round(max_angle_izq,2)
	dict_paso['Angulo flexion rodilla derecha /deg']= round(max_angle_dcha,2)
	
	return(max_angle_izq,max_angle_dcha)
	
def InfoCads(HipLeft_X,HipLeft_Y,HipLeft_Z,HipRight_X,HipRight_Y,HipRight_Z, list_ang_tronco, ktime, steps_izq, steps_dcha,directory, save_fig=False):
	#Busca los ángulos de la cadera en cada paso en función de los frames encontrados con steps_index()
		 
	ci_x_fit=Smooth(HipLeft_X,6)
	ci_y_fit=Smooth(HipLeft_Y,6)
	ci_z_fit=Smooth(HipLeft_Z,6)
	cd_x_fit=Smooth(HipRight_X,6)
	cd_y_fit=Smooth(HipRight_Y,6)
	cd_z_fit=Smooth(HipRight_Z,6)

	 #OBLICUIDAD
	ci_x_arr=np.asarray(ci_x_fit)
	ci_y_arr=np.asarray(ci_y_fit)
	cd_x_arr=np.asarray(cd_x_fit)
	cd_y_arr=np.asarray(cd_y_fit)
	dif_cadera_x=ci_x_arr-cd_x_arr
	dif_cadera_y=ci_y_arr-cd_y_arr

	tan_alpha=dif_cadera_y/dif_cadera_x
	alpha=np.rad2deg(np.arctan(tan_alpha))

	#ROTACION
	ci_z_arr=np.asarray(ci_z_fit)
	cd_z_arr=np.asarray(cd_z_fit)

	dif_cadera_z=ci_z_arr-cd_z_arr

	tan_alpha_rot=dif_cadera_z/dif_cadera_x
	alpha_rot=np.rad2deg(np.arctan(tan_alpha_rot))

	######################matriz figuras###########################################
	if len(steps_izq)>4:
		steps_izq_cut=steps_izq[1:-1]
	elif len(steps_izq)>3:
		steps_izq_cut=steps_izq[1:]
	else:
		steps_izq_cut=steps_izq
		
	if len(steps_dcha)>4:
		steps_dcha_cut=steps_dcha[1:-1]
	elif len(steps_dcha)>3:
		steps_dcha_cut=steps_dcha[1:]
	else:
		steps_dcha_cut=steps_dcha
		
	steps_ang_tronco_izq=[]
	steps_rot_izq=[]
	steps_ob_izq=[]
	x_list_int_izq=[]


	for n,step in enumerate(steps_izq_cut):
		y1=Smooth(list_ang_tronco[step[0]:step[1]],6)
		y2=alpha_rot[step[0]:step[1]]
		y3=alpha[step[0]:step[1]]
		x=np.linspace(0,100,len(ktime[step[0]:step[1]]))
		x_int=[int(i) for i in x]
		steps_ang_tronco_izq.append(y1)
		steps_rot_izq.append(y2)
		steps_ob_izq.append(y3)
		x_list_int_izq.append(x_int)

	steps_ang_tronco_dcha=[]
	steps_rot_dcha=[]
	steps_ob_dcha=[]
	x_list_int_dcha=[]
	for n,step in enumerate(steps_dcha_cut):
		y1=Smooth(list_ang_tronco[step[0]:step[1]],6)
		y2=alpha_rot[step[0]:step[1]]
		y3=alpha[step[0]:step[1]]
		x=np.linspace(0,100,len(ktime[step[0]:step[1]]))
		x_int=[int(i) for i in x]
		steps_ang_tronco_dcha.append(y1)
		steps_rot_dcha.append(y2)
		steps_ob_dcha.append(y3)
		x_list_int_dcha.append(x_int)
		  

	fig, axs = plt.subplots(3, 2, figsize=(12,5))
	fig.tight_layout(rect=[0, 0, 1, 0.9]) 
	fig.suptitle('Ángulos de la Cadera', fontsize=14)
	x=np.arange(101)

	tronco_izq=mean_std(x_list_int_izq, steps_ang_tronco_izq)
	rot_izq=mean_std(x_list_int_izq, steps_rot_izq)
	ob_izq=mean_std(x_list_int_izq, steps_ob_izq)

	axs[0, 1].plot(x, tronco_izq[0], label='{} Ciclo'.format(n))
	axs[0, 1].fill_between(x,tronco_izq[0]-tronco_izq[1], tronco_izq[0]+tronco_izq[1], alpha=0.1, color='blue')
	axs[1, 1].plot(x, rot_izq[0],label='{} Ciclo'.format(n))
	axs[1, 1].fill_between(x,rot_izq[0]-rot_izq[1], rot_izq[0]+rot_izq[1], alpha=0.1, color='blue')
	axs[2, 1].plot(x,ob_izq[0],label='{} Ciclo'.format(n))
	axs[2, 1].fill_between(x,ob_izq[0]-ob_izq[1], ob_izq[0]+ob_izq[1], alpha=0.1, color='blue')
	axs[0, 1].set_title('INCLINACIÓN COLUMNA')
	axs[0, 1].grid(True)
	axs[0, 1].axhline(0, color='black')
		
	axs[1, 1].set_title('ROTACIÓN')
	axs[1, 1].grid(True)
	axs[1, 1].axhline(0, color='black')
		
	axs[2, 1].set_title('OBLICUIDAD')
	axs[2, 1].grid(True)
	axs[2, 1].axhline(0, color='black')
	axs[2, 1].set_xlabel('\n% Ciclo Pierna IZQUIERDA (n={})'.format(len(steps_izq_cut)), fontsize=14)


	tronco_dcha=mean_std(x_list_int_dcha, steps_ang_tronco_dcha)
	rot_dcha=mean_std(x_list_int_dcha, steps_rot_dcha)
	ob_dcha=mean_std(x_list_int_dcha, steps_ob_dcha)

	axs[0, 0].plot(x, tronco_dcha[0], label='{} Ciclo'.format(n))
	axs[0, 0].fill_between(x,tronco_dcha[0]-tronco_dcha[1], tronco_dcha[0]+tronco_dcha[1], alpha=0.1, color='blue')
	axs[1, 0].plot(x, rot_dcha[0],label='{} Ciclo'.format(n))
	axs[1, 0].fill_between(x,rot_dcha[0]-rot_dcha[1], rot_dcha[0]+rot_dcha[1], alpha=0.1, color='blue')
	axs[2, 0].plot(x,ob_dcha[0],label='{} Ciclo'.format(n))
	axs[2, 0].fill_between(x,ob_dcha[0]-ob_dcha[1], ob_dcha[0]+ob_dcha[1], alpha=0.1, color='blue')
	axs[0, 0].set_title('INCLINACIÓN COLUMNA')
	axs[0, 0].grid(True)
	axs[0, 0].axhline(0, color='black')

	axs[1, 0].set_title('ROTACIÓN')
	axs[1, 0].grid(True)
	axs[1, 0].axhline(0, color='black')

	axs[2, 0].set_title('OBLICUIDAD')
	axs[2, 0].grid(True)
	axs[2, 0].axhline(0, color='black')
	axs[2, 0].set_xlabel('\n% Ciclo Pierna DERECHA (n={})'.format(len(steps_dcha_cut)), fontsize=14)

	if save_fig==True:
		plt.savefig(directory+'/data_info/paso/hip_angles_gait.png',bbox_inches = 'tight')
	else:
		plt.show()
	plt.close()


