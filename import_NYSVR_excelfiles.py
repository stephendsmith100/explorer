#import libraries
import pandas as pd

#create filepaths
fp21 = r"C:\Users\green\Downloads\county_nov21.xlsx"
fp22 = r"C:\Users\green\Downloads\11-01-2022.xlsx"
fp23 = r"C:\Users\green\Downloads\county_nov23.xlsx"
fp24 = r"C:\Users\green\Downloads\county_nov24.xlsx"

#ingest each excel files into a dataframe 
df21 = pd.read_excel(fp21)
df22 = pd.read_excel(fp22)
df23 = pd.read_excel(fp23)
df24 = pd.read_excel(fp24)

#clean each dataframe and add a 'YEAR' column
df21.columns = df21.iloc[3]
df21 = df21.iloc [4:]
df21 = df21.dropna(how='all')
df21.insert (0,'YEAR',2021)

df22.columns = df22.iloc[3]
df22 = df22.iloc [4:]
df22 = df22.dropna(how='all')
df22.insert (0,'YEAR',2022)

df23.columns = df23.iloc[3]
df23 = df23.iloc [4:]
df23 = df23.dropna(how='all')
df23.insert (0,'YEAR',2023)

df24.columns = df24.iloc[3]
df24 = df24.iloc [4:]
df24 = df24.dropna(how='all')
df24.insert (0,'YEAR',2024)

#Merge all the years into a single dataframe
df_combined = pd.concat([df21, df22, df23, df24], ignore_index=True)

