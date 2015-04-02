import lxml.etree
import urllib


title = "List_of_best-selling_music_artists"
#title = "Jason Orange"
list = []
list2 = []
list3 = []
infoboxes = []
step = 0

params = { "format":"xml", "action":"query", "prop":"revisions", "rvprop":"timestamp|user|comment|content" }
params["titles"] = "API|%s" % urllib.quote(title.encode("utf8"))
qs = "&".join("%s=%s" % (k, v)  for k, v in params.items())
url = "http://en.wikipedia.org/w/api.php?%s" % qs
tree = lxml.etree.parse(urllib.urlopen(url))
revs = tree.xpath('//rev')

result = []
combo = ""

def insertIb(x):
	y = ""
	name = ""
	origin = ""
	type = ""
	bd = ""
	nw = ""
	bn = ""
	bp = ""
	ya = ""
	labels = []
	cm = []
	aa = []
	rel = []
	pm = []
	genres = []
	instruments = []
	genre = ""
	s = False
	help = 1
	num = 0
	title = ""
	th = False
	for n in range (0, 100):
		if x[n-7: n] == "Artist " or x[n-7: n] == "Person ":
			th = True
		if x[n] == ":":
			th = False
			break
		if th == True:
			title = title + x[n]
	for n in range(0, len(x)):
		if x[n-5: n] == "Name:":
			if name == "":
				num = 1
		if num == 1:
			if x[n] != " ":
				s = True
			if s == True:
				if x[n] == "\'":
					name = name
				elif x[n] == "\n" or x[n] == "<" or x[n: n+2] == " \n" or x[n] == "[":
					num = 0 
					s = False
				else:
					name = name + x[n]
		if x[n-5: n] == "Type:":
			if type == "":
				num = 5
		if num == 5:
			if x[n] != " ":
				s = True
			if s == True:
				if x[n] == "\n":
					num = 0 
					s = False
				else:
					type = type + x[n]
		if x[n-7: n] == "Origin:":
			num = 2
		if num == 2:
			if x[n] != " ":
				s = True
			if s == True:
				if x[n] == "\n" or x[n] == "|":
					num = 0 
					s = False
				else:
					origin = origin + x[n]
		if x[n-7: n] == "Genres:":
			num = 3
			y = ""
		if num == 3:
			if x[n] != " ":
				s = True
			if s == True:
				if x[n-1] == " " or x[n-1] == "|":
					y = y + x[n].upper()
				elif x[n-1: n+1] == ", ":
					y = ""
				elif x[n] == "\n":
					num = 0
					s = False
					if y != "":
						if y[:1] == " ":
							genres.append(y[1:])
						else:
							genres.append(y)
					y = ""
				elif x[n] == "|":
					y = ""
				elif x[n] == ",":
					if y[:1] == " ":
						genres.append(y[1:])
					else:
						genres.append(y)
				else:
					y = y + x[n]
		if x[n-12: n] == "Instruments:":
			num = 4
		if num == 4:
			if x[n] != " ":
				s = True
			if x[n: n+2] == " \n":
				num = 0
				s = False
				if y != "":
					if y[:1] == " ":
						instruments.append(y[1:])
					else:
						instruments.append(y)
			if s == True:
				if x[n-1] == " " or x[n-1] == "|":
					y = y + x[n].upper()
				elif x[n-1: n+1] == ", " or x[n] == "\'":
					y = ""
				elif x[n] == "\n":
					num = 0
					s = False
					if y != "":
						if y[:1] == " ":
							instruments.append(y[1:])
						else:
							instruments.append(y)
						y = ""
				elif x[n] == "|":
					y = ""
				elif x[n] == "," or x[n: n+2] == "  ":
					if y != "":
						if y[:1] == " ":
							instruments.append(y[1:])
						else:
							instruments.append(y)
						y = ""	
				else:
					y = y + x[n]
		if x[n-7: n] == "Labels:":
			num = 6
		if num == 6:
			if x[n] != " ":
				s = True
			if s == True:
				if x[n-1: n+1] == ", " or x[n-1: n+1] == ": ":
					y = ""
				elif x[n] == "\n":
					num = 0
					s = False
					if y != "":
						if y[:1] == " ":
							labels.append(y[1:])
							y = ""
							help = 1
						else:
							labels.append(y)
							y = ""
							help = 1
					help = 1
				elif x[n] == "|" or x[n] == "(" or x[n: n+2] == " (":
					help = 0
				elif x[n] == "," or x[n] == ")":
					if y[:1] == " ":
						labels.append(y[1:])
						y = ""
						help = 1
					else:
						labels.append(y)
						y = ""
						help = 1
				else:
					if help == 0:
						y = y
					else:
						y = y + x[n]
		if x[n-11: n] == "Birth Date:":
			num = 7
			dat= 0
			sec = 1
		if num == 7:
			if x[n] != " ":
				s = True
			if s == True:
				if x[n] == "\n" or sec == 3 and dat > 1:
					num = 0 
					s = False
				else:
					bd = bd + x[n]
					if x[n].isdigit():
						dat = dat + 1
					else:
						dat = 0
						sec = sec + 1
		if x[n-3: n] == "bn:":
			num = 8
		if num == 8:
			if x[n] != " ":
				s = True
			if s == True:
				if x[n] == "\n" or x[n+1] == "(":
					if bn[:1] == " ":
							bn = bn[1:]
					num = 0 
					s = False
				else:
					bn = bn + x[n]
		
		if x[n-13: n] == "Years Active:":
			num = 9
			dat= 0
			sec = 1
		if num == 9:
			if x[n] != " ":
				s = True
			if s == True:
				if x[n] == "\n":
					num = 0 
					s = False
					y = ""
				elif x[n] == "(":
					if ya[-1:] == " ":
						ya = ya[:-1]
					num = 0 
					s = False
					y = ""
				else:
					if dat > 3 and x[n].isdigit() or dat == 2 and x[n].isdigit() and x[n-2]=="0" and sec == 2:
						ya = ya + ", " + x[n]
						dat = 0
						sec = 1
					else:
						ya = ya + x[n]
						if x[n].isdigit():
							dat = dat + 1
						else:
							dat = 0
							sec = sec + 1
		if x[n-16: n] == "Current Members:":
			num = 10
		if num == 10:
			if x[n] != " ":
				s = True
			if s == True:
				if x[n-1: n+1] == ", " and x[n: n+4] != " Jr.":
					y = ""
				elif x[n] == "\n":
					num = 0
					s = False
					if len(y) > 1:
						cm.append(y)
						if y not in list2:
							list2.append(y)
				elif x[n] == "|" or x[n: n+4] == ":de:" or x[n].isdigit():
					help = 0
				elif x[n] == "," and x[n+1: n+5] != " Jr.":
					if y != "" or y != " ":
						cm.append(y)
						if y not in list2:
							list2.append(y)
						help = 1
						y = ""
					help = 1
				else:
					if help == 0:
						y = y
					else:
						y = y + x[n]
		if x[n-13: n] == "Past Members:":
			num = 11
		if num == 11:
			if x[n] != " ":
				s = True
			if s == True:
				if x[n-1: n+1] == ", " and x[n: n+4] != " Jr.":
					y = ""
				elif x[n] == "\n":
					num = 0
					s = False
					if y != "":
						pm.append(y)
						if y not in list2:
							list2.append(y)
						help = 1
						y = ""
					help = 1
				elif x[n] == "|" or x[n: n+4] == ":de:" or x[n].isdigit():
					help = 0
				elif x[n] == "," and x[n+1: n+5] != " Jr.":
					if y != "":
						pm.append(y)
						if y not in list2:
							list2.append(y)
						help = 1
						y = ""
					help = 1
				else:
					if help == 0:
						y = y
					else:
						y = y + x[n]
		if x[n-10: n] == "Religions:":
			num = 12
		if num == 12:
			if x[n] != " ":
				s = True
			if s == True:
				if x[n-1: n+1] == ", ":
					y = ""
				elif x[n] == "\n":
					num = 0
					s = False
					if len(y) > 1:
						rel.append(y)
					y = ""
				elif x[n] == ",":
					rel.append(y)
					y = ""
				elif x[n: n+2] != " \n":
					y = y + x[n]
		if x[n-12: n] == "Birth Place:":
			num = 13
		if num == 13:
			if x[n] != " ":
				s = True
			if s == True:
				if x[n] == "\n" or x[n] == "|":
					if bp[-1:] == " ":
						bp = bp[:-1]
					num = 0 
					s = False
				else:
					bp = bp + x[n]
		if x[n-10: n] == "Net Worth:":
			num = 14
		if num == 14:
			if x[n] != " ":
				s = True
			if s == True:
				if x[n: n+8] == " million" or x[n: n+8] == " billion":
					num = 0
					s = False
					nw = nw + "000000"
				elif not x[n].isdigit():
					nw = nw
				elif x[n] == "\n" or x[n] == "|":
					num = 0 
					s = False
				else:
					nw = nw + x[n]
		if x[n-16: n] == "Associated acts:":
			num = 15
		if num == 15:
			if x[n] != " ":
				s = True
			if s == True:
				if x[n-1: n+1] == ", ":
					y = ""
				elif x[n] == "\n":
					num = 0
					s = False
					if len(y) > 1:
						aa.append(y)
						if y not in list3:
							list3.append(y)
				elif x[n] == ",":
					aa.append(y)
					if y not in list3:
						list3.append(y)
					y = ""
				else:
					y = y + x[n]
	#print "----------TITLE: " + title	+ "-----------------"				
	
	if name != "":			
		#print  "name: " + name
		name = "\'" + name + "\'"
	else:
		name = "\'" + title + "\'"
	
	if bn != "":
		#print "bn: " + bn
		bn = "\'" + bn + "\'"
	else:
		bn = name	
	
	if bd != "":
		#print "bd: " + bd
		bd = "\'" + bd + "\'"
	else:
		bd = "NULL"
	
	if bp != "":
		#print "bp: " + bp
		bp = "\'" + bp + "\'"
	else:
		bp = "NULL"
		
	if origin != "":
		#print  "origin: " + origin
		origin = "\'" + origin + "\'"
	else:
		origin = bp
	
	if ya != "" and ya != "  ":
		#print "ya: " + ya
		ya = "\'" + ya + "\'"
	else:
		ya = "NULL"
		
	if nw != "":
		#print "nw: " + nw
		nw = "\'" + nw + "\'"
	else:
		nw = "NULL"
		
	print "INSERT IGNORE INTO artist VALUES("+name+","+nw+","+origin+","+ya+");"
	
	if type != "group_or_band":
		print "INSERT IGNORE INTO person (name, dob, pob) VALUES ("+bn+","+bd+","+bp+");"
		print "INSERT IGNORE INTO musician (personId, artistId) VALUES ("+bn+","+name+");"	
	
	if type == "group_or_band":
		print "INSERT IGNORE INTO band VALUES("+name+");"
		
	for n in range (0, len(cm)):
		print "INSERT IGNORE INTO currentmembers VALUES ("+name+",\'"+cm[n]+"\');"
	
	for n in range (0, len(pm)):
		print "INSERT IGNORE INTO pastmembers VALUES ("+name+",\'"+pm[n]+"\');"
		
	for n in range (0, len(genres)):
		if genres[n] != "See Below)" and genres[n][1:] != "\n":
			print "INSERT IGNORE INTO artistgenre VALUES ("+name+",\'"+genres[n]+"\');"
			print "INSERT IGNORE INTO genre VALUES (\'"+genres[n]+"\');"
	
	for n in range (0, len(instruments)):
		if instruments[n][4:] != "Url=":
			print "INSERT IGNORE INTO artistinstrument VALUES ("+name+",\'"+instruments[n]+"\');"
			print "INSERT IGNORE INTO instrument VALUES (\'"+instruments[n]+"\');"
	
	for n in range (0, len(labels)):
		print "INSERT IGNORE INTO artistlabel VALUES ("+name+",\'"+labels[n]+"\');"
		print "INSERT IGNORE INTO recordlabel VALUES (\'"+labels[n]+"\');"
	
	
		
#----------------------------------------------------------------------------------------	
		


def simpleArtist(x):
	num = 0
	y = ""
	f = ""
	include = False
	start = False
	seen1 = False
	for n in range(0, len(x)):
			if x[n: n+6] == "| name" or x[n: n+5] == "|name":
				if seen1 == True:
					num = 0
				else:	
					num = 1
					y = y + "Name: " 
			if num == 1 and seen1 == False:
				if x[n: n+2] == "{{":
					start = False
				if x[n-1] == "=":
					start = True
				if start == True:
					y = y + x[n]
				if x[n + 2] == "|" or x[n] == "\n" or x[n+1: n+4] == "}}\n":
					start = False
					y = y + "\n"
					seen1 = True
					num = 0
					
			if x[n: n+12] == "| background" or x[n: n+11] == "|background":
				num = 2
				y = y + "Type: "
			if num == 2:
				if x[n-1] == "=":
					start = True
				if start == True:
					y = y + x[n]
				if x[n + 2] == "|" or x[n] == "\n" or x[n+1: n+4] == "}}\n":
					start = False
					y = y + "\n"
					num = 0
					
			if x[n: n+8] == "| origin" or x[n: n+7] == "|origin":
				num = 3
				y = y + "Origin: "
			if num == 3:
				if x[n-1] == "=":
					start = True				
				if start == True:
					if x[n] == "[" or x[n] == "]" or x[n] == "{" or x[n] == "}":
						y = y
					else:
						y = y + x[n]
				if x[n+2:n+4] == "| " or x[n] == "\n" or x[n+1:n+5] == "http":
					start = False
					y = y + "\n"
					num = 0
					
			if x[n: n+7] == "| genre" or x[n: n+6] == "|genre":
				num = 4
				y = y + "Genres: "
			if num == 4:
				if x[n-1] == "=":
					start = True		
				if start == True:
					if x[n] == "[" or x[n] == "]" or x[n] == "\n" or x[n] == "{" or x[n] == "}":
						if x[n: n+2] != "][":
							y = y
						else:
							y = y + ", "
					elif x[n] == "*":
						y = y + ", "
					else:
						y = y + x[n]
				if x[n + 1 : n+3] == "\n|" or x[n + 1 : n+4] == "\n |"or x[n] == "}" or x[n+1: n+7] == "{{cite" or x[n+1].isdigit() or x[n+1: n+5] == "http":
					start = False
					y = y + "\n"
					num = 0
					
			if x[n: n+14] == "| years_active" or x[n: n+13] == "|years_active":
				num = 5
				y = y + "Years Active: "
			if num == 5:
				if x[n-1] == "=":
					start = True				
				if start == True:
					if x[n] == "[" or x[n] == "]" or x[n] == "{" or x[n] == "}" or x[n] == "\n":
						y = y
					else:
						y = y + x[n]
				if x[n + 1 : n+3] == "\n|" or x[n +1: n+4] == "\n |" or x[n+1: n+5] == "cite" or x[n+1: n+5] == "http" or x[n + 1 : n+3] == "| " :
					start = False
					y = y + "\n"
					num = 0
					
			if x[n: n+7] == "| label" or x[n: n+6] == "|label":
				num = 6
				y = y + "Labels: "
			if num == 6:
				if x[n-1] == "=":
					start = True				
				if start == True:
					if x[n] == "[" or x[n] == "]" or x[n] == "\n" or x[n] == "{" or x[n] == "}" or x[n] == "/":
						if x[n-2: n] == "]]" or x[n: n+3] == "/[[":
							y = y + ", "
						else:
							y = y 
					elif x[n] == "*":
						y = y + ", "
					else:
						y = y + x[n]
				if x[n] == "}" or x[n + 1 : n+3] == "\n|" or x[n +1: n+4] == "\n |" or x[n+1: n+5] == "cite" or x[n+1: n+5] == "http" or x[n+1: n+4] == "]\n ":
					start = False
					y = y + "\n"
					num = 0
					
			if x[n: n+17] == "| current_members" or x[n: n+16] == "|current_members":
				num = 7
				y = y + "Current Members: "
			if num == 7:
				if x[n-2: n] == "[[":
					start = True
				if x[n: n+2] == "]]":
					y = y + ", "
					start = False
				if start == True:
					y = y + x[n]
				if x[n+2:n+4] == "| " or x[n] == "\n":
					start = False
					y = y + "\n"
					num = 0
					
			if x[n: n+14] == "| past_members" or x[n: n+13] == "|past_members":
				num = 8
				y = y + "Past Members: "
			if num == 8:
				if x[n-2: n] == "[[":
					if x[n] != "#":
						start = True
				if x[n: n+2] == "]]":
					y = y + ", "
					start = False				
				if start == True:
					if x[n] == "[" or x[n] == "]" or x[n] == "\n" or x[n] == "{" or x[n] == "}":
						if x[n-1: n+1] == "][":
							y = y + ", "
						else:
							y = y
					elif x[n] == "*":
						y = y + ", "
					else:
						y = y + x[n]
				if x[n] == "}" or x[n + 1 : n+3] == "\n|" or x[n +1: n+4] == "\n |" or x[n+1: n+5] == "cite" or x[n+1: n+4] == "See":
					start = False
					y = y + "\n"
					num = 0
					
					
			if x[n: n+12] == "| instrument" or x[n: n+12] == "|instrument ":
				num = 9
				y = y + "Instruments: "
			if num == 9:
				if x[n-1] == "=":
					start = True				
				if start == True:
					if x[n] == "[" or x[n] == "]" or x[n] == "\n" or x[n] == "{" or x[n] == "}":
						if x[n: n+2] != "][":
							y = y
						else:
							y = y + ", "
					elif x[n] == "*":
						y = y + ", "
					else:
						y = y + x[n]
				if x[n+1:n+3] == "\n|" or x[n] == "}" or x[n: n+3] == " | ":
					start = False
					y = y + "\n"
					num = 0
					
			if x[n: n+12] == "| birth_name" or x[n: n+11] == "|birth_name":
				num = 10
				y = y + "bn:"
			if num == 10:
				if x[n-1] == "=":
					start = True				
				if start == True:
					if x[n] == "[" or x[n] == "]" or x[n] == "\n" or x[n] == "{" or x[n] == "}":
						y = y
					elif x[n] == "*":
						y = y + ", "
					else:
						y = y + x[n]
				if x[n+2:n+4] == "| " or x[n] == "\n" or x[n+1: n+5] == "cite" or x[n+1: n+5] == "http" :
					start = False
					y = y + "\n"
					num = 0
					
			if x[n: n+12] == "| birth_date" or x[n: n+11] == "|birth_date":
				num = 11
				y = y + "Birth Date: "
			if num == 11:
				if x[n] == "|" and x[n+5] == "|":
					start = True				
				if start == True:
					if x[n] == "|":
						y = y + "-"
					elif x[n].isdigit(): 
						y = y + x[n]
					else:
						y = y
				if x[n+2:n+4] == "| " or x[n] == "\n" or x[n+1: n+7] == "{{cite":
					start = False
					y = y + "\n"
					num = 0
			
			if x[n: n+13] == "| birth_place" or x[n: n+12] == "|birth_place":
				num = 12
				y = y + "Birth Place: "
			if num == 12:
				if x[n-1] == "=":
					start = True				
				if start == True:
					if x[n-2: n] == "]]" and x[n] != ",":
						y = y + ", "
					if x[n] == "[" or x[n] == "]" or x[n] == "\n" or x[n] == "{" or x[n] == "}" or x[n-1: n+1] == "  ":
						y = y
					elif x[n] == "*":
						y = y + ", "
					else:
						y = y + x[n]
				if x[n+2:n+4] == "| " or x[n] == "\n" or x[n+1: n+12] == "Conflicting" or x[n+1:n+5] == "cite":
					start = False
					y = y + "\n"
					num = 0
			if x[n: n+11] == "| net_worth" or x[n: n+10] == "|net_worth":
				num = 13
				y = y + "Net Worth: "
			if num == 13:
				if x[n-1] == "=":
					start = True				
				if start == True:
					if x[n-2: n] == "]]" and x[n] != ",":
						y = y + ", "
					if x[n] == "[" or x[n] == "]" or x[n] == "\n" or x[n] == "{" or x[n] == "}":
						y = y
					elif x[n] == "*":
						y = y + ", "
					else:
						y = y + x[n]
				if x[n+2:n+4] == "| " or x[n] == "\n" or x[n+1] == "(" or x[n+1: n+3] == " (":
					start = False 
					y = y + "\n"
					num = 0
			if x[n: n+17] == "| associated_acts" or x[n: n+16] == "|associated_acts":
				num = 14
				y = y + "Associated acts: "
			if num == 14:
				if x[n-2: n] == "[[":
					if x[n] != "#":
						start = True
				if x[n: n+2] == "]]":
					y = y + ", "
					start = False				
				if start == True:
					if x[n] == "[" or x[n] == "]" or x[n] == "\n" or x[n] == "{" or x[n] == "}":
						if x[n-1: n+1] == "][":
							y = y + ", "
						else:
							y = y
					elif x[n] == "*":
						y = y + ", "
					else:
						y = y + x[n]
				if x[n] == "}" or x[n + 1 : n+3] == "\n|" or x[n +1: n+4] == "\n |" or x[n+1: n+5] == "cite" or x[n+1: n+4] == "See" :
					start = False
					y = y + "\n"
					num = 0
			
					
	for n in range(0, len(y)):
		if y[n-11: n] == "flat list|," or y[n-11: n] == "Flat list|," or y[n-11: n] == "Flat list |" or y[n-11: n] == "flatlist| ," or y[n-12: n] == "Flat list| ," or y[n-12: n] == "flat list |,":
			f = f[:-12] 
		if y[n-10: n] == "flatlist|," or y[n-10: n] == "Flatlist|,":
			f = f[:-11]
		if y[n-15: n] == "Unbulleted list":
			f = f[:-15]
		if y[n-5: n] == "hlist":
			f = f[:-6]
		if y[n-7: n] == "nowrap|":
			f = f[:-7]
		if y[n: n+3] == ", \n":
			f = f
		if y[n] == "\'":
			f = f + "\'"
		if y[n-6: n] == "&nbsp;":
			f = f[:-6] + " "
		if y[n-7: n] == "&ndash;":
			f = f[:-7] + "-"
		if y[n-11: n] == "start date|" or y[n-11: n] == "Start date|":
			f = f[:-11]
		if y[n-9: n] == "end date|" or y[n-9: n] == "End date|":
			f = f[:-9] + "-"
		if y[n-10: n] == " in music|":
			f = f[:-10] + "-"
		if y[n-2: n] == "\n\n":
			f = f[:-1]
		if y[n: n + 2] == "  ":
			f = f
		if y[n] == "-":
			if y[n-1] == " " or y[n+1] == " " or y[n+1] == "\n":
				f = f
			else:
				f = f + y[n]
		else:
			f = f + y[n]
	
	f = "InfoBox Musicial Artist " + title + ":\n" + f
	result.append(f)
	
#TO MAKE A PERSON INFOBOX READABLE-------------------------------------------------------	
	
def simplePerson(x):
	num = 0
	y = ""
	f = ""
	include = False
	start = False
	for n in range(0, len(x)):
			if x[n: n+6] == "| name" or x[n: n+5] == "|name":
				num = 1
				y = y + "Name: " 
			if num == 1:
				if x[n-1] == "=":
					start = True
				if start == True:
					y = y + x[n]
				if x[n + 2] == "|" or x[n] == "\n":
					start = False
					y = y + "\n"
					num = 0
					
			if x[n: n+10] == "| religion" or x[n: n+9] == "|religion":
				num = 2
				y = y + "Religions: "
			if num == 2:
				if x[n-1] == "=":
					start = True
				if start == True:
					if x[n] == "[" or x[n] == "]" or x[n] == "\n" or x[n] == "{" or x[n] == "}":
						if x[n-1: n+1] == "][":
							y = y + ", "
						else:
							y = y
					elif x[n] == "*":
						y = y + ", "
					else:
						y = y + x[n]
				if  x[n] == "\n":
					start = False
					y = y + "\n"
					num = 0
					
			if x[n: n+11] == "| home_town" or x[n: n+10] == "|home_town":
				num = 3
				y = y + "Home Town: "
			if num == 3:
				if x[n-1] == "=":
					start = True				
				if start == True:
					if x[n] == "[" or x[n] == "]" or x[n] == "{" or x[n] == "}":
						y = y
					else:
						y = y + x[n]
				if x[n+2:n+4] == "| " or x[n] == "\n":
					start = False
					y = y + "\n"
					num = 0
			if x[n: n+14] == "| years_active" or x[n: n+13] == "|years_active":
				num = 5
				y = y + "Years Active: "
			if num == 5:
				if x[n-1] == "=":
					start = True				
				if start == True:
					if x[n] == "[" or x[n] == "]" or x[n] == "{" or x[n] == "}" or x[n] == "\n":
						y = y
					else:
						y = y + x[n]
				if x[n+1] == "\n" or x[n +1: n+4] == "\n |" or x[n+1: n+5] == "cite" or x[n+1: n+5] == "http" or x[n + 1 : n+3] == "| " :
					start = False
					y = y + "\n"
					num = 0
					
			if x[n: n+12] == "| birth_name" or x[n: n+11] == "|birth_name":
				num = 10
				y = y + "bn: "
			if num == 10:
				if x[n-1] == "=":
					start = True				
				if start == True:
					if x[n] == "[" or x[n] == "]" or x[n] == "\n" or x[n] == "{" or x[n] == "}":
						y = y
					elif x[n] == "*":
						y = y + ", "
					else:
						y = y + x[n]
				if x[n+2:n+4] == "| " or x[n] == "\n" or x[n+1: n+7] == "{{cite" or x[n +1: n+5] == "http":
					start = False
					y = y + "\n"
					num = 0
					
			if x[n: n+12] == "| birth_date" or x[n: n+11] == "|birth_date":
				num = 11
				y = y + "Birth Date: "
			if num == 11:
				if x[n] == "|" and x[n+5] == "|":
					start = True				
				if start == True:
					if x[n] == "|":
						y = y + "-"
					elif x[n].isdigit(): 
						y = y + x[n]
					else:
						y = y
				if x[n+2:n+4] == "| " or x[n] == "\n" or x[n+1: n+7] == "{{cite":
					start = False
					y = y + "\n"
					num = 0
			
			if x[n: n+13] == "| birth_place" or x[n: n+12] == "|birth_place":
				num = 12
				y = y + "Birth Place: "
			if num == 12:
				if x[n-2] == "=":
					start = True				
				if start == True:
					if x[n] == "[" or x[n] == "]" or x[n] == "\n" or x[n] == "{" or x[n] == "}" :
						y = y
					elif x[n] == "*":
						y = y + ", "
					else:
						y = y + x[n]
				if x[n+2:n+4] == "| " or x[n] == "\n" or x[n+1: n+5] == "cite" or x[n+1: n+5] == "<ref":
					start = False
					y = y + "\n"
					num = 0
			if x[n: n+11] == "| net_worth" or x[n: n+10] == "|net_worth":
				num = 13
				y = y + "Net Worth: "
			if num == 13:
				if x[n-1] == "=":
					start = True				
				if start == True:
					if x[n-2: n] == "]]" and x[n] != ",":
						y = y + ", "
					if x[n] == "[" or x[n] == "]" or x[n] == "\n" or x[n] == "{" or x[n] == "}":
						y = y
					elif x[n] == "*":
						y = y + ", "
					else:
						y = y + x[n]
				if x[n+2:n+4] == "| " or x[n] == "\n" or x[n+1: n+3] == " (":
					start = False 
					y = y + "\n"
					num = 0
			if x[n: n+17] == "| associated_acts" or x[n: n+16] == "|associated_acts":
				num = 14
				y = y + "Associated acts: "
			if num == 14:
				if x[n-2: n] == "[[":
					if x[n] != "#":
						start = True
				if x[n: n+2] == "]]":
					y = y + ", "
					start = False				
				if start == True:
					if x[n] == "[" or x[n] == "]" or x[n] == "\n" or x[n] == "{" or x[n] == "}":
						if x[n-1: n+1] == "][":
							y = y + ", "
						else:
							y = y
					elif x[n] == "*":
						y = y + ", "
					else:
						y = y + x[n]
				if x[n] == "}" or x[n + 1 : n+3] == "\n|" or x[n +1: n+4] == "\n |" or x[n+1: n+5] == "cite" or x[n+1: n+4] == "See" :
					start = False
					y = y + "\n"
					num = 0
			
					
	for n in range(0, len(y)):
		if y[n-11: n] == "flat list|," or y[n-11: n] == "Flat list|," or y[n-11: n] == "flatlist| ,":
			f = f[:-12]
		if y[n-10: n] == "flatlist|," or y[n-10: n] == "Flatlist|,":
			f = f[:-11]
		if y[n-7: n] == "nowrap|":
			f = f[:-7]
		if y[n-6: n] == "&nbsp;":
			f = f[:-6] + " "
		if y[n-7: n] == "&ndash;":
			f = f[:-7] + "-"
		if y[n-7: n] == "<small>":
			f = f[:-7] + ", "
		if y[n: n+3] == ", \n":
			f = f
		if y[n] == "\'":
			f = f + "\'"
		if y[n-2: n] == "\n\n":
			f = f[:-1]
		if y[n: n+2] == "  ":
			f = f
		if y[n] == "-":
			if y[n-1] == " " or y[n+1] == " " or y[n+1] == "\n":
				f = f
			else:
				f = f + y[n]
		else:
			f = f + y[n]
	
	f = "InfoBox Person " + title + ":\n" + f
	result.append(f)
	
				
		
	
		
			
#To get the info boxes of a page--------------------------------------------------------			
										
def getInfoBox(x):
	y = ""
	help = 0
	z = False
	include = True
	for n in range(0, len(x)):
		if x[n: n+8] == "| module" or x[n: n+7] == "|module":
		    if x[help: help + 6] == "person":
		    	simplePerson(y)
		    	y = ""
		    	include = True
		if x[n: n+9] == "{{Infobox":
		    help = n + 10
		    z = True
		if z == True:
			if x[n: n+3] == "\'\'\'" and x[n-1] == "\n":
					z = False
					if x[help: help + 14] == "musical artist":
						simpleArtist(y)
						break
					else:
						#print "not a music artist"
						break
			
			else:
				if x[n] == "<":
					include = False	
				if x[n-1] == ">":
					include = True
				if include == True:
					y = y + x[n]

def getTitles(x):
	title = ""
	write = False
	for n in range(0, len(x)):
		if x[n -5: n] == " | [[":
			write = True
		if write == True and x[n] == "|":
			write = False
			list.append(title)
			title = ""
		if write== True and x[n: n+2] == "]]":
			write = False
			list.append(title)
			title = ""
		if write == True: 
			title = title + x[n]
			

getTitles(revs[-1].text)
#print list
for n in range (0, len(list)):
	step = n
	title = list[n]
	params["titles"] = "API|%s" % urllib.quote(title.encode("utf8"))
	qs = "&".join("%s=%s" % (k, v)  for k, v in params.items())
	url = "http://en.wikipedia.org/w/api.php?%s" % qs
	tree = lxml.etree.parse(urllib.urlopen(url))
	revs = tree.xpath('//rev') 
	getInfoBox(revs[-1].text)
	for x in range (0, len(result)):
		combo = combo + result[x]
	infoboxes.append(combo)
	combo = ""
	result = []	
	print "#building IBs 1--- " + str(n) + "/" + str(len(list))
	
	
for n in range (0, len(infoboxes)):
	if len(infoboxes[n]) > 10:
		insertIb(infoboxes[n])
		
infoboxes = []

#print list3
for n in range (0, len(list3)):
	title = list3[n]
	params["titles"] = "API|%s" % urllib.quote(title.encode("utf8"))
	qs = "&".join("%s=%s" % (k, v)  for k, v in params.items())
	url = "http://en.wikipedia.org/w/api.php?%s" % qs
	tree = lxml.etree.parse(urllib.urlopen(url))
	revs = tree.xpath('//rev') 
	getInfoBox(revs[-1].text)
	for x in range (0, len(result)):
		combo = combo + result[x]
	if combo != "":
		infoboxes.append(combo)
	combo = ""
	result = []	
	print "#building IBs 2--- " + str(n) + "/" + str(len(list3))
	
for n in range (0, len(infoboxes)):
	if len(infoboxes[n]) > 10:
		insertIb(infoboxes[n])
		
infoboxes = []
#print list2
for n in range (0, len(list2)):
	title = list2[n]
	params["titles"] = "API|%s" % urllib.quote(title.encode("utf8"))
	qs = "&".join("%s=%s" % (k, v)  for k, v in params.items())
	url = "http://en.wikipedia.org/w/api.php?%s" % qs
	tree = lxml.etree.parse(urllib.urlopen(url))
	revs = tree.xpath('//rev') 
	getInfoBox(revs[-1].text)
	for x in range (0, len(result)):
		combo = combo + result[x]
	if combo != "":
		infoboxes.append(combo)
	combo = ""
	result = []	
	print "#building IBs 3--- " + str(n) + "/" + str(len(list2))
	
for n in range (0, len(infoboxes)):
	if len(infoboxes[n]) > 10:
		insertIb(infoboxes[n])
		

#-----For Testing-------
#print revs[-1].text
#getInfoBox(revs[-1].text)
#for n in range (0, len(result)):
#	combo = combo + result[n]
#print combo	
#insertIb(combo)
