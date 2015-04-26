import xml.etree.ElementTree as ET
tree = ET.parse('events.xml')
root = tree.getroot()

import re

file = open("data.csv", "w")

for i in range(len(root)):
	try:

		titulo = root[i][0][0].text
		if titulo is None:
			continue

		fecha = root[i][2][2][0].text
		if fecha is None:
			continue
		if fecha[0].isdigit():
			fecha = root[i][2][2][0].text
		else:
			fecha = root[i][2][2][1].text

		descripcion = root[i][3][0].text
		if descripcion is None:
			continue
		descripcion = re.sub(';', '', descripcion)

		url = root[i][4].attrib['url']

		print "Evento: %s\nFecha: %s\nDescripcion: %s\nurl: %s\n" % (titulo, fecha, descripcion, url)
		line = fecha + ";" + titulo + ";" + descripcion + ";" + url
		file.write(line+"\n")
	except:
		pass

