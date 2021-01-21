import csv
from sklearn import tree
from sklearn import preprocessing
import mysql.connector
x = []
y = []
cnx = mysql.connector.connect(user='behafarin', password='127281', host='localhost',
                              database='shabesh', charset='utf8', auth_plugin='mysql_native_password')
cursor = cnx.cursor()
query = 'select * from Tehran'
cursor.execute(query)
cnx.close()
le = preprocessing.LabelEncoder()
records = cursor.fetchmany(2500)
for row in records:
    x.append(list(row[0:3]))
    y.append(row[3])

locations = [s[0] for s in x]
le.fit(locations)
for i in range(len(x)):
    x[i][0] = (le.transform([x[i][0]]))[0]
clf = tree.DecisionTreeClassifier()
clf = clf.fit(x, y)
loc = input('Enter your willing location: ')
area = input('area: ')
room = input('room number: ')
le.fit(list(loc))
loc = le.transform(list(loc))[0]
new_data = [loc, area, room]
answer = clf.predict([new_data])
print('قیمت تخمینی: ', answer[0])
