import matplotlib.pyplot as plt
import numpy as np


def speed(SpineBase_Z, ktime, frame_inc, frame_change, directory,dict_marcha, plot=False, save_fig=False):     
	dist_recorrida_vel=[]
	l=[]
	dist_recorrida_vel2=[]
	l2=[]
	
	c=-1
	for i in SpineBase_Z[:frame_change]:
		c+=1  
		if i <=3 and i>=2:
			dist_recorrida_vel.append(i)
			l.append(c)
		if i <=3.3 and i>=1.8:
			dist_recorrida_vel2.append(i)
			l2.append(c)
					
	dist=dist_recorrida_vel[0]-dist_recorrida_vel[-1]
	t=ktime[l[-1]]-ktime[l[0]]
	vel_med1=dist/t

	dist2=dist_recorrida_vel2[0]-dist_recorrida_vel2[-1]
	t2=ktime[l2[-1]]-ktime[l2[0]]
	vel_med2=dist2/t2
	
	
	dict_marcha['Velocidad de la marcha  (medida entre 2 y 3 m) / m/s']= round(vel_med1,2)
	dict_marcha['Velocidad de la marcha  (medida entre 1.8 y 3.3 m) / m/s']= round(vel_med2,2)

	
	n=3
	slice_= lambda A, n=n: [A[i:i+n] for i in range(0, len(A), n)] #agrupa valores de una lista de n en n
	#slice_2= lambda A, n=2: [A[i:i+n] for i in range(0, len(A), n)]
	
	SpineBase_slice=slice_(SpineBase_Z[frame_inc+5:frame_change])
	ktime_slice=slice_(ktime[frame_inc+5:frame_change])
	
	dist_inst=[]
	for i in SpineBase_slice:
		if len(i)==n:
			dist_inst.append(np.abs(i[1]-i[0]))
	dist_plot=[]
	for i in SpineBase_slice:
		if len(i)==n:
			dist_plot.append(np.nanmean(i))

	time_inst=[]      
	for i in ktime_slice:
		if len(i)==n:
			time_inst.append(np.abs(i[1]-i[0]))   
	time_plot=[]      
	for i in ktime_slice:
		if len(i)==n:
			time_plot.append(np.nanmean(i))   
			
	vel_inst=np.array(dist_inst)/np.array(time_inst)
	
	vel_max=np.nanmax(vel_inst[vel_inst != np.inf])
	
	#if dicti==True:
	dict_marcha['Velocidad maxima / m/s']= round(vel_max,2)
		
	if plot==True:
		fig, axs = plt.subplots(2, 1,figsize=(16,5))
		axs[0].bar(dist_plot,vel_inst,color='red', edgecolor='black',width=0.05, align='center')
		axs[1].bar(time_plot,vel_inst,color='blue', edgecolor='black',width=0.05, align='center')
		axs[0].set_xlabel('Distancia a la Kinect (ida) /m')
		axs[0].set_ylabel('Velocidad instantánea  / m/s')
		axs[0].set_xlim(np.nanmax(dist_plot)+0.2,np.nanmin(dist_plot)-0.2)
		axs[1].set_xlim(np.nanmin(time_plot)-0.2,np.nanmax(time_plot)+0.2)
		axs[1].set_xlabel('Tiempo transcurrido (ida) /s')
		axs[1].set_ylabel('Velocidad instantánea  / m/s')
		axs[0].set_title('Velocidad Instantánea (ida) / m/s', fontsize=12)
		axs[1].set_axisbelow(True)
		axs[0].set_axisbelow(True)
		axs[1].grid(True)
		axs[0].grid(True)
		time_span_ind=[index for index, value in enumerate(np.array(dist_plot).astype(int)) if value == 2]
		time_span_ind2=[index for index, value in enumerate(np.array(dist_plot)) if (value <= 3.3 and value >=1.8)]
		axs[1].axvspan(time_plot[time_span_ind[0]],time_plot[time_span_ind[-1]],alpha=0.1,color='blue')
		axs[0].axvspan(dist_plot[time_span_ind[0]],dist_plot[time_span_ind[-1]],alpha=0.1,color='red')
		axs[1].axvspan(time_plot[time_span_ind2[0]],time_plot[time_span_ind2[-1]],alpha=0.1,color='blue')
		axs[0].axvspan(dist_plot[time_span_ind2[0]],dist_plot[time_span_ind2[-1]],alpha=0.1,color='red')
		fig.subplots_adjust(hspace=0.5)
		if save_fig==True:
			plt.savefig(directory+'/data_info/marcha/vel_inst.png')
		else:
			plt.show()
		plt.close()

	return(vel_med1,vel_med2,round(vel_max,2))