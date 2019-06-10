import urllib.request
import os
import re
from pdb import set_trace as bp
import pysnooper
class Tools(object):
	def get_archives(root_url, from_year):
		#print("Downloading from: ",root_url,"\n2019 -", from_year)
		full_url = root_url + "/content/by/year/"
		print(full_url)
		with urllib.request.urlopen(full_url) as response:
			page = response.read().decode('utf-8')
		results = set()
		for match in re.finditer(r"/content/[0-9]+/[0-9]+", page):
			results.add(match[0])

		parent_url = "/content/by/year/advances%3B2019"
		path_length = len(parent_url)
		last = int(parent_url.split('%3B')[1])

		for x in range(0, 2019-from_year):
			years = []

			for match in re.finditer(r"\/content\/(by)\/(year)\/(.*?\")", page):
				advances_year = match[0][:-1]
				next_year = advances_year[-4:]

				if(path_length == len(advances_year)):
					if(int(next_year) < last):
						years.append(advances_year)
						last = int(next_year)
					else:
						pass
			if(years):
				print("Going to:", years[0], "now.\n")
				with urllib.request.urlopen(root_url+years[0]) as response:
					page = response.read().decode('utf-8')
				for match in re.finditer(r"/content/[0-9]+/[0-9]+", page):
					results.add(match[0])

			else:
				print("We're done!")
				results = sorted(results, key = lambda x: (int(x.split('/')[2]), int(x.split('/')[3])))
				print(results)
				break;

		return results

	def get_page(_url, volume, issue):
		url = _url
		current_dir = os.getcwd()
		title = ""

		print("Fetching magazine information: ", url)
		try:
			with urllib.request.urlopen(url) as response:
				page = response.read().decode('utf-8')
				if re.search(r'403 Forbidden', page):
					error("Could not access page: 403 Forbidden error.")
				else:
					return page
		except IOError as e:
			print("IOError getPage", e)
			pass
		except Exception as e:
			print("Exception getPage", e)
			pass

	def get_chapters(page):
		chapters = set()
		for match in re.finditer(r"/.*\.full\.pdf", page):
			chapterLink = "https://advances.sciencemag.org" + match.group(0)
			chapters.add(chapterLink)
		return chapters

