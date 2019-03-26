import sys
from numpy import *

element_d={}


def counterofelements(element):
	element_d.setdefault(element,1)	
	if element_d[element] >= 1:
		element_d[element] = element_d[element] + 1
	return(element_d)


def main():
	if len(sys.argv) <= 1:
 		print("Provide a file to be read: ")
	else:
		print(sys.argv[0])
		print(sys.argv[1])
		print(len(sys.argv))
		print(str(sys.argv))
	print("---------------------------------------")

	f = open(sys.argv[1],"r")
	pfile = open(sys.argv[1]+"Structured.txt","w+")
	remove_signs = ["!",",","?","<",">","*",":","@","\'",]

	
	fl = f.readlines()
	wordlist = list()



	for x in fl:
	#Removes unwanted signes liste in remove_signes
		for remove_sign in remove_signs:
			words = x.replace(remove_sign,"")
#		words = words.split()
		wordlist.append(words)
	print(wordlist[10])
	listylist = []

#	print(wordlist[5].split(" "))

	for nsentence in range(len(wordlist)):
		swords = wordlist[nsentence].split()
		#cell_length
		if nsentence == 3:
			pfile.write(str(swords[1])+"\t")
		if nsentence == 4:
			pfile.write(str(swords[1])+"\t")
		if nsentence == 5:
			pfile.write(str(swords[1])+"\t")

		#cell_angle
		if nsentence == 6:
			pfile.write(str(swords[1])+"\t")
		if nsentence == 7:
			pfile.write(str(swords[1])+"\t")
		if nsentence == 8:
			pfile.write(str(swords[1])+"\t")

		#spacegorup
		if nsentence == 9:
			pfile.write(str(swords[1])+"\t")
#		if nsentence == 10:
#			pfile.write(str(swords[1])+"\t")	

		if nsentence >=21:
			swords = wordlist[nsentence].split()
			counterofelements(swords[1])
	print(element_d.items())
	pfile.write("\n")
	pfile.write(str(element_d))

if __name__ == "__main__":
	main()



