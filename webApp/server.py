import os
import pandas as pd
#from pandas.plotting import scatter_matrix
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
plt.ioff()
#import mpld3
#from mpld3 import plugins
from flask import Flask, request, json,  render_template,  session
import time
import pickle

app = Flask(__name__, static_url_path='/static')
app.secret_key = "wellwellwell"

dfcsv = pd.read_csv("OnlineRetail.csv",encoding = "ISO-8859-1")

global itemsDict
global emailList
global soloItem
dfuwc = pd.DataFrame() 


itemsDict = {}
emailList = []


@app.route('/',methods=['GET'])
def index():
   return render_template('base.html',
                          mainDrop = getMainDropDown() )
@app.route('/fill_first_table',methods = ['GET'])
def fillFirstTable():
   rows = dfcsv.shape[0]
   cols = dfcsv.shape[1]
   htmlOut = "<table><caption id = 'maintablecaption'> Data Before Cleaning (first 18 rows). Row Count = %s. Column Count= %s </caption></table> "% (rows,cols)
   htmlOut += dfcsv.head(18).to_html()
   return htmlOut



@app.route('/drop_unwanted_columns',methods = ['GET'])
def dropUnwamtedColumns():
   global dfuwc
   column_names = dfcsv.columns
   columns_to_drop = [column_names[i] for i in [0,1,4,5,7]]# Drop unwanted columns
   dfuwc = dfcsv.copy()
   dfuwc.drop(columns_to_drop, inplace=True, axis=1)
   rows = dfuwc.shape[0]
   cols = dfuwc.shape[1]
   htmlOut = "<table><caption id = 'maintablecaption'> Data After Unwanted Column Drop (first 20 rows). Row Count = %s. Column Count= %s </caption></table> "% (rows,cols)
   htmlOut += dfuwc.head(20).to_html()
   return htmlOut

@app.route('/remove_nans',methods = ['GET'])
def removeNans():
   #dfrn = dfuwc.copy()
   global dfuwc 
   dfuwc['CustomerID'].replace('  ', np.nan, inplace=True)
   dfuwc['Description'].replace('  ', np.nan, inplace=True)
   dfuwc['Quantity'].replace('  ', np.nan, inplace=True)
   dfuwc = dfuwc.dropna()
   rows = dfuwc.shape[0]
   cols = dfuwc.shape[1]
   htmlOut = "<table><caption id = 'maintablecaption'> Data After NaNs Removed (first 20 rows). Row Count = %s. Column Count= %s </caption></table> "% (rows,cols)
   htmlOut += dfuwc.head(20).to_html()
   return htmlOut

@app.route('/remove_negatives',methods = ['GET'])
def removeNegatives():
   #dfrn = dfuwc.copy()
   global dfuwc
   dfuwc = dfuwc.loc[dfuwc['Quantity']>=0]
   rows = dfuwc.shape[0]
   cols = dfuwc.shape[1]
   htmlOut = "<table><caption id = 'maintablecaption'> Data After Negatives Removed (first 20 rows). Row Count = %s. Column Count= %s </caption></table> "% (rows,cols)
   htmlOut += dfuwc.head(20).to_html()
   return htmlOut
@app.route('/adj_to_std',methods = ['GET'])
def adjTOStd():
   #dfrn = dfuwc.copy()
   global dfuwc
   dfuwc = dfuwc.loc[dfuwc['Quantity'] < dfuwc.loc[:,'Quantity'].std()]
   rows = dfuwc.shape[0]
   cols = dfuwc.shape[1]
   htmlOut = "<table><caption id = 'maintablecaption'> Data After STD Adjustment (first 20 rows). Row Count = %s. Column Count= %s </caption></table> "% (rows,cols)
   htmlOut += dfuwc.head(20).to_html()
   return htmlOut

@app.route('/dfuwc_stats1',methods = ['GET'])
def dfuwcStats1():
   #dfrn = dfuwc.copy()
   global dfuwc
   htmlOut = "<table><caption id = 'maintablecaptions'> Data After Unwanted Column Drop Describe  </caption></table> "
   htmlOut += dfuwc.describe().to_html()
   htmlOut += "<table><caption id = 'maintablecaptions'> Scatter Matrix Graph After Unwanted Column Drop  </caption></table> "
   htmlOut += "<div class = 'graphbox'><img src='/static/images/graph1.png' alt='' width='400' height='400'></div>"
   return htmlOut

@app.route('/dfuwc_stats2',methods = ['GET'])
def dfuwcStats2():
   #dfrn = dfuwc.copy()
   global dfuwc
   htmlOut = "<table><caption id = 'maintablecaptions'> Data After NaNs Removed Describe  </caption></table> "
   htmlOut += dfuwc.describe().to_html()
   htmlOut += "<table><caption id = 'maintablecaptions'> Scatter Matrix Graph After NaNs Removed   </caption></table> "
   htmlOut += "<div class = 'graphbox'><img src='/static/images/graph2.png' alt='' width='400' height='400'></div>"
   return htmlOut

@app.route('/dfuwc_stats3',methods = ['GET'])
def dfuwcStats3():
   #dfrn = dfuwc.copy()
   global dfuwc
   htmlOut = "<table><caption id = 'maintablecaptions'> Data After Negatives Removed Describe  </caption></table> "
   htmlOut += dfuwc.describe().to_html()
   htmlOut += "<table><caption id = 'maintablecaptions'> Scatter Matrix Graph After Negatives Removed   </caption></table> "
   htmlOut += "<div class = 'graphbox'><img src='/static/images/graph3.png' alt='' width='400' height='400'></div>"
   return htmlOut

@app.route('/dfuwc_stats4',methods = ['GET'])
def dfuwcStats4():
   #dfrn = dfuwc.copy()
   global dfuwc
   htmlOut = "<table><caption id = 'maintablecaptions'> Data After STD Adjustment  </caption></table> "
   htmlOut += dfuwc.describe().to_html()
   htmlOut += "<table><caption id = 'maintablecaptions'> Scatter Matrix Graph After STD Adjustment  </caption></table> "
   htmlOut += "<div class = 'graphbox'><img src='/static/images/graph4.png' alt='' width='400' height='400'></div>"
   return htmlOut


   
@app.route('/fill_main_table',methods = ['GET'])
def fillMainTable():
    item = request.args.get('item')
    session['itemx'] = item
    dfByItem = dfcsv.loc[(dfcsv['CustomerID'].notnull()) & (dfcsv['Description'] == item)]
    dfByItemSorted = dfByItem.sort_values(['CustomerID'], ascending=[False])

    #When item chosen from dropdown create dataframe with only that item.
    #soloItem = dfcsv.loc[(dfcsv['Description'] == item) & (dfcsv['CustomerID'].notnull()) ]

    #Get List of customers who purchased the chosen item.
    customerList = dfByItemSorted['CustomerID'].drop_duplicates().tolist()
    with open('outfile', 'wb') as fp:
       pickle.dump(customerList, fp)

    htmlOut = "<table><caption id = 'maintablecaption'>%s unfiltered table. Sales Count = %s. Total Customers = %s </caption></table> "% (item,len(dfByItem),len(customerList))
    htmlOut += dfByItemSorted.to_html()
    return htmlOut



@app.route('/fill_cust_table',methods = ['GET'])
def fillItemsTable():
   result = []
   tempDict = {}
   otherItemList = []
   item = request.args.get('item')

   customerList = []
   with open ('outfile', 'rb') as fp:
      customerList = pickle.load(fp)

   dfotherPur = dfcsv.loc[(dfcsv['CustomerID']).isin(customerList)]
   comb = dfotherPur.reset_index().groupby("Description").sum()
   comb = comb.loc[comb['Quantity']>0]
   dfItemsList = comb.drop(comb.columns[[0, 2, 3]], axis=1)
   dfItemsListSorted = dfItemsList.sort_values(['Quantity'], ascending=[False]).rename_axis(None)

   htmlOut = "<table><caption id = 'maintablecaption'>Other Items bought by Customers who purchased %s ____ Items Count = %s</caption></table> "% (item, len(dfItemsList))
   htmlOut += dfItemsListSorted.to_html()
   #htmlOut += dfItemsList.to_html()
   tempDict['custHtml'] = htmlOut
   htmlOut = ""
   statsDataframe = dfItemsList.describe(include='all')
   htmlOut = "<table><caption id = 'maintablecaption'>Statistics for %s </caption></table> "% (item)
   htmlOut += statsDataframe.to_html()
   tempDict['statsHtml'] = htmlOut
   result.append(tempDict)
   data = json.dumps(tempDict)
   return data

@app.route('/fill_stats_table',methods = ['GET'])
def fillStatsTable():
   statsDataframe = dfItemsList.describe(include='all')
   htmlOut = "<table><caption id = 'maintablecaption'>Statistics for %s </caption></table> "% (session['item'])
   htmlOut += statsDataframe.to_html()
   return htmlOut

@app.route('/fill_email_table',methods = ['GET'])
def fillEmailTable():
   item = request.args.get('item')
   customerList = []
   emailList = []
   dfBySecondItem = dfcsv.loc[(dfcsv['CustomerID'].notnull()) & (dfcsv['Description'] == item)]
   with open ('outfile', 'rb') as fp:
      customerList = pickle.load(fp)
   for cust in customerList:
       y = dfBySecondItem .loc[(dfBySecondItem ['CustomerID'] == cust)  ,['Description','Quantity']]
       if len(y) == 0:
           emailList.append(cust)
   dfemailList = pd.DataFrame(emailList).rename(columns={0:'Customer Email'})
   #dfemailListSorted = dfemailList.sort_values(['Customer Email'], ascending=[False])
   htmlOut = "<table><caption id = 'maintablecaption'>Emails For Customers who purchased %s and have not purchased %s  Count = %s from %s</caption></table> "% (session['itemx'],item, len(dfemailList),len(customerList))
   htmlOut += dfemailList.to_html()
   return htmlOut



##cnx=MySQLdb.connect(host = "localhost", user ="root", passwd="admin",db='play')
##cnx=MySQLdb.connect(sqlconfig)
def getMainDropDown():
    stringOut = """<select id = 'mainselect'>"""
    dfDropList =  dfcsv['Description'].drop_duplicates()
    dfDropListSorted = dfDropList.sort_values()
    for index, row in dfDropListSorted.iteritems():
       stringOut = stringOut + "<option value = '%s'>%s</option>"%(str(row),str(row))

##    cnx=MySQLdb.connect(host = "localhost", user ="root", passwd="admin",db='play')
##    with cnx:
##        cur = cnx.cursor(MySQLdb.cursors.DictCursor)#returns dictionary instead of default tuple
##        cur.callproc('getAllItems')
##        rows = cur.fetchall()
##        cur.close()
##        for row in rows
##            stringOut = stringOut + "<option value = '%s'>%s</option>"%(row['item_name'],row['item_name'])

    stringOut = stringOut + """</select><span id ='choose'> Data Cleansing</span> </select><span id ='toggle'>| Goto Item Comparitor |</span>"""

    return stringOut

if __name__ == "__main__":
    app.run( port=5002, debug=True)
