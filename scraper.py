import os
import sys
import glob
import getopt
import urllib.request
import re
import tempfile
import shutil
from PyPDF2 import PdfFileMerger
import random

# to do
# 1. merge pdfs into a single issue
# 2. better structure for folders

def error(msg=""):
	if msg != "":
		print("ERROR: ", msg)
		sys.exit(2)
		return None

def getPage(url, volume, issue):
	#link = url + str(volume) + "/" + str(issue)
	link = url
	current_dir = os.getcwd()
	title = ""

	print("Fetching magazine information: ", link)
	try:
		with urllib.request.urlopen(link) as response:
			page = response.read().decode('utf-8')

			if re.search(r'403 Forbidden', page):
				error("Could not access page: 403 Forbidden error.")
			else:
				return page
	except IOError as e:
		print('IOError getPage: ', e)
		pass
	except Exception as e:
		print('EXCError getPage', e)
		pass

	

def getChapters(page):
	chapters = []
	for match in re.finditer(r"/.*\.full\.pdf", page):
		chapterLink = "https://advances.sciencemag.org" + match.group(0)
		chapters.append(chapterLink)
	return chapters

# array of pdf paths
# to do later on
def merger(output, input_paths):
	merger = PdfFileMerger()
	with open(output, 'wb') as fh:
		writer.write(fh)

def getArchives(year):
	url = "https://advances.sciencemag.org"
	first = "/front-archive"
	with urllib.request.urlopen(url+first) as response:
		page = response.read().decode('utf-8')

	results = []
	for match in re.finditer(r"/content/[0-9]+/[0-9]+", page):
		results.append(match[0])

	results.sort()
	sset = set(results)
	print("Should download this: ", sorted(sset, key=len))


	a = len("/content/by/year/advances%3B2019")
	b = "/content/by/year/advances%3B2019"

	#a = len("/content/by/year/sci%3B2019")
	#b = "/content/by/year/sci%3B2019"

	#print(b[-4:]) #2019
	for x in range(0, 2019-year):
		years = []
		last = int(b[-4:])
		
		#for match in re.finditer(r"/content/by/year/sci.[A-Za-z0-9]+", page):
		for match in re.finditer(r"\/content\/(by)\/(year)\/(.*?\")", page):
			sd = match[0][:-1]
			temp = sd[-4:]

			if(a != len(sd)):
				pass
			elif(a == len(sd)):
				if(int(temp) < last):
					years.append(match[0][:-1]) #correct url
					#print("b before = ", b)
					b = match[0][-5:-1]
					#print("b after = ", b)
					#print("last = ", last)
					last = int(temp)
					#print("temp = ", temp)
				else:
					pass

		if(len(years) != 0):
			print("Going to: ", years[0], " now.\n") #/content/by/year/advances%3B2018
			
			with urllib.request.urlopen(url+years[0]) as response:
				page = response.read().decode('utf-8')

			results = []
			for match in re.finditer(r"/content/[0-9]+/[0-9]+", page):
				results.append(match[0])
			results.sort()

			tset = set(results)
			sset.update(tset)
		else:
			print("Nothing else, we're done!")
			return 0
	print("Total to download: ", sorted(sset, key=len))
	print("We're done with fetching list of content!")
	return sorted(sset, key=len)

def main():
	url_base = "https://advances.sciencemag.org"
	year = 2015
	archives = getArchives(year)
	numberOfVolumes = 0
	curdir = os.getcwd()
	#print("current dir = ", curdir)

	for x in archives:
		os.chdir(curdir)
		current_volume = x.split('/')[2]
		issue = x.split('/')[3]

		volumePath = "volume_" + str(current_volume)
		issuePath = "issue_" + str(issue)
		
		if(os.path.isdir(volumePath)):
			os.chdir(volumePath)
			if(os.path.isdir(issuePath)):
				try:
					pageTest = getPage(url_base+x, current_volume, issue)
					chptrs = getChapters(pageTest)
				except IOError as e:
					print('Error: ', e)
				except Exception as e:
						print('error')
						continue
				
				print("found ", len(chptrs), " articles!")
				for x in range(0, len(chptrs)):
					print("Downloading article: ", x, "/", len(chptrs))
					print(chptrs[x])
					exists = os.path.isfile(issuePath+"//ch_"+str(x)+".pdf")
					if exists:
						print("File already exists! Skipping")
						pass
					else:
						try:
							urllib.request.urlretrieve(chptrs[x], (issuePath+"//ch_"+str(x)+".pdf"))
						except IOError as e:
							print('Error: ', e)
							continue
						except Exception as e:
							print('Error', e)
							continue
				print("Completed!")
			else:
				os.mkdir(issuePath)
		else:
			os.mkdir(volumePath)
			os.chdir(volumePath)
			if(os.path.isdir(issuePath)):
				pass
			else:
				os.mkdir(issuePath)
			#print("created!\n")


		


if __name__ == '__main__':
	main()