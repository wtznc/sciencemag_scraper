import os
from PyPDF2 import PdfFileMerger
from pdb import set_trace as bp 
import sys
sys.setrecursionlimit(10000)

def main():
	pdf_paths = []
	for root, dirs, files in os.walk("./"):
		for file in files:
			if file.endswith(".pdf"):
				pdf_paths.append(os.path.join(root, file))





	allofem = set()
	for file in pdf_paths:
		#print("file = ", file)
		parent = file.split("/")[1]
		child = file.split("/")[2]
		combined = parent+"/"+child
		if combined not in allofem:
			allofem.add(parent+"/"+child)


	listFolders = list(allofem)

	for folder in listFolders:
		x = [a for a in os.listdir(folder) if a.endswith(".pdf")]
		merger = PdfFileMerger()
		for pdf in x:
			current = folder+"/"+pdf
			print("current = ", current)
			merger.append(open(current, 'rb'))
		with open(folder+"merged.pdf", "wb") as fout:
			merger.write(fout)
	
if __name__ == '__main__':
	main()