import numpy as np
from scipy.signal import argrelextrema
from scipy.signal import savgol_filter
import pandas as pd


def SinglePoint(iterable): #elimina valores duplicados y adyacentes
	lista=[]
	prev = object()
	for item in iterable:
		if item != prev and item != np.nan:
			prev = item
			lista.append(item)
			
	return(lista)


def change_nans(l1,l2): #intercala los nans de una lista entre los valores de otra en la misma posición
	l=[]
	c=-1
	for i in l1:
		if np.isnan(i):
			l.append(i)
		else:
			c+=1
			l.append(l2[c])
	return(l)
	
def Smooth(data,g): #suaviza las curvas aunque tengan valores nans, analiza todos los datos no nans en conjunto
	data=np.asarray(data)
	data_nans=data[~ np.isnan(data)]
	window=41
	if len(data_nans)<window and len(data_nans)%2==0:
		window=len(data_nans)-1
	elif len(data_nans)<window and len(data_nans)%2!=0:
		window=len(data_nans)
	data_filter=savgol_filter(data_nans,window,g)
	data_fit=[]
	c=-1
	for i in data:
		if np.isnan(i):
			data_fit.append(i)
		else:
			c+=1
			data_fit.append(data_filter[c])
	return(data_fit)
	
			
def Maximos(data):#función para encontrar máximos en iterables que contengan nans y que requieren suavizado
	if isinstance(data,list):
		pass
	else:
		data=data.tolist()
		
	data_arr=np.asarray(data)
	data_nan=data_arr[~np.isnan(data_arr)]
	window=41
	if len(data_nan)<window and len(data_nan)%2==0:
		window=len(data_nan)-1
	elif len(data_nan)<window and len(data_nan)%2!=0:
		window=len(data_nan)
		
	data_filter=savgol_filter(data_nan,window,9)
	maximos=argrelextrema(data_filter, np.greater_equal)[0]
	maximos_fit=[]
	for i in maximos:
		maximos_fit.append(data.index(data_nan[i]))

	if maximos_fit[-1]==data.index(data_nan[-1]):
		maximos_fit=maximos_fit[:-1]    

	if maximos_fit[0]==0:
		maximos_fit=maximos_fit[1:]


	return(maximos_fit)
	
def Minimos(data):#función para encontrar mínimos en iterables que contengan nans y que requieren suavizado
	if isinstance(data,list):
		pass
	else:
		data=data.tolist()
		
	data_arr=np.asarray(data)
	data_nan=data_arr[~np.isnan(data_arr)]
	
	window=41
	if len(data_nan)<window and len(data_nan)%2==0:
		window=len(data_nan)-1
	elif len(data_nan)<window and len(data_nan)%2!=0:
		window=len(data_nan)
	print('window',window)
	if window>9:
		data_filter=savgol_filter(data_nan,window,9)
	else:
		data_filter=savgol_filter(data_nan,window,window-1)
	
	minimos=argrelextrema(data_filter, np.less_equal)[0]
	minimos_fit=[]
	for i in minimos:
		minimos_fit.append(data.index(data_nan[i]))

	if minimos_fit[-1]==data.index(data_nan[-1]):
		minimos_fit=minimos_fit[:-1]    

	if minimos_fit[0]==0:
		minimos_fit=minimos_fit[1:]

	return(minimos_fit)

def CountMax2(data,umbral):  #Máximos a partir de un umbral
	index=Maximos(data)
	values=[]
	for i in index:
		values.append(data[i])
	max_abs=np.max(values)
	index_umbral=[]
	for i in index:
		if data[i]>=max_abs*umbral:
			index_umbral.append(i)
	first_max=index_umbral[0]
	return(first_max)
	
def CountMax(data):
	values=SinglePoint(data)
	maxvalue=[]

	for i in values:
		if (i > np.nanmax(values)*0.95):
			maxvalue.append(i)

	return(maxvalue)
	
def frame_firstmax_lists(data1, data2): #busca el primer máximo para cada lista y hace la media

	max_1=CountMax(data1)
	max_2=CountMax(data2)
	values_1=np.where(data1 == max_1[0])
	values_2=np.where(data2 == max_2[0])

	frame=int((values_1[0]+values_2[0])/2)

	return(frame)
	
def mean_std(data_x, data_y): 
	#data_x: lista de listas con range(0,100) en la que faltan números intermedios
	#data_y: lista de listas con el valor de la función para cada x
	#Busca las x que faltan e interpola el valor de las y para cada lista
	#Genera una lista con las medias de los valores de data_y y otra con sus desviaciones típicas
    y_list_norm=[]
    for n,y in enumerate(data_y):
        y_norm=[]
        c=0
        k=0
        for j in np.arange(101):
            if c in data_x[n]:
                y_norm.append(y[k])
                k+=1
            else:
                y_norm.append(np.nan)
            c+=1
        y_norm=pd.Series(y_norm).interpolate(method='polynomial', order=2).tolist()
        y_list_norm.append(y_norm)
        
    mean=np.nanmean(np.array(y_list_norm), axis=0)
    std=np.nanstd(np.array(y_list_norm), axis=0)
    return(mean,std)