#import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandasql import sqldf

#create filepaths
fp21 = r"C:\Users\green\Downloads\county_nov21.xlsx"
fp22 = r"C:\Users\green\Downloads\11-01-2022.xlsx"
fp23 = r"C:\Users\green\Downloads\county_nov23.xlsx"
fp24 = r"C:\Users\green\Downloads\county_nov24.xlsx"

#ingest each excel files into a dataframe 
df21 = pd.read_excel(fp21, engine="openpyxl")
df22 = pd.read_excel(fp22, engine="openpyxl")
df23 = pd.read_excel(fp23, engine="openpyxl")
df24 = pd.read_excel(fp24, engine="openpyxl")

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


#Use pandasql to query the dataframe
#Goals: analyze the dataframe, create secondary dataframes for visualizations

###Query to create a dataframe showing YoY change in Total voters for each county
queryYoY = """SELECT 
    a.COUNTY, 
    a.YEAR, 
    a.TOTAL AS total_voters, 
    (a.TOTAL - b.TOTAL) * 100.0 / b.TOTAL AS yoy_growth_rate
FROM df_combined a
LEFT JOIN df_combined b 
    ON a.COUNTY = b.COUNTY 
    AND a.YEAR = b.YEAR + 1
WHERE b.TOTAL IS NOT NULL
AND a.STATUS = 'Total' 
AND b.STATUS = 'Total'
ORDER BY a.COUNTY, a.YEAR;"""


###Query for Percent Inactive as share of Total Voters
queryPercentInactive = """SELECT 
    COUNTY, 
    YEAR, 
    (INACTIVE * 100.0 / TOTAL) AS percent_voters_inactive
FROM df_combined
WHERE STATUS = 'Total'
ORDER BY COUNTY, YEAR;"""

###create dataframes based on each query
df_inactive_rate = sqldf(queryPercentInactive,locals())
df_county_yoy = sqldf(queryYoY, locals())

###Create a line plot for Percent Inactive Voters
# Convert YEAR to integer for proper sorting
df_inactive_rate['YEAR'] = df_inactive_rate['YEAR'].astype(int)

# Create the line plot
plt.figure(figsize=(12, 6))
sns.lineplot(data=df_inactive_rate, x="YEAR", y="percent_voters_inactive", hue="COUNTY", marker="o")

# Customize the plot
plt.title("Percent of Inactive Voters by County (2021-2024)")
plt.xlabel("Year")
plt.ylabel("Percent of Voters Inactive (%)")
plt.xticks([2021, 2022, 2023, 2024])  # Ensure all years are shown
plt.legend(title="County", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.grid(True)

# Show the plot
plt.show()


### Create a line plot for YoY
plt.figure(figsize=(12, 6))
sns.lineplot(data=df_county_yoy, x="YEAR", y="yoy_growth_rate", hue="COUNTY", marker="o")

# Customize the plot
plt.title("YoY Growth Rate by County (2022-2024)")
plt.xlabel("Year")
plt.ylabel("YoY Growth Rate (%)")
plt.xticks([2022, 2023, 2024])  # Ensure only relevant years are shown
plt.legend(title="County", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.grid(True)

#show the plot
plt.show()
