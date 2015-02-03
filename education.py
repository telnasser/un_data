import pandas as pd
from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import sqlite3 as lite



url = "http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm"

r = requests.get(url)
soup = BeautifulSoup(r.content)

# Got this form the table structure via "inspect element" 
table = soup.find('table', {"align":"left"})

i = 0

df = pd.DataFrame(columns = ('Country/Area','Year','Total', 'Men', 'Women'))

for row in table.findAll('tr')[4:]:
        col = row.findAll('td')
        # I faced unicode errors. I've encoded it in utf-8 to avoid that.
        df.loc[i] = [col[0].text.encode('utf-8'), col[1].text.encode('utf-8'),col[4].text.encode('utf-8'),col[7].text.encode('utf-8'),col[10].text.encode('utf-8')]
        i +=1

        # for xx in col:
        #       i+=1
        #       print i, xx.text.encode('utf-8')

# Convert the proper type for int columns
df['Men'] = df['Men'].astype(int)
df['Women'] = df['Women'].astype(int)
df['Total'] = df['Total'].astype(int)

# Establish the connection with the datrabase and create the table. If it's already exists, it'll drop and create a new one!

con = lite.connect('un_data.db')
cur = con.cursor()
# with con:
#     cur.execute('CREATE TABLE education_indicators ( country TEXT,  year int, total int, men int, women int);') 

# I'm changing the column name of country to be something acceptable by the Database
df.rename(columns={'Country/Area': 'country'}, inplace=True)

# Dropping the table
con.execute("DROP TABLE IF EXISTS education_indicators;")

# I faced a problem inserting unicode text to the table. I overcome this by setting the connection to str
con.text_factory = str 

# Inserting the DataFrame data into the table
df.to_sql('education_indicators', con,  if_exists='replace')

df['Men'].hist()
plt.show()

df['Women'].hist()
plt.show()

df['Total'].hist()
plt.show()

### Getting data from UN and inserting it to a database. I used pandas read_csv instead of the method instructed

un_df = pd.read_csv('ny.gdp.mktp.cd_Indicator_en_csv_v2.csv', skiprows = 2)
con.execute("DROP TABLE IF EXISTS gdp;")
un_df.to_sql('gdp', con, if_exists'replace') # note that you can access the column names with [xxx] 

df2 = pd.read_sql_query('select Men, Women, [1999], [2000], [2001], [2002], [2003], [2004], [2005], [2006], [2007], [2008], [2009], [2010] from education_indicators inner join gdp on country = [Country Name] ', con)


##  df2[df_val] = df2[df_val].map(lambda x: math.log(x))
# putting it in a loop did not work and gave me: KeyError: "'1999'"

df2['1999'] = df2['1999'].map(lambda x: math.log(x))
df2['2000'] = df2['2000'].map(lambda x: math.log(x))
df2['2001'] = df2['2001'].map(lambda x: math.log(x))
df2['2002'] = df2['2002'].map(lambda x: math.log(x))
df2['2003'] = df2['2003'].map(lambda x: math.log(x))
df2['2004'] = df2['2004'].map(lambda x: math.log(x))
df2['2005'] = df2['2005'].map(lambda x: math.log(x))
df2['2006'] = df2['2006'].map(lambda x: math.log(x))
df2['2007'] = df2['2007'].map(lambda x: math.log(x))
df2['2008'] = df2['2008'].map(lambda x: math.log(x))
df2['2009'] = df2['2009'].map(lambda x: math.log(x))
df2['2010'] = df2['2010'].map(lambda x: math.log(x))

df2.plot()
plt.show

