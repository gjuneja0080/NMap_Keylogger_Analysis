#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 04:05:23 2019

@author: gopaljuneja
"""
import pandas as pd
import os
import numpy as np
from datetime import datetime as dt



def deleteRow(df, colName, val):
    #delete last row from dataframe
    if df[colName].str.contains(val).any():
        df = df.drop(df.index[-1])
    return df
     

def readLogFile(df, path):
    df = pd.read_csv(path,names=["DateTime", "Time(Milliseconds)", "Key"], dtype={'Time(Milliseconds)': str})
    return df

def extractTime(df):
    #Extracting time out of DateTime into a separate column
    df['Time'] = df['DateTime'].str.split(' ').str[1]
    #Combining the time column with milliseconds column
    df['Time'] = df['Time'] + "." + df["Time(Milliseconds)"].map(str)
    df = df.drop(['DateTime'], axis =1)
    return df

def toMSformat(df, label1):
    #column for key pressed time
    df[label1] = df["Time"]
    df[label1] = df[label1].astype(str) 
    #converting the type to timedelta from object
    df[label1] = df[label1].apply(pd.to_timedelta)
    #converting time to milliseconds
    df[label1] = df[label1].astype('timedelta64[ms]')
    df[label1] = df[label1].apply(lambda x: '%.f' % x)
    
    return df[label1]
    

def calcTimeDiff(df1, df2):
    #df_TimeDifference = pd.DataFrame()
    df_TimeDifference = pd.DataFrame()
    
    df_TimeDifference["timeKeyPressed(ms)"] = toMSformat(df1, "timeKeyPressed(ms)")
    df_TimeDifference["timeKeyReleased(ms)"] = toMSformat(df2, "timeKeyReleased(ms)")
    #calculating the time difference
    df_TimeDifference['time_diff'] = df_TimeDifference['timeKeyReleased(ms)'].astype(float) - df_TimeDifference['timeKeyPressed(ms)'].astype(float)
    #Adding the key values to dataframe
    df_TimeDifference['Key'] = df1['Key']
    return df_TimeDifference


def formatDF(df, filepath):
    df = pd.DataFrame()
    df = readLogFile(df,filepath)
    df = deleteRow(df, 'Key', 'Key.esc')
    df = extractTime(df)
    df['Time(ms)'] = toMSformat(df, 'Time(ms)')
    return df

df_attackerKeyPress = pd.DataFrame()
df_attackerKeyPress = formatDF(df_attackerKeyPress,r'/Users/gopaljuneja/Desktop/CS4203/key_ErnielogPress.csv')

df_attackerKeyRelease = pd.DataFrame()
df_attackerKeyRelease = formatDF(df_attackerKeyRelease,r'/Users/gopaljuneja/Desktop/CS4203/key_ErnielogRelease.csv')

df_victimKeyPress = pd.DataFrame()
df_victimKeyPress = formatDF(df_victimKeyPress,r'/Users/gopaljuneja/Desktop/CS4203/key_PandalogPress.csv')

df_victimKeyRelease = pd.DataFrame()
df_victimKeyRelease = formatDF(df_victimKeyRelease,r'/Users/gopaljuneja/Desktop/CS4203/key_PandalogRelease.csv')


#Getting Interaction time with each key: which is key released - key pressed
df_timeTakenA = calcTimeDiff(df_attackerKeyPress, df_attackerKeyRelease)
df_timeTakenA['Key'] = df_attackerKeyPress['Key']
df_timeTakenV = calcTimeDiff(df_victimKeyPress, df_victimKeyRelease)
df_timeTakenV['Key'] = df_victimKeyPress['Key']

#this is checking the time taken to press each key by the victim and the attacker and then creates a threshold checking attackers logs 
#under tolerance rates
#Interaction Time: The time taken to press and release a key

def hyp2a(threshold):
    df_verifyHypothesis = pd.DataFrame()
    df_verifyHypothesis["Victim's Key "] = df_timeTakenV["Key"]
    df_verifyHypothesis["Victim's Key Interaction Time"] = df_timeTakenV["time_diff"]
    df_verifyHypothesis["Attacker's Key"] = df_timeTakenA["Key"]
    df_verifyHypothesis["Attacker's Key Interaction Time"] = df_timeTakenA["time_diff"]

  
    df_verifyHypothesis["Threshold Val"] = (df_timeTakenV["time_diff"] * threshold)/100

    df_verifyHypothesis['Tolerance+'] = df_verifyHypothesis["Victim's Key Interaction Time"] + df_verifyHypothesis['Threshold Val']
    df_verifyHypothesis['Tolerance-'] = df_verifyHypothesis["Victim's Key Interaction Time"] - df_verifyHypothesis['Threshold Val']
    
    df_verifyHypothesis['Within Threshold'] = np.where((df_verifyHypothesis["Attacker's Key Interaction Time"] > df_verifyHypothesis['Tolerance+']) | (df_verifyHypothesis["Attacker's Key Interaction Time"] < df_verifyHypothesis['Tolerance-']) , 'False', 'True')
    return  df_verifyHypothesis

#################### Case1 hypothesis 1
    
df_Hypothesis1C1T25 = hyp2a(25)
countC1T25 = df_Hypothesis1C1T25['Within Threshold'].value_counts()
df_Hypothesis1C1T25.to_csv(r'/Users/gopaljuneja/Desktop/CS4203/Hyp1C1T25.csv')

df_Hypothesis1C1T50 = hyp2a(50)
countC1T50 = df_Hypothesis1C1T50['Within Threshold'].value_counts()
df_Hypothesis1C1T50.to_csv(r'/Users/gopaljuneja/Desktop/CS4203/Hyp1C1T50.csv')

df_Hypothesis1C1T75 = hyp2a(75)
countC1T75 = df_Hypothesis1C1T75['Within Threshold'].value_counts()
df_Hypothesis1C1T75.to_csv(r'/Users/gopaljuneja/Desktop/CS4203/Hyp1C1T75.csv')

#################### Case2 hypothesis 1
df_Hypothesis1C2T25 = hyp2a(25)
countC2T25 = df_Hypothesis1C2T25['Within Threshold'].value_counts()
df_Hypothesis1C2T25.to_csv(r'/Users/gopaljuneja/Desktop/CS4203/Hyp1C2T25.csv')

df_Hypothesis1C2T50 = hyp2a(50)
countC2T50 = df_Hypothesis1C2T50['Within Threshold'].value_counts()
df_Hypothesis1C2T50.to_csv(r'/Users/gopaljuneja/Desktop/CS4203/Hyp1C2T50.csv')

df_Hypothesis1C2T75 = hyp2a(75)
countC2T75 = df_Hypothesis1C2T75['Within Threshold'].value_counts()
df_Hypothesis1C2T75.to_csv(r'/Users/gopaljuneja/Desktop/CS4203/Hyp1C2T75.csv')

#################### Case3 hypothesis 1
df_Hypothesis1C3T25 = hyp2a(25)
countC3T25 = df_Hypothesis1C3T25['Within Threshold'].value_counts()
df_Hypothesis1C3T25.to_csv(r'/Users/gopaljuneja/Desktop/CS4203/Hyp1C3T25.csv')

df_Hypothesis1C3T50 = hyp2a(50)
countC3T50 = df_Hypothesis1C3T50['Within Threshold'].value_counts()
df_Hypothesis1C3T50.to_csv(r'/Users/gopaljuneja/Desktop/CS4203/Hyp1C3T50.csv')

df_Hypothesis1C3T75 = hyp2a(75)
countC3T75 = df_Hypothesis1C3T75['Within Threshold'].value_counts()
df_Hypothesis1C3T75.to_csv(r'/Users/gopaljuneja/Desktop/CS4203/Hyp1C3T75.csv')

#################### Case1 hypothesis 2
df_Hypothesis1C1T25 = hyp2a(25)
H2countC1T25 = df_Hypothesis1C1T25['Within Threshold'].value_counts()
df_Hypothesis1C1T25.to_csv(r'/Users/gopaljuneja/Desktop/CS4203/Hyp2C1T25.csv')

df_Hypothesis1C1T50 = hyp2a(50)
H2countC1T50 = df_Hypothesis1C1T50['Within Threshold'].value_counts()
df_Hypothesis1C1T50.to_csv(r'/Users/gopaljuneja/Desktop/CS4203/Hyp2C1T50.csv')

df_Hypothesis1C1T75 = hyp2a(75)
H2countC1T75 = df_Hypothesis1C1T75['Within Threshold'].value_counts()
df_Hypothesis1C1T75.to_csv(r'/Users/gopaljuneja/Desktop/CS4203/Hyp2C1T75.csv')

#################### Case2 hypothesis 2
df_Hypothesis2C2T25 = hyp2a(25)
H2countC2T25 = df_Hypothesis2C2T25['Within Threshold'].value_counts()
df_Hypothesis2C2T25.to_csv(r'/Users/gopaljuneja/Desktop/CS4203/Hyp2C2T25.csv')

df_Hypothesis2C2T50 = hyp2a(50)
H2countC2T50 = df_Hypothesis2C2T50['Within Threshold'].value_counts()
df_Hypothesis2C2T50.to_csv(r'/Users/gopaljuneja/Desktop/CS4203/Hyp2C2T50.csv')

df_Hypothesis2C2T75 = hyp2a(75)
H2countC2T75 = df_Hypothesis2C2T75['Within Threshold'].value_counts()fttttttttttttttttttt7y]
df_Hypothesis2C2T75.to_csv(r'/Users/gopaljuneja/Desktop/CS4203/Hyp2C2T75.csv')

#################### Case3 hypothesis 2
df_Hypothesis2C3T25 = hyp2a(25)
H2countC3T25 = df_Hypothesis2C3T25['Within Threshold'].value_counts()
df_Hypothesis2C3T25.to_csv(r'/Users/gopaljuneja/Desktop/CS4203/Hyp2C3T25.csv')

df_Hypothesis2C3T50 = hyp2a(50)
H2countC3T50 = df_Hypothesis2C3T50['Within Threshold'].value_counts()
df_Hypothesis2C3T50.to_csv(r'/Users/gopaljuneja/Desktop/CS4203/Hyp2C3T50.csv')

df_Hypothesis2C3T75 = hyp2a(75)
H2countC3T75 = df_Hypothesis2C3T75['Within Threshold'].value_counts()
df_Hypothesis2C3T75.to_csv(r'/Users/gopaljuneja/Desktop/CS4203/Hyp2C3T75.csv')

#################### Case1 hypothesis 4
df_Hypothesis4C1T25 = hyp2a(25)
H4countC1T25 = df_Hypothesis4C1T25['Within Threshold'].value_counts()
df_Hypothesis4C1T25.to_csv(r'/Users/gopaljuneja/Desktop/CS4203/Hyp4C1T25.csv')

df_Hypothesis4C1T50 = hyp2a(50)
H4countC1T50 = df_Hypothesis4C1T50['Within Threshold'].value_counts()
df_Hypothesis4C1T50.to_csv(r'/Users/gopaljuneja/Desktop/CS4203/Hyp4C1T50.csv')

df_Hypothesis4C1T75 = hyp2a(75)
H4countC1T75 = df_Hypothesis4C1T75['Within Threshold'].value_counts()
df_Hypothesis4C1T75.to_csv(r'/Users/gopaljuneja/Desktop/CS4203/Hyp4C1T75.csv')

#################### Case2 hypothesis 4
df_Hypothesis4C2T25 = hyp2a(25)
H4countC2T25 = df_Hypothesis4C2T25['Within Threshold'].value_counts()
df_Hypothesis4C2T25.to_csv(r'/Users/gopaljuneja/Desktop/CS4203/Hyp4C2T25.csv')

df_Hypothesis4C2T50 = hyp2a(50)
H4countC2T50 = df_Hypothesis4C2T50['Within Threshold'].value_counts()
df_Hypothesis4C2T50.to_csv(r'/Users/gopaljuneja/Desktop/CS4203/Hyp4C2T50.csv')

df_Hypothesis4C2T75 = hyp2a(75)
H4countC2T75 = df_Hypothesis4C2T75['Within Threshold'].value_counts()
df_Hypothesis4C2T75.to_csv(r'/Users/gopaljuneja/Desktop/CS4203/Hyp4C2T75.csv')

#################### Case3 hypothesis 4
df_Hypothesis4C3T25 = hyp2a(25)
H4countC3T25 = df_Hypothesis4C3T25['Within Threshold'].value_counts()
df_Hypothesis4C3T25.to_csv(r'/Users/gopaljuneja/Desktop/CS4203/Hyp4C3T25.csv')

df_Hypothesis4C3T50 = hyp2a(50)
H4countC3T50 = df_Hypothesis4C3T50['Within Threshold'].value_counts()
df_Hypothesis4C3T50.to_csv(r'/Users/gopaljuneja/Desktop/CS4203/Hyp4C3T50.csv')

df_Hypothesis4C3T75 = hyp2a(75)
H4countC3T75 = df_Hypothesis4C3T75['Within Threshold'].value_counts()
df_Hypothesis4C3T75.to_csv(r'/Users/gopaljuneja/Desktop/CS4203/Hyp4C3T75.csv')