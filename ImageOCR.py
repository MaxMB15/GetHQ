# -*- coding: utf-8 -*-

import time
start_time = time.time()

import threading
import ScreenCapture
from PIL import Image
import textract
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob

print("--- %s seconds ---" % (time.time() - start_time))

resultCount = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

def threadStoreResults(threadNum, s):
	resultCount[threadNum] = numResults(s) / 10000.0

class myThread (threading.Thread):
	def __init__(self, threadNum, s):
		threading.Thread.__init__(self)
		self.threadID = threadNum
		self.name = s
	def run(self):
   		threadStoreResults(self.threadID, self.name)

def text_balance(img, brightnessLevel, contrastLevel):
	factor = (259 * (contrastLevel + 255)) / (255 * (259 - contrastLevel))

	def change(c):
		return 128 + factor * ((c * brightnessLevel) - 128)

	return img.point(change)



def numResults(str):
	r = requests.get('http://www.google.com/search', params={'q':'"'+str+'"'})
	soup = BeautifulSoup(r.text, "html.parser" )
	aboutStr = soup.find('div',{'id':'resultStats'}).text
	#print "-> " + aboutStr
	if aboutStr.split(" ")[0] == "About":
		return int((aboutStr.split(" ")[1]).replace(',', ''))
	else:
		print aboutStr
		return int((aboutStr.split(" ")[0]).replace(',', ''))
def getImportantWords(str):
	str.decode("utf-8")
	blob = TextBlob(str)
	words = blob.tags
	retList = []
	for w in words:
		t1, t2 = w
		t2.replace("u'", "")

		if t2.startswith("N"):
			retList.append(t1)

	return retList



result = text_balance(Image.open('screenshot.png'), 0.65, 150)
result = result.crop((100,430,720,1000))
result.save("screenshot.png")

print("--- %s seconds ---" % (time.time() - start_time))

text = textract.process("screenshot.png", encoding='ascii', 
                        method='tesseract')

print("--- %s seconds ---" % (time.time() - start_time))


lines = text.split("\n")
lines = list(filter(None, lines))
#print lines

#Get the useful data
i = -1
usefulData = []

for s in lines:
	if s[-1:] == '?':
		usefulData[0] = usefulData[0] + " " + s
		i = 1
	elif i > -1 and i < 4:
		usefulData.append(s)
		i = i + 1
	else:
		if len(usefulData) == 0:
			usefulData.append(s)
		else:
			usefulData[0] = usefulData[0] + " " + s

print usefulData

print("--- %s seconds ---" % (time.time() - start_time))

#Take out the returns for the question
tempQ = usefulData[0].split("\n")
usefulData[0] = ""
for s in tempQ:
	if "?" not in s:
		usefulData[0] = usefulData[0] + s + " "
	else:
		usefulData[0] = usefulData[0] + s

totalResults = [0.0, 0.0, 0.0, 0.0]
resultFrac = [0.0, 0.0, 0.0, 0.0]

print("--- %s seconds ---" % (time.time() - start_time))




importantWordString = " ".join(getImportantWords(usefulData[0]))
print importantWordString


thr1 = myThread(0, usefulData[1])
thr2 = myThread(1, usefulData[2])
thr3 = myThread(2, usefulData[3])

thr4 = myThread(3, str(importantWordString + " " + usefulData[1]))
thr5 = myThread(4, str(importantWordString + " " + usefulData[2]))
thr6 = myThread(5, str(importantWordString + " " + usefulData[3]))

thr1.start()
thr2.start()
thr3.start()

thr4.start()
thr5.start()
thr6.start()

thr1.join()
totalResults[1] = resultCount[0]
totalResults[0] = totalResults[0] + totalResults[1]
thr2.join()
totalResults[2] = resultCount[1]
totalResults[0] = totalResults[0] + totalResults[2]
thr3.join()
totalResults[3] = resultCount[2]
totalResults[0] = totalResults[0] + totalResults[3]

print("--- %s seconds ---" % (time.time() - start_time))	

for x in xrange(len(usefulData)):
	if x != 0:
		resultFrac[x] = totalResults[0] / totalResults[x]





print "\n"

thr4.join()
print usefulData[1] + "   ~~~   " + str(resultCount[3] * resultFrac[1]) + "   ~~~   " + str(int(resultCount[3]*1000))
print "\n"

thr5.join()
print usefulData[2] + "   ~~~   " + str(resultCount[4] * resultFrac[2]) + "   ~~~   " + str(int(resultCount[4]*1000))
print "\n"

thr6.join()
print usefulData[3] + "   ~~~   " + str(resultCount[5] * resultFrac[3]) + "   ~~~   " + str(int(resultCount[5]*1000))
print "\n"


