import io
from json2html import *
import json
import os

def HtmlGenerator(directory):
	#genera un archivo html con toda la informacion del test
	f = io.open(directory+'/data.html','w', encoding="utf-8")
	
	with open(directory+'/data_info/marcha/tracking_results.json') as data_file_tr:
		tr_rs = json.loads(data_file_tr.read())
	with open(directory+'/data_info/incorporacion/gettingup_results.json') as data_file_inc:
		inc_rs = json.loads(data_file_inc.read())
	with open(directory+'/data_info/tecnics_results.json') as data_file_tec:
		tec_rs = json.loads(data_file_tec.read())
	with open(directory+'/data_info/silla/silla_results.json') as data_file_silla:
		silla_rs = json.loads(data_file_silla.read())
	with open(directory+'/data_info/paso/gait_results.json') as data_file_paso:
		paso_rs = json.loads(data_file_paso.read())
		
	a=json2html.convert(json=tr_rs)
	b=json2html.convert(json=inc_rs)
	c=json2html.convert(json=silla_rs)
	d=json2html.convert(json=paso_rs)
	e=json2html.convert(json=tec_rs)

	
	message = """
	<html>
	<head>
	<title>Datos procesados</title>
	<p style="text-align:center;"><img src='"""+os.getcwd()+"""\\logo3.png' alt="Logo"></p>
	<br/><br/>
	<p style="text-align:center;"><img src="data_info\\fases.png" alt="fases"></p>
	<br/><br/><button class="accordion">DATOS SOBRE LA MARCHA ADELANTE</button>
	<div class="panel">
	<br/><br/>
	"""+a+"""<br>
		
	<input type="submit" id="Map" value="Mostrar graficas" onclick="showImg()"/>
	<input type="submit" id="Map" value="Ocultar graficas" onclick="hideImg()"/><br>
	
	<img id="map_img1" src="data_info\marcha\\vel_inst.png" style="display:;"/><br>
	<img id="map_img2" src="data_info\marcha\\shoulder_angles.png" style="display:;"/><br>
	<img id="map_img3" src="data_info\marcha\\knee_angles.png" style="display:;"/><br>
	<img id="map_img4" src="data_info\marcha\\spine_angles.png" style="display:;"/><br>
	<img id="map_img5" src="data_info\marcha\\elbow_mov.png" style="display:;"/><br>
	<br/><br/>
	</div>
	<button class="accordion">DATOS SOBRE LA INCORPORACION</button>
	<div class="panel">
	<br/><br/>
	"""+b+"""<br>
	<input type="submit" id="Map" value="Mostrar graficas" onclick="showImg1()"/>
	<input type="submit" id="Map" value="Ocultar graficas" onclick="hideImg1()"/><br>
	
	<img id="map_img11" src="data_info\incorporacion\\spine_legs_angles.png" style="display:;"/><br>
	<img id="map_img12" src="data_info\incorporacion\\spine_angles.png" style="display:;"/><br>
	<img id="map_img13" src="data_info\incorporacion\\knee_angles.png" style="display:;"/><br>
	<img id="map_img14" src="data_info\silla\\chair_inc.png" style="display:;"/><br>
	<br/><br/>
	</div>
	
	<button class="accordion">DATOS SOBRE LA SENTADA</button>
	
	<div class="panel">
	<br/><br/>
	"""+c+"""<br>
	<input type="submit" id="Map" value="Mostrar graficas" onclick="showImg2()"/>
	<input type="submit" id="Map" value="Ocultar graficas" onclick="hideImg2()"/><br>
	
	<img id="map_img15" src="data_info\silla\\knee_angles.png" style="display:;"/><br>
	<img id="map_img16" src="data_info\silla\\chair_sent.png" style="display:;"/><br>
	<br/><br/>
	
	</div>
	
	<button class="accordion">DATOS POR CICLO DE PIERNA</button>
	
	<div class="panel">
	<br/><br/>
	"""+d+"""<br>
	<input type="submit" id="Map" value="Mostrar graficas" onclick="showImg3()"/>
	<input type="submit" id="Map" value="Ocultar graficas" onclick="hideImg3()"/><br>
	
	<img id="map_img18" src="data_info\paso\\knee_angles_gait.png" style="display:;"/><br>
	<br/><br/><br/>
	<img id="map_img19" src="data_info\paso\\hip_angles_gait.png" style="display:;"/><br>
	<br/><br/>
	
	</div>
	
	<button class="accordion">DATOS TECNICOS</button>
	
	<div class="panel">
	<br/><br/>
	"""+e+"""<br>
		
	
	</div><br/><br/>
	
	<style>
	
	.accordion {
	
	  background-color: #eee;
	  color: #444;
	  cursor: pointer;
	  padding: 18px;
	  width: 100%;
	  border: none;
	  text-align: left;
	  outline: none;
	  font-size: 15px;
	  transition: 0.4s;
	  font-weight: bold;
	}
	
	.active,
	.accordion:hover {
	  background-color: #ccc;
	}
	
	.accordion:after {
	
	  content: "+";
	  color: #777;
	  font-weight: bold;
	  float: right;
	  margin-left: 5px;
	
	}
	.active:after {
	
	  content: "-";
	
	}
	
	.panel {
	
	  padding: 0 18px;
	  background-color: white;
	  max-height: 0;
	  overflow: hidden;
	  transition: max-height 0.2s ease-out;
	
	}
	
	table {
	  font-family: arial, sans-serif;
	  border-collapse: collapse;
	  width: 50%;
	}
	td, th {
	  border: 1px solid #dddddd;
	  text-align: left;
	  padding: 8px;
	}
	
	tr:nth-child(even) {
	  background-color: #dddddd;
	}
	</style>
	
	<script>
	
	var acc = document.getElementsByClassName("accordion");
	
	  var i;
	
	  for (i = 0; i < acc.length; i++) {
		acc[i].addEventListener("click", function() {
		  this.classList.toggle("active");
		  var panel = this.nextElementSibling;
		  if (panel.style.maxHeight) {
			panel.style.maxHeight = null;
		  } else {
			panel.style.maxHeight = panel.scrollHeight + "px";
		  }
		});
	  }
	
	function showImg() {
		document.getElementById("map_img1").style.display = "";
		document.getElementById("map_img2").style.display = "";
		document.getElementById("map_img3").style.display = "";
		document.getElementById("map_img4").style.display = "";
		document.getElementById("map_img5").style.display = "";
	}
	function hideImg() {
		document.getElementById("map_img1").style.display = "none";
		document.getElementById("map_img2").style.display = "none";
		document.getElementById("map_img3").style.display = "none";
		document.getElementById("map_img4").style.display = "none";
		document.getElementById("map_img5").style.display = "none";
	}
	 function showImg1() {
		document.getElementById("map_img11").style.display = "";
		document.getElementById("map_img12").style.display = "";
		document.getElementById("map_img13").style.display = "";
		document.getElementById("map_img14").style.display = "";
	}
	function hideImg1() {
		document.getElementById("map_img11").style.display = "none";
		document.getElementById("map_img12").style.display = "none";
		document.getElementById("map_img13").style.display = "none";
		document.getElementById("map_img14").style.display = "none";
	}
	function showImg2() {
		document.getElementById("map_img15").style.display = "";
		document.getElementById("map_img16").style.display = "";
	}
	function hideImg2() {
		document.getElementById("map_img15").style.display = "none";
		document.getElementById("map_img16").style.display = "none";
		document.getElementById("map_img17").style.display = "none";
	}
	function showImg3() {
		document.getElementById("map_img18").style.display = "";
		document.getElementById("map_img19").style.display = "";
	}
	function hideImg3() {
		document.getElementById("map_img18").style.display = "none";
		document.getElementById("map_img19").style.display = "none";
	}
	
	</script>
	</html>"""
	
	f.write(message)
	f.close()