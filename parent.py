	
# Load libraries
import pandas as pd
import numpy as np
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

# Load dataset
file_path = "OnlineRetail.csv"
pd.set_option('display.expand_frame_repr', False)
dataset = pd.read_csv(file_path, encoding = "ISO-8859-1")

### shape
print("************ Shape ******************")
print(dataset.shape)
##print("*********************************************************")
### head
##print("************ Head Firat 20 Rows ******************")
##print(dataset.head(20))
##print("*********************************************************")
##
### descriptions
##print("************ Descriptions ******************")
##print(dataset.describe())
##print("*********************************************************")
##
### class distribution
##print("************ Description Distributions ******************")
##print(dataset.groupby('Description').size())
##print("*********************************************************")

#Clean the data base. Remove Unwanted Columns, Remove NaNs, Add index
df = dataset

# Create list comprehension of the columns you want to lose
#['InvoiceNo', 'StockCode','InvoiceDate','UnitPrice','Country']
column_names = df.columns
print(column_names)

columns_to_drop = [column_names[i] for i in [0, 1,4,5,7]]# Drop unwanted columns
df.drop(columns_to_drop, inplace=True, axis=1)
print(df.head(20))
scatter_matrix(df)
#plt.title("Data After Unwanted Column Drop", color='g')
plt.show()

#Remove Nulls and NaNs

df['CustomerID'].replace('  ', np.nan, inplace=True)
df['Description'].replace('  ', np.nan, inplace=True)
df['Quantity'].replace('  ', np.nan, inplace=True)


# Drop any rows which have any nans
print()
print(" Shape before NsN removal ")
print(df.shape)
df= df.dropna(subset=['CustomerID'])
df= df.dropna(subset=['Description'])
df= df.dropna(subset=['Quantity'])
print()
print(" Shape after NaN removal ")
print(df.shape)
scatter_matrix(df)
#plt.title("Data after NaN removal", color='g')
plt.show()

# Check the index values
print(df.index.values)
#df.set_index('column_name_to_use', inplace=True)


# Remove Negative Quantities
df = df.loc[df['Quantity']>=0]
print()
print(" Shape df['Quantity']>=0")
print(df.shape)
print()
print(" Describe df['Quantity']>=0")
print(df.describe())

scatter_matrix(df)
#plt.title("Data After Negatives Removed", color='g')
plt.show()

# Remove Quantities above Standard Deviation
df = df.loc[df['Quantity'] < df.loc[:,'Quantity'].std()]
print()
print(" Shape df.['Quantity'] > df.loc[:,'Quantity'].std()")
print(df.shape)
print()
print(" Describe df.['Quantity'] > df.loc[:,'Quantity'].std()")
print(df.describe())
scatter_matrix(df)
#plt.title("Data After STD Adjustment", color='g')
plt.show()




#Data Visualization of Original Dataset (Univariate Plots)

# box and whisker plots
dataset.plot(kind='box', subplots=True, layout=(1,2), sharex=False, sharey=False)
plt.title("Data Before Data Cleansing\n", color='g')
plt.show()

# histograms
dataset.hist()
plt.title("Data Before Data Cleansing\n", color='g')
plt.show()

# scatter plot matrix
scatter_matrix(dataset)
plt.title("Data Before Data Cleansing\n", color='g')
plt.show()

#Data Visualization of Cleaned (Univariate Plots)

# box and whisker plots
df.plot(kind='box', subplots=True, layout=(1,2), sharex=False, sharey=False)
plt.title("Data After Data Cleansing\n", color='g')
plt.show()

# histograms
df.hist()
plt.title("Data After Data Cleansing\n", color='g')
plt.show()

# scatter plot matrix
#scatter_matrix(df)
#plt.title("Data After Data Cleansing", color='g')
#plt.show()

# Make Dataframe with only one choosen Item
# WHITE METAL LANTERN

itemxDF = df.loc[df['Description'] == 'WHITE METAL LANTERN']
print(itemxDF.head(20))
print(itemxDF.describe())
itemGroupByCustomerId = itemxDF.groupby('CustomerID', as_index=False).agg({'Quantity':'sum'}).sort_values('Quantity', ascending=False)
print(itemGroupByCustomerId.head(20))
print(itemGroupByCustomerId.describe())
custIDdf = itemGroupByCustomerId.loc[itemGroupByCustomerId['CustomerID'] ==16779.0]
print(custIDdf.head(20))
print(custIDdf.describe())

# Make Dataframe with only one choosen Item
# ASSORTED COLOUR BIRD ORNAMENT

itemyDF = df.loc[df['Description'] == 'ASSORTED COLOUR BIRD ORNAMENT']
print(itemyDF.head(20))
print(itemyDF.describe())
itemyGroupByCustomerId = itemyDF.groupby('CustomerID', as_index=False).agg({'Quantity':'sum'}).sort_values('Quantity', ascending=False)
print(itemyGroupByCustomerId.head(20))
print(itemyGroupByCustomerId.describe())
custIDydf = itemyGroupByCustomerId.loc[itemyGroupByCustomerId['CustomerID'] ==16779.0]
print(custIDydf.head(20))
print(custIDydf.describe())

# Make Comparison Dataframes of
# WHITE METAL LANTERN ,ASSORTED COLOUR BIRD ORNAMENT
df_merge = pd.merge(itemGroupByCustomerId, itemyGroupByCustomerId, left_on='CustomerID',right_on='CustomerID',how='outer',suffixes=('_left','_right'))
df_merge = df_merge.fillna(0)
print('************* BASIC OUTER MERGE ****************')
print(df_merge.head(20))
print(df_merge.describe())
# scatter plot matrix
scatter_matrix(df_merge)
plt.title("Comparison of two merged Items\n", color='g')
plt.show()
# box and whisker plots
df_merge.plot(kind='box', subplots=True, layout=(2,2), sharex=False, sharey=False)
plt.title("Comparison of two merged Items\n", color='g')
plt.show()
# Percentage/ratio of itemX to itemY
seriesxObj = df_merge.apply(lambda x: True if x['Quantity_right'] > 0 else False , axis=1)
seriesyObj = df_merge.apply(lambda x: True if x['Quantity_right'] == 0 else False , axis=1)
#countall = df_merge[df_merge['Quantity_right'] >= 0].count()
countx = len(seriesxObj[seriesxObj == True].index)
county = len(seriesyObj[seriesyObj == True].index)
print('************* Percentage Brakedown *************')
print('countx = '+ str(countx))
print('county = '+ str(county))


df_inner = pd.merge(itemGroupByCustomerId, itemyGroupByCustomerId, how = 'inner')
print('************* INNER ****************')
print(df_inner.head(20))
print(df_inner.describe())


print("All Done")
