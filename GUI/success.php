<!doctype html>
<html lang="de">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
	<link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
	<link rel="stylesheet" href="style.css" type="text/css">
	<link rel="stylesheet" href="material.min.css" type="text/css">
	<link rel="stylesheet" href="http://fonts.googleapis.com/css?family=Roboto:300,400,500,700" type="text/css">
	<script defer src="https://code.getmdl.io/1.3.0/material.min.js"></script>
    <title>Score Scan</title>
  </head>
  <body>
	<div id="header" style="width:100%; height:250px; background:#1e2426; position:absolute; z-index:1;">
	
		<div style="position:relative; float:left; color:white; margin-left:25%;">
		
			<h3>Der Musiknoten Scanner</h3>
			<p> 
			Lesen Sie Ihr PDF oder Bild ein. In wenigen Augenblicken steht Ihnen die MusicXML-Datei zum Download bereit.
			</p>
			
			
		</div>
	</div>
	<div id ="menue" style="width:10%; min-width:185px; height:500px; background:#e1dbd9; margin-left:5%; margin-top:10px; text-align: center; position:absolute; z-index:2;"> 
	
	<img src="Logo1.svg" alt="Logo" height="150px">
	
	<nav style="margin-top:40%;">
		<ul>
			<li><a class="mdl-navigation__link" href="" style='color:black; font-size: 16px; font-weight: bold;'>SPENDEN</a></li>
			<li><a class="mdl-navigation__link" href="" style='color:black; font-size: 16px; font-weight: bold;'>ÜBER UNS</a></li>
			<li><a class="mdl-navigation__link" href="" style='color:black; font-size: 16px; font-weight: bold;'>IMPRESSUM</a></li>
		</ul>
	</nav>
	</div>
	
	<div id="content" style="margin-top: 320px; margin-left: 25%; position:absolute; z-index:3;">
	
		<a href="fröhliche_weihnacht.xml" download>
			<button class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect">
				Datei herunterladen
			</button>
		</a>
		
	</div>
	
	<footer >
		<div style="width:100%; height:25%; bottom: 0; position:absolute; background-image:url(footer1.svg); background-size: 100% 100%;">
		
			
		</div>
	</footer>
  </body>
</html>