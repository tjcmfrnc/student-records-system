import sqlite3 as sql
from flask import Flask, render_template, request


app = Flask(__name__)

conn = sql.connect('testbase2.db')
print "db opened"

conn.execute('CREATE TABLE IF NOT EXISTS students (idno TEXT PRIMARY KEY, firstname TEXT, middlename TEXT, lastname TEXT, sex TEXT, courseid INTEGER, FOREIGN KEY(courseid) REFERENCES courses(cid) ON DELETE CASCADE ON UPDATE CASCADE)')
conn.execute('CREATE TABLE IF NOT EXISTS courses (cid INTEGER PRIMARY KEY, coursename TEXT, coursecode TEXT)')


print "table created"
conn.close()


class Student(object):
    def __init__(self, idNum, firstName, middleName, lastName, sex, courseID):
        self.id = idNum
        self.fn = firstName
        self.mn = middleName
        self.ln = lastName
        self.sex = sex
        self.cid = courseID

class Course(object):
    def __init__(self, courseID, courseName, courseCode):
        self.cno=courseID
        self.cname=courseName
        self.cc=courseCode

@app.route('/')
def home():
    return render_template('home1.html')

@app.route('/addnew', methods=['GET', 'POST'])
def addnew():
    return render_template('addstud.html')

@app.route('/addrec', methods=['GET', 'POST'])
def addrec():
    if request.method == 'POST':
        try:
            id = request.form['id']
            fn = request.form['fn']
            mn = request.form['mn']
            ln = request.form['ln']
            sex = request.form['sex']
            cid = request.form['cid']

            student = Student(id, fn, mn, ln, sex, cid)
            with sql.connect("testbase2.db") as con:
                cur1 = con.cursor()
                cur1.execute("SELECT * FROM courses WHERE cid = ? ", (cid,))
                query = cur1.fetchone()
                print query
                if query is None:
                    msg='Course does not exist!'
                else:
                    cur = con.cursor()
                    cur.execute("INSERT INTO students (idno,firstname,middlename,lastname,sex,courseid) "
                            "VALUES (?,?,?,?,?,?)",
                            (student.id, student.fn, student.mn, student.ln, student.sex, student.cid))
                    con.commit()
                    msg = "Record added successfully!"
        except:
            con.rollback()
            msg = "Error in adding. Try again."

        finally:
            return render_template('result.html', msg=msg)
            con.close()

@app.route('/updatenew', methods=['GET', 'POST'])
def updatenew():
    return render_template('updatestud.html')

@app.route('/updaterec', methods=['GET', 'POST'])
def updaterec():
    if request.method == 'POST':
        try:
            id = request.form['id']
            fn = request.form['fn']
            mn = request.form['mn']
            ln = request.form['ln']
            sex = request.form['sex']
            cid = request.form['cid']

            with sql.connect("testbase2.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM students")

                for row in cur.fetchall():
                    if row[0] == id:
                        cur.execute("UPDATE students SET firstname = ?, middlename = ?, lastname = ?, sex = ?, courseid = ? WHERE idno = ?", (fn, mn, ln, sex, cid, id,))
                        con.commit()
                        msg = "Record updated!"
                        break
                    else:
                        msg = "Error! Student not found!"
                else:
                    msg = "Update error. Try again."
        except:
            con.rollback()
            msg = "Update error. Try again."

        finally:
            return render_template('result.html', msg=msg)
            con.close()

@app.route('/deletenew', methods=['GET', 'POST'])
def deletenew():
    return render_template('deletestud.html')

@app.route('/deleterec', methods=['GET', 'POST'])
def deleterec():
    if request.method == 'POST':
        try:
            id = request.form['id']

            with sql.connect("testbase2.db") as con:
                cur = con.cursor()
                cur.execute('DELETE FROM students WHERE idno = ?', (id,))
                con.commit()
                msg = "Record successfully deleted!"
        except:
            con.rollback()
            msg = "Cannot delete. Try again."
        finally:
            return render_template('result.html', msg=msg)
            con.close()

@app.route('/studentlist')
def studentlist():
    con = sql.connect("testbase2.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from students")

    rows = cur.fetchall()
    return render_template('list.html', rows=rows)

@app.route('/searchstudent', methods = ['GET', 'POST'])
def searchstudent():
    return render_template('searching.html')

@app.route('/searchrec', methods = ['GET', 'POST'])
def searchrec():
    if request.method == 'POST':
        try:
            data = request.form['data']

            with sql.connect('testbase2.db') as con:
                cur1 = con.cursor()
                cur1.execute('SELECT idno, firstname, middlename, lastname, sex, cid, coursename, coursecode FROM '
                             'students INNER JOIN courses ON students.courseid = courses.cid WHERE idno = ?', (data,))
                row1 = cur1.fetchall()

                cur2 = con.cursor()
                cur2.execute('SELECT idno, firstname, middlename, lastname, sex, cid, coursename, coursecode FROM '
                             'students INNER JOIN courses ON students.courseid = courses.cid WHERE firstname = ?', (data,))
                row2 = cur2.fetchall()

                cur3 = con.cursor()
                cur3.execute('SELECT idno, firstname, middlename, lastname, sex, cid, coursename, coursecode FROM '
                             'students INNER JOIN courses ON students.courseid = courses.cid WHERE lastname = ?',
                             (data,))
                row3 = cur3.fetchall()

                cur4 = con.cursor()
                cur4.execute('SELECT idno, firstname, middlename, lastname, sex, cid, coursename, coursecode FROM '
                             'students INNER JOIN courses ON students.courseid = courses.cid WHERE coursename = ?',
                             (data,))
                row4 = cur4.fetchall()

                cur5 = con.cursor()
                cur5.execute('SELECT idno, firstname, middlename, lastname, sex, cid, coursename, coursecode FROM '
                             'students INNER JOIN courses ON students.courseid = courses.cid WHERE coursecode = ?',
                             (data,))
                row5 = cur5.fetchall()

                cur6 = con.cursor()
                cur6.execute('SELECT idno, firstname, middlename, lastname, sex, cid, coursename, coursecode FROM '
                             'students INNER JOIN courses ON students.courseid = courses.cid WHERE sex = ?',
                             (data,))
                row6 = cur6.fetchall()

                msg = "Valid search detected. Results that have keyword '%s': " %data
                result = row1+row2+row3+row4+row5+row6
        except:
            con.rollback()
            msg = "Search error detected. Try again."
        finally:
            return render_template('searchlist.html', msg=msg, rows=result)
            con.close()

@app.route('/addcourse', methods=['GET', 'POST'])
def addcourse():
    return render_template('coursenew.html')

@app.route('/courseadd', methods=['GET', 'POST'])
def courseadd():
    if request.method == 'POST':
        try:
            cno = request.form['cno']
            cname = request.form['cname']
            cc = request.form['cc']

            course = Course(cno, cname, cc)
            with sql.connect("testbase2.db") as con:
                if cno.isdigit():
                    cur = con.cursor()
                    cur.execute("INSERT INTO courses (cid, coursename, coursecode) VALUES (?,?,?)", (course.cno, course.cname, course.cc))
                    con.commit()
                    msg = "Course added successfully!"
                else:
                    msg = "Error in adding. Try again."
        except:
            con.rollback()
            msg = "Error in adding. Try again."

        finally:
            return render_template('result.html', msg=msg)
            con.close()


@app.route('/updatecourse', methods=['GET', 'POST'])
def updatecourse():
    return render_template('courseup.html')

@app.route('/courseupdate', methods=['GET', 'POST'])
def courseupdate():
    if request.method == 'POST':
        try:
            cno = request.form['cno']
            cname = request.form['cname']
            cc = request.form['cc']

            with sql.connect("testbase2.db") as con:
                if cno.isdigit():
                    cur = con.cursor()
                    cur.execute("UPDATE courses SET coursename = ?, coursecode = ? WHERE cid = ?", (cname,cc,cno,))
                    con.commit()

                    msg = "Record updated!"
                else:
                    msg = "Update error. Try again."
        except:
            con.rollback()
            msg = "Update error. Try again."
        finally:
            return render_template('result.html', msg=msg)
            con.close()

@app.route('/deletecourse', methods=['GET', 'POST'])
def deletecourse():
    return render_template('coursedelete.html')

@app.route('/coursedel', methods=['GET', 'POST'])
def coursedel():
    if request.method == 'POST':
        try:
            cno = request.form['cno']
            if cno.isdigit():
                with sql.connect("testbase2.db") as con:
                    cur = con.cursor()
                    cur.execute('DELETE FROM courses WHERE cid = ?', (cno,))
                    con.commit()
                    msg = "Course successfully deleted!"
            else:
                msg = "Cannot delete. Try again."
        except:
            con.rollback()
            msg = "Cannot delete. Try again."
        finally:
            return render_template('result.html', msg=msg)
            con.close()

@app.route('/courselist')
def list():
    con = sql.connect("testbase2.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from courses")

    rows = cur.fetchall()
    return render_template('clist.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
    app.static_folder = 'static'
