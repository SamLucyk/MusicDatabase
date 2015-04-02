import lxml.etree
import urllib

title = "List_of_best-selling_music_artists"
#title = "Dave Matthews Band"

otitle = ""
tlist=[]
list = []
infoboxes = []
step = 0

params = { "format":"xml", "action":"query", "prop":"revisions", "rvprop":"timestamp|user|comment|content" }
params["titles"] = "API|%s" % urllib.quote(title.encode("utf8"))
qs = "&".join("%s=%s" % (k, v)  for k, v in params.items())
url = "http://en.wikipedia.org/w/api.php?%s" % qs
tree = lxml.etree.parse(urllib.urlopen(url))
revs = tree.xpath('//rev')

				
def getTracks(x):
	y = ""
	art = ""
	result = ""
	trks = []
	tnum = 1
	a = False
	z = False
	strt = False
	s = False
	lngth = False
	ttle = False
	include = False
	for n in range(0, len(x)):
		if x[n: n+8] == "| Artist" and art == "" or x[n: n+8] == "| artist" and art == "" or x[n: n+13] == "Artist      =" and art == "" or x[n: n+13] == "artist      =" and art == "":
			a = True
		if a == True:
			if x[n-2: n] == "[[":
				include = True
			if x [n: n+2] == "]]":
				include = False
				a = False
			if include == True:
				art = art + x[n]
				
		if x[n: n+17] == "==Track listing==" or x[n: n+17] == "==Track Listing==":
			z = True
		if z == True:
			if x[n-7: n] == "| title" or x[n-2: n] == "#\"" or x[n-6:n] == "|title":
				include = True
				ttle = True	
				s = True
				y = art + "--->" + title + "--->"	
			if x[n-8: n] == "| length" or x[n-7: n] == "|length":
				include = True
				lngth = True					
			if include == True:
				if x[n-2: n] == "= " or x[n-1] == "=" or x[n-2: n] == "#\"" or x[n].isdigit() and x[n+1] == ":":
					strt = True
				if strt == True and lngth == False and ttle == True:
					if 	x[n] == "\n" or x[n] == "\"" or x[n: n+5] == "<ref>" or x[n] == "#" or x[n] == "|":
						include = False
						strt = False
						y = y + "--->"
					elif not x[n] == "[" or not x[n] == "]":
						y = y + x[n]
				if lngth == True and strt == True and ttle == True:
					if 	x[n] == "\n" or x[n: n+5] == "<ref>" or x[n] == "#":
						include = False
						lngth = False
						ttle = False
						strt = False
						y = y + "--->" + str(tnum)
						trks.append(y)
						tnum = tnum + 1
						y = ""
					elif not x[n] == "[" or not x[n] == "]":
						y = y + x[n]
			if x[n: n+4] == "}}\n\n" and s == True or x[n: n+4] == "#" and s == True :
				for n in range(0, len(trks)):
					#print trks[n]
					result = result + trks[n] + "\n"
				break
	now = ""
	one = []
	all = []
	p = 0
	#print result
	for n in range (0, len(result)):
		if p == 0:
			if result[n: n+4] == "--->":
				p = 3
				one.append(now)
				now = ""
			elif result[n] == "\n":
				one.append(now)
				all.append(one)
				now = ""
				one = []
			elif now == "" and result[n] == " ":
				now = now
			else:
				now = now + result[n]
		else:
			p = p - 1
	for n in range (0, len(all)):
		if all[n]: 
			art = all[n][0]
			artist = ""
			for n1 in range (0, len(art)):
				if art[n1] == "\'":
					artist = artist + art[n1] + "\'"
				else:
					artist = artist + art[n1]
					
			alb = all[n][1]
			album = ""
			for n2 in range (0, len(alb)):
				if alb[n2] == "\'":
					album = album + alb[n2] + "\'"
				else: 
					album = album + alb[n2]
					
			son = all[n][2]
			song = ""
			for n3 in range (0, len(son)):
				if son[n3] == "\'":
					song = song + son[n3] + "\'"
				else: 
					song = song + son[n3]
			if song[-2:] == "]]":
				song = song[:-2]
			if song[:2] == "[[":
				song = song[2:]
				
			leng = all[n][3]
			length = ""
			for n4 in range (0, len(leng)):
				if leng[n4] == " ":
					length = length
				else: 
					length = length + leng[n4]
			
			tn = all[n][4]
			if n == 0:
				print "INSERT IGNORE INTO artistalbum VALUES (\'"+artist+"\',\'"+album+"\');"
			print "INSERT IGNORE INTO song VALUES (\'"+song+"\',\'"+album+"\',\'"+length+"\',"+str(tn)+");"
			if n == len(all) - 1:
				print "INSERT IGNORE INTO album (albumId, trackNum) VALUES (\'"+album+"\',"+ tn +");"


def getAlbums(x):
	y = ""
	res = ""
	z = False
	s = False
	include = False
	for n in range(0, len(x)):
		if x[n: n+15] == "==Discography==" or x[n: n+16] == "== Discography==":
			#print "\n" + "-------" + title + "\'s Discography-----"
			z = True
		if z == True:
			if x[n-4: n] == "* \'\'" or x[n-3: n] == "*\'\'":
				include = True	
				s = True				
			if include == True:
				if x[n: n+2] == "\'\'":
					include = False
					for n in range(0, len(y)):
						if y[n] == "]" or y[n] == "[":
							res = res
						else:
							res = res + y[n]
					list.append(res)
					y = ""
					res = ""
				else:	
					y = y + x[n]
			if x[n: n+2] == "\n\n" and s == True:
				break
				
def getRedirect(x):
	start = False
	for n in range (0, len(x)):
		if x[n-2:n] == "[[":
			start = True
			title = ""
		if x[n] == "]":
			break
		if start == True:
			title = title + x[n]
	params["titles"] = "API|%s" % urllib.quote(title.encode("utf8"))
	qs = "&".join("%s=%s" % (k, v)  for k, v in params.items())
	url = "http://en.wikipedia.org/w/api.php?%s" % qs
	tree = lxml.etree.parse(urllib.urlopen(url))
	revs = tree.xpath('//rev') 
	getTracks(revs[-1].text)
	

def getTitles(x):
	title = ""
	write = False
	for n in range(0, len(x)):
		if x[n -5: n] == " | [[":
			write = True
		if write == True and x[n] == "|":
			write = False
			tlist.append(title)
			title = ""
		if write== True and x[n: n+2] == "]]":
			write = False
			tlist.append(title)
			title = ""
		if write == True: 
			title = title + x[n]
		
		

getTitles(revs[-1].text)
#print tlist

for n in range (0, len(tlist)):
	title = tlist[n]
	params["titles"] = "API|%s" % urllib.quote(title.encode("utf8"))
	qs = "&".join("%s=%s" % (k, v)  for k, v in params.items())
	url = "http://en.wikipedia.org/w/api.php?%s" % qs
	tree = lxml.etree.parse(urllib.urlopen(url))
	revs = tree.xpath('//rev') 
	getAlbums(revs[-1].text)

#print list

for n in range (0, len(list)):
	title = list[n]
	params["titles"] = "API|%s" % urllib.quote(title.encode("utf8"))
	qs = "&".join("%s=%s" % (k, v)  for k, v in params.items())
	url = "http://en.wikipedia.org/w/api.php?%s" % qs
	tree = lxml.etree.parse(urllib.urlopen(url))
	revs = tree.xpath('//rev') 
	if revs[-1].text[0:9] == "#REDIRECT":
		getRedirect(revs[-1].text)
	else:
		getTracks(revs[-1].text)
	
		

		
#-----For Testing-------
#print revs[-1].text
#getInfoBox(revs[-1].text)
#getTracks(revs[-1].text, title)
#for n in range (0, len(result)):
#	combo = combo + result[n]
#print combo	
#insertIb(combo)
