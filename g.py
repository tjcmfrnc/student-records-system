class student:
    def __init__(self,firstName,lastName,age,idnumber,course,gender):
        self.age = age
        self.idnumber = idnumber
        self.firstName = firstName
        self.lastName = lastName
        self.course = course
        self.gender = gender

        
def add (firstName, lastName, idnumber, age, gender, course):
    f = open ('info.csv','a')
    
    f.write(idnumber + ",")
    f.write (firstName + ",")
    f.write (lastName + ",")
    f.write (age + ",")
    f.write (gender + ",")
    f.write (course + "\n")
    f.close ()

def checker (idnumber):
    f = open ('info.csv','r')
    counter = 0
    for line in f:
        currentline = line.split (",")
        if (currentline [0] == idnumber):
            counter = 1
    f.close ()
    if(counter == 1):
        return True
    else:
        return False
    
def search (idnumber):
    if (checker (idnumber) == False):
        print ("\nERROR: Id number does not exist")
        pass        
    else:
        f = open ('info.csv','r')
        for line in f:
            currentline = line.split (",")
            if (currentline [0] == idnumber):
                print ('ID number:'+currentline[0])
                print ('Firstname: '+currentline [1])
                print('Lastname: '+currentline [2])
                print('Age: '+currentline [3])
                print ('Gender: '+currentline [4])
                print ('Course: '+currentline [5])
        f.close ()
    
def update(idnumber):
    if (checker (idnumber) == False):
        print ("\nERROR: Id number does not exist")
        pass
    else:
        storage  = []
        f = open ('info.csv','r')
        choice = raw_input ('what  you want to update?\n(idnumber/firstname/lastname/age/gender/course): ')
        for line in f:       
            currentline = line.split(",")
            if(currentline [0] == idnumber):
                    if (choice == 'idnumber'):
                        newID= raw_input ('Enter the new ID number: ')
                        storage.append(newID+ ","+currentline[1]+","+currentline [2]+","+currentline [3]+","+currentline [4]+","+currentline [5])
                    elif (choice == 'firstname'):
                        newfirstname = raw_input ('Enter the new firstname: ')
                        storage.append(currentline [0]+ ","+newfirstname+","+currentline [2]+","+currentline [3]+","+currentline [4]+","+currentline [5])
                    elif(choice == 'lastname'):
                        newlastname = raw_input ('Enter the new lastname: ')
                        storage.append(currentline [0]+ ","+currentline[1]+","+newlastname+","+currentline [3]+","+currentline [4]+","+currentline [5])
                    elif(choice == 'age'):
                        newage = raw_input ('Enter the new age: ')
                        storage.append(currentline [0]+ ","+currentline[1]+","+currentline [2]+","+newage+","+currentline [4]+","+currentline [5])
                    elif (choice == 'gender'):
                        newgender = raw_input ('Enter the new gender: ')
                        storage.append(currentline[0]+ ","+currentline[1]+","+currentline [2]+","+currentline [3]+","+newgender+","+currentline [5]) 
                    elif (choice == 'course'):
                        newcourse = raw_input('Enter the new course: ')
                        storage.append(currentline[0]+ ","+currentline[1]+","+currentline [2]+","+currentline [3]+","+currentline [4]+","+newcourse+"\n")
            else:
                storage.append (line)       
        f.close ()
        f = open("info.csv","w")
        for l in storage:
            f.write(l)
        f.close()
    
def delete(idnumber):
    if (checker (idnumber) == False):
        print ("\nERROR: Id number does not exist")
        pass
    else:
        storage = []
        f = open("info.csv","r")
        for line in f:
            currentline = line.split (",")
            if (currentline[0] != idnumber):
                storage.append (line)
        f.close ()
        f = open ("info.csv","w")
        for l in storage:
            f.write (l)
        f.close ()

def oper():
    print ("Choose an Operations:\n \nPress [1] for :Add info\nPress [2] for :Update info\nPress [3] for :Search info\nPress [4] for :Delete info\n")
    	
    
print("\n------Welcome------Welcome------Welcome------Welcome------Welcome-------\n")

while (True):
    oper()
    operations = raw_input('Enter an Operation: ')
    
    if (operations == '1'):
        firstname = raw_input('Enter firstname: ')
        lastname = raw_input('Enter lastname: ')
        idnumber = raw_input('Enter id number: ')
        gender = raw_input('Enter gender: ')
        age = raw_input('Enter age: ')
        course = raw_input('Enter course: ')
        
        stud = student (firstname,lastname,age,idnumber,course,gender)
        add (stud.firstName,stud.lastName,stud.idnumber,stud.age,stud.gender,stud.course)

    elif (operations == '3'):
        searchid = raw_input ('Enter the id no.: ')
        search (searchid)  
        
    elif (operations == '2'):
        searchid = raw_input ('Enter the id number: ')
        update(searchid)
        print(".....Updated Successfully...!!")
    elif (operations == '4'):
        searchid = raw_input ('Enter the id no.: ')
        delete(searchid)     
 
    choice = raw_input("\nWant to try again? y/n: ")
    if (choice == "n"):
            break