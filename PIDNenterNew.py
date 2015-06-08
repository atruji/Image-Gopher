import easygui as eg
import os


msg = "Enter the PIDN:"
title="Image Gopher"
fieldNames=["PIDN"]
fieldValues=[] 
fieldValues=eg.multenterbox(msg,title,fieldNames)

# make sure that none of the fields was left blank
while 1:  # do forever, until we find acceptable values and break out
	if fieldValues == None: 
		break
	errmsg = ""
    
    # look for errors in the returned values
	for i in range(len(fieldNames)):
		
	        if fieldValues[i].strip() == "":
	        	errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
        
	if errmsg == "": 
        	break # no problems found
    	else:
        	# show the box again, with the errmsg as the message    
       		fieldValues = eg.multenterbox(errmsg, title, fieldNames, fieldValues)
    
print "PIDN selected:", fieldValues


import MySQLdb

# Open database connection
db = MySQLdb.connect("localhost","root","sl4155140868;","SLPatientDB" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT * from SLPatientDB.Scans where PIDN="+fieldValues[0])

# Fetch a single row using fetchone() method.
data = cursor.fetchall()
choices=[]

for i in data:

	choices.append(str(i[1]))
	
msg     = "Select the scan date for PIDN:"+str(fieldValues[0])+":"
title   = "Image Gopher"
choic   = eg.choicebox(msg, title, choices)

choice="'%s'" % choic
# execute SQL query using execute() method.
cursor.execute("SELECT * from SLPatientDB.Scans where PIDN="+fieldValues[0]+" and DATE(ScanDate)="+choice)

# Fetch a single row using fetchone() method.
data = cursor.fetchone()



#msg="Select image type for PIDN:"
#title ="Image Gopher"
#choices= ["T1","FLAIR"]
#ImgType=eg.buttonbox(msg,title,choices,image=None,root=None)

#print "Image selected for PIDN:",str(fieldValues[0]),"for Date:",choic, "and Image Type:", ImgType
T1=data[3]
Flair=data[4]
T1=T1.replace('/data5/','/Volumes/seeley_imaging/data5/')
T1=T1.replace('img','hdr')

Flair=Flair.replace('/data5/','/Volumes/seeley_imaging/data5/')
Flair=Flair.replace('img','hdr')

commandT1="/usr/local/fsl/bin/fslview.app/Contents/MacOS/fslview "+T1
commandFlair="/usr/local/fsl/bin/fslview.app/Contents/MacOS/fslview "+Flair
os.system(commandT1+"|"+commandFlair)


#disconnect from server
db.close()
