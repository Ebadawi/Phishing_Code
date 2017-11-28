import urllib 
import io
import shutil
import sys
from shutil import copyfile

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
def terms_report(URLListFile,year, month):
	URLList=[]
	oldTermsList = []
	newTermsList = []
	NewTerms=[]
	DeletedTerms=[]
	count=0
	oldMonth=12 if month==1 else month-1
	oldYear=year-1 if month==1 else year
	oldDate=str(oldYear)+'-0'+str(oldMonth) if month<11 and month > 1 else str(oldYear)+'-'+str(oldMonth)
	newDate=str(year)+'-0'+str(month) if month<10 else str(year)+'-'+str(month)
	new_Occ=4
	old_Rank=2
	header=""
	termsReportFileName="inurl-terms-report-"
	oldPathReportFileName=open(termsReportFileName+oldDate+".csv", 'r', encoding='utf-8') # the previous report
	termsReportFileName=termsReportFileName+newDate+".csv"# to create new report

	#read the old data month by month (based on the input argumant) to make the report 
	with io.open(URLListFile, 'r', encoding='utf-8') as fin: # the complete list from Si
		datalist2 = eval(fin.read())
	for file in datalist2:
		#print ("a")
		if(newDate in file[3]):
			URLList.append(file[1])

	for str2 in URLList:
		str2=str2.split()
		#str2[0] =urllib.unquote(str2[0]).decode('utf8') 
		#print str2[0]
		urlsplit=str2[0].split("/")
		lenn=len(urlsplit)
		if not urlsplit[lenn-1]:
			lenn=lenn-1
		#urlsplit = filter(None, urlsplit)
		#print urlsplit
		for loc in range(3,lenn):
			word=urlsplit[loc]
			
			if (loc==(lenn-1)or loc==(lenn-2))and ((".html" in word or ".htm" in word or ".php"  in word)):
				#print word +" imad"
				continue
			#print word
			found=find_term_inList(word,newTermsList)
			if found==-1 :
				term=[word,1,0]
				newTermsList.append(term)
				#print term
			else:
				newTermsList[found][1]=newTermsList[found][1]+1
	print(str(len(newTermsList)))	

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
		oldTermsList.append(str2)
	
	for FullTerm in oldTermsList: # to check all the old terms we have
		term = FullTerm[0]
		found=find_term_inList(term,newTermsList)
		if found==-1 : # the term did not appear this month
			DeletedTerms.append(FullTerm)
		else: # copy the new occurrence for the specified term
			FullTerm[new_Occ]=newTermsList[found][1]
			newTermsList[found][2]=1 # the term did appear before	
					
	for FullTerm2 in newTermsList: # to check all the new terms we have
		TermTemplate=["aa",0,0,0,0,0,0,0]
		if FullTerm2[2]==0 : # the term did not appear in the previous month
			NewTerms.append(FullTerm2)
			TermTemplate[0]=FullTerm2[0]
			TermTemplate[new_Occ]=FullTerm2[1]
			oldTermsList.append(TermTemplate)

	TermsDataOutput2 = open(termsReportFileName, "w") # the analysis output
	oldTermsList=sorted(oldTermsList, key=lambda index_loc: index_loc[new_Occ], reverse=True) 
	count=1
	TermsDataOutput2.write (str(header))
	for FullTerm in oldTermsList:
		FullTerm[old_Rank-1]=count
		FullTerm[old_Rank+1]=int(FullTerm[old_Rank])-count
		FullTerm[new_Occ+2] = str(int(FullTerm[new_Occ])-int(FullTerm[new_Occ+1]))
		if str(FullTerm[new_Occ+1])=='0':
			FullTerm[old_Rank]="NA"
			FullTerm[old_Rank+1]="NA"
		for i in range(0,len(FullTerm)-2):
			TermsDataOutput2.write ('"'+str(FullTerm[i])+'",')
		TermsDataOutput2.write ('"'+str(FullTerm[len(FullTerm)-2])+'"')
		if(count==len(oldTermsList)):
			TermsDataOutput2.write ('"')
		else:
			TermsDataOutput2.write ("\n")
		count=count+1
		
	TermsDataOutput2.close()

# main	
year=int(sys.argv[1])
month=int(sys.argv[2])


print ("Emad")

terms_report('urltime_20170901_20170927',year,month)	

	
	