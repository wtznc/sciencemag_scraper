import pysnooper
import os
import sys
import urllib.request

import argparse
from pdb import set_trace as bp

from tools import Tools as tl

def args():
	parser = argparse.ArgumentParser(description='SCIENCEMAG - Web Scrapper')
	parser.add_argument('url', type=str, help='Provide a main URL: e.g https://advances.sciencemag.org')
	parser.add_argument('save_to', type=str, help='Where to save downloaded files')
	parser.add_argument('year', type=int, help='Year: ')
	args = parser.parse_args()
	return args

def main(args):
	current_directory = os.getcwd()
	if(args.url=='1'):
		root_url = 'https://advances.sciencemag.org'
	if(args.save_to == '.'):
		save_to = os.getcwd()
	if(args.year):
		year = args.year


	archives = tl.get_archives(root_url, year)



	for x in archives:
		os.chdir(current_directory)
		current_volume = x.split('/')[2]
		current_issue = x.split('/')[3]

		volume_path = "volume_" + str(current_volume)
		issue_path = "issue_" + str(current_issue)

		if(os.path.isdir(volume_path)):
			os.chdir(volume_path)
			if(os.path.isdir(issue_path)):
				try:
					current_page = tl.get_page(root_url+x, current_volume, current_issue)
					chapters = tl.get_chapters(current_page)
					chapters = list(chapters)
				except IOError as e:
					print('Error: ', e)
				except Exception as e:
					print("Exception: ", e)
					continue

				print("I found ", len(chapters), " articles!")
				for x in range(0, len(chapters)):
					exists = os.path.isfile(issue_path+"//ch"+str(x)+".pdf")
					# not only path but also file size
					if exists:
						print("["+str(x+1)+"/"+str(len(chapters))+"] already exists!")
						pass
					else:
						try:
							print("Downloading ["+str(x+1)+"/"+str(len(chapters))+"] article")
							urllib.request.urlretrieve(chapters[x], (issue_path+"//ch"+str(x)+".pdf"))
						except IOError as e:
							print("Error: ", e)
							continue
						except Exception as e:
							print("Error: ", e)
							continue
				print("Finished!")
			else:
				os.mkdir(issue_path)

		else:
			os.mkdir(volume_path)
			os.chdir(volume_path)
			if(os.path.isdir(issue_path)):
				pass
			else:
				os.mkdir(issue_path)
	

	#print(wynik)

if __name__ == '__main__':
	main()