import pandas as pd
import numpy as np
from .utils import Minimos
import os
import matplotlib.pyplot as plt

def fases_prueba(SpineBase_Z_arr,list_ang_pdcha_col,list_ang_pizq_col,ktime,frame_acomodo,frame_sentada,frame_inc, frame_inc_begin, directory, save_fig=False):
	#INCORPORACION
	
	if os.path.exists(directory+'\weight.csv') is True:
		frame_inc_begin=int(frame_inc_begin*3/8)
		fase_inc=ktime[frame_inc]-ktime[frame_inc_begin]
		
	else:
	  
		minimos_col_dcha=Minimos(list_ang_pdcha_col[0:frame_inc])
		minimos_col_izq=Minimos(list_ang_pizq_col[0:frame_inc])
		for i in minimos_col_dcha[::-1]:
			if list_ang_pdcha_col[i] <90:
				frame_inc_begin_dcha=i
		for i in minimos_col_izq[::-1]:
			if list_ang_pizq_col[i] <90:
				frame_inc_begin_izq=i
				
		frame_inc_begin=int((frame_inc_begin_izq+frame_inc_begin_dcha)/2)
		fase_inc=ktime[frame_inc]-ktime[frame_inc_begin]
		
		
	#MARCHA HACIA DELANTE Y GIRO 
	l=[]
	c=-1
	for i in SpineBase_Z_arr:
		c+=1
		if i<=1.4:
				l.append(c)
				
	fase_marcha_adelante=ktime[l[0]]-ktime[frame_inc]
	fase_giro1=ktime[l[-1]]-ktime[l[0]]
	
	#MARCHA HACIA ATRÁS
	fase_marcha_atras=ktime[frame_acomodo]-ktime[l[-1]]
	
	#SEGUNDO GIRO
	fase_giro2=ktime[frame_sentada]-ktime[frame_acomodo]
	
	#SENTADA
	
	minimos_sent_fin_dcha=Minimos(list_ang_pdcha_col[frame_sentada:])
	minimos_sent_fin_izq=Minimos(list_ang_pizq_col[frame_sentada:])

	for i in minimos_sent_fin_dcha:
		if list_ang_pdcha_col[frame_sentada:][i]<120:
			frame_sentada_fin_dcha=i
			break

	for i in minimos_sent_fin_izq:
		if list_ang_pizq_col[frame_sentada:][i]<120:
			frame_sentada_fin_izq=i
			break
	frame_sentada_fin=int((frame_sentada_fin_izq+frame_sentada_fin_dcha)/2)
	frame_sentada_fin=frame_sentada+frame_sentada_fin
	fase_sentarse=ktime[frame_sentada_fin]-ktime[frame_sentada]
	print('ktime sentada fin',ktime[frame_sentada_fin])
	tiempo_total=fase_inc+fase_marcha_adelante+fase_giro1+fase_marcha_atras+fase_giro2+fase_sentarse
	
	#FIGURA
	label1=(ktime[frame_inc_begin]+ktime[frame_inc])/2
	label2=(ktime[frame_inc]+ktime[l[0]])/2
	label3=(ktime[l[0]]+ktime[l[-1]])/2
	label4=(ktime[l[-1]]+ktime[frame_acomodo])/2
	label5=(ktime[frame_acomodo]+ktime[frame_sentada])/2
	label6=(ktime[frame_sentada]+ktime[frame_sentada_fin])/2
	alt_label=0.7
	
	if frame_inc_begin<frame_inc<l[0]<l[-1]<frame_acomodo<frame_sentada<frame_sentada_fin:
	
		plt.figure(figsize=(20,3))
		plt.plot(ktime,np.repeat(0,len(ktime)),'k')
		plt.axvline(ktime[frame_inc_begin],color='k',ls='--')
		plt.axvline(ktime[frame_inc],color='k',ls='--')
		plt.axvline(ktime[l[0]],color='k',ls='--')
		plt.axvline(ktime[l[-1]],color='k',ls='--')
		plt.axvline(ktime[frame_acomodo],color='k',ls='--')
		plt.axvline(ktime[frame_sentada],color='k',ls='--')
		plt.axvline(ktime[frame_sentada_fin],color='k',ls='--')
		plt.ylim(0,1)
		plt.yticks([])
		plt.title('FASES DE LA PRUEBA (Tiempo Total: {} s)'.format(round(tiempo_total,2)))
		plt.xlabel('tiempo /s')
		plt.text(label1,alt_label,'INCORPORACIÓN\n\n{}s'.format(round(fase_inc,2)),horizontalalignment='center',rotation=0)
		plt.text(label2,alt_label,'MARCHA\nADELANTE\n\n{}s'.format(round(fase_marcha_adelante,2)),horizontalalignment='center',rotation=0)
		plt.text(label3,alt_label,'GIRO\nMEDIO\n\n{}s'.format(round(fase_giro1,2)),horizontalalignment='center',rotation=0)
		plt.text(label4,alt_label,'MARCHA\nATRÁS\n\n{}s'.format(round(fase_marcha_atras,2)),horizontalalignment='center',rotation=0)
		plt.text(label5,alt_label,'GIRO\nFINAL\n\n{}s'.format(round(fase_giro2,2)),horizontalalignment='center',rotation=0)
		plt.text(label6,alt_label,'SENTADA\n\n{}s'.format(round(fase_sentarse,2)),horizontalalignment='center',rotation=0)
		plt.axvspan(ktime[frame_inc_begin],ktime[frame_inc],alpha=0.1,color='green')
		plt.axvspan(ktime[frame_inc],ktime[l[0]],alpha=0.1,color='red')
		plt.axvspan(ktime[l[0]],ktime[l[-1]],alpha=0.1,color='yellow')
		plt.axvspan(ktime[l[-1]],ktime[frame_acomodo],alpha=0.1,color='red')
		plt.axvspan(ktime[frame_acomodo],ktime[frame_sentada],alpha=0.1,color='yellow')
		plt.axvspan(ktime[frame_sentada],ktime[frame_sentada_fin],alpha=0.1,color='green')
		if save_fig==True:
			plt.savefig(directory+'/data_info/fases.png',bbox_inches = 'tight')
		else:
			plt.show()
		plt.close()
	else:
		pass

 