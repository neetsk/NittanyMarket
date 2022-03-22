from flask import Flask, render_template, request
import sqlite3 as sql
from populateDatabase import populate

# Populates Database with starting data
populate()

'''
app = Flask(__name__)

host = 'http://127.0.0.1:5000/'

con = sql.connect("NittanyMarket.db")
'''

"""
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/name', methods=['POST', 'GET'])
def name():
    error = None
    if request.method == 'POST':
        result = valid_name(request.form['FirstName'], request.form['LastName'])
        if result:
            return render_template('input.html', error=error, result=result)
        else:
            error = 'invalid input name'
    return render_template('input.html', error=error)


def valid_name(first_name, last_name):
    connection = sql.connect('database.db')
    connection.execute('CREATE TABLE IF NOT EXISTS users(firstname TEXT, lastname TEXT);')
    connection.execute('INSERT INTO users (firstname, lastname) VALUES (?,?);', (first_name, last_name))
    connection.commit()
    cursor = connection.execute('SELECT * FROM users;')
    return cursor.fetchall()

"""

"""
if __name__ == "__main__":
    app.run()
"""


#Drop tables so program can be reloaded
#and duplicate values are not loaded
#cur.execute('''DROP TABLE IF EXISTS Emp''')

#Create Tables
#cur.execute('''CREATE TABLE Emp (eid INTEGER, ename STRING, age INTEGER, salary REAL
#    ,PRIMARY KEY (eid))''')

#cur.execute('''CREATE TABLE Works (eid INTEGER, did INTEGER, pct_time INTEGER, FOREIGN KEY (eid) REFERENCES Emp)''')

#cur.execute('''CREATE TABLE Dept (did INTEGER, budget REAL, managerid INTEGER
#    ,FOREIGN KEY (did) REFERENCES Works)''')

#Read data from file into list
#dataset = open("Homework5-dataset-sp2022.txt", 'r')
#dataList = dataset.readlines()

#empList = []
#worksList = []
#deptList = []

#empFlag = False
#worksFlag = False
#deptFlag = False

#Parse data from lists into each view
#for x in dataList:
#    if empFlag and x.strip() != '':
#        empList.append(x.strip().replace("'", ''))
#    elif worksFlag and x.strip() != '':
#        worksList.append(x.strip().replace("'", ''))
#    elif deptFlag and x.strip() != '':
#        deptList.append(x.strip().replace("'", ''))

#    if "Emp" in x:
#        empFlag = True
#        worksList.pop()
#    elif "Works" in x:
#        empFlag = False
#        worksFlag = True
#        empList.pop()
#    elif "Dept" in x:
#        worksFlag = False
#        deptFlag = True

#Put items from empList into our database
#for x in empList:
#    tempList = x.split(',')
#    tempList[0] = int(tempList[0])
#    tempList[2] = int(tempList[2])
#    tempList[3] = float(tempList[3])
#
#    cur.execute('''INSERT INTO Emp (eid, ename, age, salary) VALUES (?,?,?,?)''',(tempList[0],
#        tempList[1], tempList[2], tempList[3]))

#put items from worksList into our works table
#for x in worksList:
#    tempList = x.split(',')
#    tempList[0] = int(tempList[0])
#    tempList[1] = int(tempList[1])
#    tempList[2] = int(tempList[2])

#    cur.execute('''INSERT INTO Works (eid, did, pct_time) VALUES (?,?,?)''', (tempList[0],
#        tempList[1], tempList[2]))

#put items from deptList into our dept table
#for x in deptList:
#    tempList = x.split(',')
#    tempList[0] = int(tempList[0])
#    tempList[1] = float(tempList[1])
#    tempList[2] = int(tempList[2])

#    cur.execute('''INSERT INTO Dept (did, budget, managerid) VALUES (?,?,?)''', (tempList[0],
#        tempList[1], tempList[2]))

#Confirm values are in the table
#print('Task 1')
#cur.execute('''SELECT * FROM Emp''')
#print(cur.fetchall())
#cur.execute('''SELECT * FROM Works''')
#print(cur.fetchall())
#cur.execute('''SELECT * FROM Dept''')
#print(cur.fetchall())

#Queries for Task 2
#Query 1
#cur.execute('''SELECT E.ename, E.salary FROM Emp E, Works W1, Works W2
#    WHERE E.eid = W1.eid and E.eid = W2.eid and W1.did = 0 and W2.did = 2''')

#print('\n\nTask 2')
#print('1: ', cur.fetchall())

#Query 2
#cur.execute('''SELECT E.ename, E.salary, E.age, MIN(E.eid) AS minage FROM Emp E, Works W
#    WHERE E.eid = W.eid GROUP BY W.did''')
#print('2: ', cur.fetchall())

#Query 3
#cur.execute('''SELECT E.ename, MAX(D.budget) AS maxbudget FROM Emp E, Works W, Dept D
#    WHERE E.eid = W.eid and W.did = D.did and D.managerid = E.eid''')
#print('3: ', cur.fetchall())

#Query 4
#cur.execute('''SELECT W1.did, MAX(maxbudget) FROM Works W1, (SELECT W2.did, AVG(E.salary) AS maxbudget FROM Emp E, Works W2, Dept D
#    WHERE E.eid = W2.eid and W2.did = D.did GROUP BY W2.did)''')
#print('4: ', cur.fetchall())

#Query 5
#cur.execute('''SELECT DISTINCT E1.ename, E1.salary FROM Emp E1, Works W1, (SELECT E2.ename, MIN(E2.salary) as minmanagersalary FROM Emp E2, Works W2, Dept D
#    WHERE E2.eid = W2.eid and W2.did = D.did and D.managerid = E2.eid) WHERE E1.eid = W1.eid and E1.salary > minmanagersalary''')
#print('5: ', cur.fetchall())

#close file and commit changes to db
#dataset.close()
#con.commit()

