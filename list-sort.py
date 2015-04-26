import csv, random, datetime

# Read CSV file
reader = reader = csv.reader(open('data.csv', 'rU'), delimiter=';')
# Put the CSV info into a list
lista = list(reader)
# Sort the list by date (sort of...)
lista.sort()
# Delete the first error element of the list which is blank data
lista.pop(0)
#print lista[random.randint(0,len(lista)-1]
# Move all events 70 days
for i in range(len(lista)):
	try:
    	csvdate = datetime.datetime.strptime(lista[i][0],"%Y-%m-%dT%H:%M:%S")
	except ValueError:
    	csvdate = datetime.datetime.strptime(lista[i][0],"%Y-%m-%d")
	tempdate = csvdate - datetime.timedelta(days=70)
	print "Pasada: %s, nueva: %s" % (lista[i][0],tempdate.strftime('%d %b %Y'))
	lista[i][0] = tempdate.strftime('%d %b %Y')
