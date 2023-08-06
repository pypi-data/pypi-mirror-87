import json, codecs

def SaveDictToJson(directory,dict_marcha,dict_inc,dict_tec,dict_silla, dict_paso):
	#convierte los diccionarios en archivos json 
	with codecs.open(directory+'/data_info/marcha/tracking_results.json', 'w', 'utf8') as f:
		 f.write(json.dumps(dict_marcha, sort_keys = False, ensure_ascii=False))
	with codecs.open(directory+'/data_info/incorporacion/gettingup_results.json', 'w', 'utf8') as f:
		 f.write(json.dumps(dict_inc, sort_keys = False, ensure_ascii=False))
	with codecs.open(directory+'/data_info/tecnics_results.json', 'w', 'utf8') as f:
		 f.write(json.dumps(dict_tec, sort_keys = False, ensure_ascii=False))
	with codecs.open(directory+'/data_info/silla/silla_results.json', 'w', 'utf8') as f:
		 f.write(json.dumps(dict_silla, sort_keys = False, ensure_ascii=False))
	with codecs.open(directory+'/data_info/paso/gait_results.json', 'w', 'utf8') as f:
		 f.write(json.dumps(dict_paso, sort_keys = False, ensure_ascii=False))