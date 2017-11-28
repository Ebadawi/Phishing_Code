import urllib 
import io
import shutil
import sys
from shutil import copyfile

def getURLPath(url, withParameter=False, removeSlash=True):
	"""
	return the path of request
	:param url: URL for checking
	:return: path of request, if just access root path, return None
	"""
	urlPath = url.split("://", 1)[-1].split("/", 1)

	if len(urlPath) < 2 or not urlPath[-1]:
		return None
	else:
		if withParameter:
			urlPath = urlPath[-1]
		else:
			urlPath = urlPath[-1].split("?", 1)[0]

		#remove last /
		if removeSlash:
			if urlPath and urlPath[-1] == "/":
				urlPath = urlPath[:-1]

	return urlPath

def find_term_inList( str2, dataList ):
	size =len(dataList)
	if size ==0:
		return -1
	for loc in range(0,size):
		#print len(dataList)
		term2=dataList[loc]
		#print term2
		if str2.lower() in term2[0].lower() and len(str2)== len(term2[0]):
			return loc
	return -1


def path_report(URLListFile,year, month):
	oldMonth=12 if month==1 else month-1
	oldYear=year-1 if month==1 else year
	oldDate=str(oldYear)+'-0'+str(oldMonth) if month<11 and month > 1 else str(oldYear)+'-'+str(oldMonth)
	newDate=str(year)+'-0'+str(month) if month<10 else str(year)+'-'+str(month)
	URLList=[] # used to save the URLs for the specified data range
	oldPathsList = [] # contains the old data
	newPathsList = []# contains the new generated data
	NewTerms=[]
	DeletedTerms=[]
	count=0
	new_Occ=4
	old_Rank=2
	header=""
	pathReportFileName="inurl-path-report-"
	oldPathReportFileName=open(pathReportFileName+oldDate+".csv", 'r') # the previous report
	pathReportFileName=pathReportFileName+newDate+".csv"# to create new report
	#read the old data month by month (based on the input argumant) to make the report 
	with io.open(URLListFile, 'r', encoding='utf-8') as fin: # the complete list from Si
		datalist2 = eval(fin.read())
	for file in datalist2:
		#print ("a")
		if(newDate in file[3]):
			URLList.append(file[1])
			#checkFile.write(file[1]+"\n")
	# find all the terms in the URLList
	for str2 in URLList:

		path=str(getURLPath(str2))
		#if(path.lower()=="none"):
			#path="root_directory"
		found=find_term_inList(path,newPathsList)
		if found==-1 :
			term=[path,1,0]
			newPathsList.append(term)
			#print term
		else:
			newPathsList[found][1]=newPathsList[found][1]+1
			
	print(len(newPathsList))	
	# to read the old repory
	h2Flag=0
	while 1:
		str2=oldPathReportFileName.readline()
		if not str2: break
		#print(str2)
		if h2Flag==0:
			header=str2
			h2Flag=1
			continue
		str2=str2[:-1]
		str2=str2.rstrip('"').lstrip('"').replace('","','"')
		str2=str2.split('"' )
		if str2[new_Occ]=="0": continue # this mean the terms did not occure in the previous month but in the one before
		str2[len(str2)-1]=0
		str2.append(0)
		str2[old_Rank]= str2[old_Rank-1]
		str2[new_Occ+1]= str2[new_Occ]
		str2[new_Occ]= 0
		oldPathsList.append(str2)
	for FullPath in oldPathsList: # to check all the old terms we have
		term = FullPath[0]
		found=find_term_inList(term,newPathsList)
		if found==-1 : # the term did not appear this month
			DeletedTerms.append(FullPath)
		else: # copy the new occurrence for the specified term
			FullPath[new_Occ]=newPathsList[found][1]
			newPathsList[found][2]=1 # the term did appear before	
			
			
	for FullPath2 in newPathsList: # to check all the new terms we have
		TermTemplate=["aa",0,0,0,0,0,0,0]
		if FullPath2[2]==0 : # the term did not appear in the previous month
			NewTerms.append(FullPath2)
			TermTemplate[0]=FullPath2[0]
			TermTemplate[new_Occ]=FullPath2[1]
			oldPathsList.append(TermTemplate)

	PathsDataOutput2 = open(pathReportFileName, "w") # the analysis output
	oldPathsList=sorted(oldPathsList, key=lambda index_loc: index_loc[new_Occ], reverse=True) 
		
	count=1
	PathsDataOutput2.write (str(header))
	for FullPath in oldPathsList:
		FullPath[old_Rank-1]=count
		FullPath[old_Rank+1]=int(FullPath[old_Rank])-count
		FullPath[new_Occ+2] = str(int(FullPath[new_Occ])-int(FullPath[new_Occ+1]))
		if str(FullPath[new_Occ+1])=='0':
			FullPath[old_Rank]="NA"
			FullPath[old_Rank+1]="NA"
		for i in range(0,len(FullPath)-2):
			PathsDataOutput2.write ('"'+str(FullPath[i])+'",')
		PathsDataOutput2.write ('"'+str(FullPath[len(FullPath)-2])+'"')
		if(count==len(oldPathsList)):
			PathsDataOutput2.write ('"')
		else:
			PathsDataOutput2.write ("\n")
		count=count+1
		
	PathsDataOutput2.close()	

	
# main	
year=int(sys.argv[1])
month=int(sys.argv[2])


print ("Emad")

path_report('urltime_20160101_20170925',year,month)	






