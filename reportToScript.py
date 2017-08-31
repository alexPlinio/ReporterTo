# -*- coding: utf-8 -*-
"""
Alex Guglielmetti
08/30/2017
Little script to create new excel file that provides a 
subset of all team members reporting under one manager, VP, Director, etc
***NOTE THERE IS A BUG - IF mgrZero = John Herbert I get an infinite loop

"""

#=============  Libraries  ==========================
import pandas as pd
import datetime

#====================================================
""" Load CSV to Pandas"""

def load_csv_to_df (file,verbose): 
    ''' loads Data Set to a temp Pandas data.frame. This file is the one I will manipulate  '''    

    tempFile = pd.read_csv(file)
    if verbose: print("DEBUG: List Headers>  ",list(tempFile))
    if verbose: print ('\nDEBUG: tempFile has >>> {1} columns and {0} rows >>> '.format(tempFile.shape[0],tempFile.shape[1]))   
    return tempFile       

#====================================================
''' Check for people that report under specific manager'''    
def myTeamDF(manager,DF):
    myTeamDF = DF[DF['Manager']==manager]
    print ('\nDEBUG: {2} has >>> {1} columns and {0} people that reports to >>> '.format(myTeamDF.shape[0],myTeamDF.shape[1],manager)) 
    return  myTeamDF

#====================================================
def myTeamList (mgr,DF):
    tDF=myTeamDF(mgr,DF)
    mgrList= tDF['Display Name'].tolist()
    return mgrList

#====================================================
def allTeamDF (DF, isinL) :
    teamDF = DF[DF['Display Name'].isin(isinL)]
    return  teamDF      
#====================================================

def save_df_to_csv(df,csvName,verbose):
    '''Saves data frame into a new CSV file. Input is: a Pandas dataframe and CSV Name string '''
    
    now=datetime.datetime.now()
    timeStamp=now.strftime("%Y.%m.%d_%H%M%S.CSV")
    fileName=csvName+timeStamp
    df.to_csv(fileName) # Saves the data frame file into CSV. The Original file remains untouched. TempFile is the one I will transform
        
    return

#================= MAIN - MAIN ===================================

if __name__ == '__main__':
 
    #Set up Variables  
    mgrZero = "Victor Chan"
    verbose= False
    allTeam=[]
    
    #load CSV to Panda
    ActDirDF=load_csv_to_df ("All-FFE-Domain-Users_201706060357.csv",verbose)
    
    #Get first row of people that report to the manager Zero. Return Dataframe
    tList=myTeamList(mgrZero, ActDirDF)
    
    # Fetch all team members
    if len(tList)>0:
        allTeam.extend(tList)
        x = 0
        while len(allTeam)>x:
            if len(myTeamList(allTeam[x],ActDirDF))>0:
                allTeam.extend(myTeamList(allTeam[x],ActDirDF))
            x+=1
            
    #print('The total Team Members {0} has is: {1}'.format(mgrZero,len(allTeam)) )
    
    
    # Create ALlTeam Data Frame to export the result to excel
    outputDF=allTeamDF (ActDirDF,allTeam)
    #print(outputDF.head(5))
    
    save_df_to_csv(outputDF,mgrZero,verbose)
    
    print(outputDF.info())
    
            
        
    