from urllib.request import Request, urlopen
import urllib.error
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt 
import re

classes = []
print("Welcome to your one stop shop for looking at Stanford grade distributions side by side for multiple classes!")
print("Note that this data is pulled from Edusalsa, which means there may be slight discrepancies with Carta, as")
print("well as missing data for smaller classes. This tool works best for more established classes with more students.")
print("Also note that the .exe application may take a few seconds longer to load the graphs for large number of classes.\n")
print("Follow the instructions below to see the course distributions for any number of classes you may want to take!\n")

toAdd = input("Enter a class using the course name and number, with a space in between (i.e. \"CS 103 \"). Press enter when done entering classes: ")
while(toAdd == ""):
	toAdd = input("Please enter at least one valid class: ")
while (toAdd != "") or (not classes):
	className = toAdd.split( )
	if (len(className) == 2):
		toAdd = className[0] + '%20' + className[1]
		classes.append(toAdd.upper())
		toAdd = input("Enter a class using the course name and number, with a space in between (i.e. \"CS 103 \"). Press enter when done entering classes: ")
	else:
		toAdd = input("Enter at least one valid course name (press Enter to stop entering classes): ")
#to test if classes have been inputted
#print(classes)

grades = [] # an array containing an array for each class. each inner array is populated with raw numbers of each grade
percents = [] # double array, like above, containing raw percents for each grade in each class
cumulativeDist = [] # double array, like above, containing the cumulative sum of each grade in each class

# This populates the grades array, which contains raw counts for each grade in each class.
for course in classes:
	try: 
		url = 'https://edusalsa.com/course?c=' + course 
		req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
		webpage = urlopen(req).read()
		bsObj = BeautifulSoup(webpage, 'html.parser')
		gradeDist = str(bsObj.find("script"))
		arrStarted = False
		arr = ""
		for c in gradeDist:
			if(c == '['):
				arrStarted = True
			if(c == ']'):
				arrStarted = False
				arr += c
				break
			if(arrStarted):
				arr += c
		#to test if the string has been properly formed
		#print(arr)
		grades.append([int(s) for s in re.findall(r'\d+', arr)])
	except urllib.error.HTTPError:
		print(course + " does not exist on Edusalsa (check your spelling?)")
		grades.append([])
# This populates the percents array, which contains raw percents for each grade in each class.
for gradeDist in grades:
	sum = np.sum(gradeDist)
	toApp = []
	for grade in gradeDist:
		toApp.append(((grade/sum)*100))
	percents.append(toApp)
# This populates the cumulativeDist array, which contains the sum of each grade and all the grades higher than it
# for each class.
for percentDist in percents:
	sum = 0
	toApp = []
	for percent in percentDist:
		sum += percent
		toApp.append(sum)
	cumulativeDist.append(toApp)

#At this point, grades, percents, and cumulative distribution have all been calculated and stored for each class.
#to test if grades, percents, and cumulativeDist are populated with proper values
#print(grades)
#print(percents)
#print(cumulativeDist)


#Matplotlib graphing code.

x = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F', 'CR', 'NC']
f, axarr = plt.subplots(2)
barWidth = 0.8/len(classes)
barX = np.arange(len(x))
graphExists = False
# plots the cumulative and absolute percent distribution for each entered class
for index, item in enumerate(classes):
	a, b = item.split("%20")
	label = a + " " + b
	if grades[index]:
		graphExists = True
		axarr[0].plot(cumulativeDist[index], '-o' ,label=label)
		axarr[1].bar(barX+((index-(len(classes)/2))*barWidth), percents[index], width=barWidth, label=label)
	else: 
		print(label + " has no grade data in Edusalsa.")
if graphExists:
	for ax in f.axes:
		ax.set_xticks(np.arange(len(x)))
		ax.set_xticklabels(x)
		ax.set_xlabel("Grade")
		leg = ax.legend(loc='best', ncol=2, mode="expand", shadow=True, fancybox=True)
		leg.get_frame().set_alpha(0.2)

	f.axes[0].set_ylabel("Cumulative Percent")
	f.axes[1].set_ylabel("Absolute Percent")
	plt.show()
else: 
	print("Oh no! None of the classes you entered can be graphed at this time. This is most likely because Edusalsa")
	print("has no grade data for any these classes, or you entered the classes in an invalid format.")