from tkinter.filedialog import askopenfilename
import numpy as np
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

np.set_printoptions(suppress=True)

#get excelfile
myFileName = askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])

#read excelfile
myExcelDoc = pd.read_excel(myFileName, sheet_name=0)

#set starting number of lines
myExampleNumber = 36

#set arrays
myXlist = []
myYList = []
myHeightList = []

#set starting number for LSA
numberofLSA = 0

#first filling of lists
for i in range(myExampleNumber):
    myXlist.append(myExcelDoc.iloc[i+4,1])
    myYList.append(myExcelDoc.iloc[i+4,2])
    myHeightList.append(myExcelDoc.iloc[i+4,3])

#calculate the LSA for one rund
def calcLSA(myXlist, myYList, myHeightList, myExampleNumber, numberofLSA):

    #print LSA iteration number
    numberofLSA = numberofLSA + 1
    print("Least square adjustment Nr. " + str(numberofLSA))

    print("Lenght of training data: " + str(len(myXlist)))

    #create matrix
    myXVector = np.empty(shape=(myExampleNumber,1)) #height
    myAMatrix = np.empty(shape=(myExampleNumber,6)) #x,y

    #iterate through line
    for i in range(myExampleNumber):
        myXVector[i] = myHeightList[i]

        #get x and y value
        x = myXlist[i]
        y = myYList[i]

        #create AMatrix
        myAMatrix[i][0] = 1.0
        myAMatrix[i][1] = x
        myAMatrix[i][2] = y
        myAMatrix[i][3] = x * y
        myAMatrix[i][4] = x * x
        myAMatrix[i][5] = y * y

    #calculate the unknown vector
    myFirstPart = np.linalg.inv(np.dot(np.transpose(myAMatrix), myAMatrix))
    mySecondPart = np.dot(np.transpose(myAMatrix), myXVector)
    myYVector = np.dot(myFirstPart, mySecondPart)

    print("a1 = " + str(myYVector[0]))
    print("a2 = " + str(myYVector[1]))
    print("a3 = " + str(myYVector[2]))
    print("a4 = " + str(myYVector[3]))
    print("a5 = " + str(myYVector[4]))
    print("a6 = " + str(myYVector[5]))

    myXEstVector = np.empty(shape=(myExampleNumber,1)) #estimated height
    myDifferenceVector = np.empty(shape=(myExampleNumber,1)) #difference between estimated height and measured height

    #create list that contains the outliers which have to be deleted
    myDeleteList = []

    for i in range(myExampleNumber):
        myXEstVector[i] = myYVector[0] + myYVector[1] * myAMatrix[i][1] + myYVector[2] * myAMatrix[i][2] + myYVector[3] * myAMatrix[i][3] + myYVector[4] * myAMatrix[i][4] + myYVector[5] * myAMatrix[i][5]
        myDifferenceVector[i] = abs(myXVector[i] - myXEstVector[i])

        #if outlier is detected
        if (myDifferenceVector[i] > 0.196):
            print("Outlier detected with difference of " + str(myDifferenceVector[i]) + " (Height: " + str(myXVector[i]) + ")")
            myDeleteList.append(i)

    #iterate LSA if there are still outliers detected
    if len(myDeleteList) > 0:

        #delete from X, Y, Z
        #need to be reversed, because the hightes indices need to be deleted first
        for myDelIndex in reversed(myDeleteList):
            del myXlist[myDelIndex]
            del myYList[myDelIndex]
            del myHeightList[myDelIndex]

        #set new myExampleNumber
        myExampleNumber = len(myXlist)

        #repeat LSA
        calcLSA(myXlist, myYList, myHeightList, myExampleNumber, numberofLSA)

#start LSA
calcLSA(myXlist, myYList, myHeightList, myExampleNumber, numberofLSA)
