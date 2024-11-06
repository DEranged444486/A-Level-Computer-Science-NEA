import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import Text, Tk
import numpy as np

# creating the sql database which will be used in the final program. 
con = sqlite3.connect("AcademicTrackerDB.db") 
cur = con.cursor() # creates a cursor object that will be used to execute SQL commands and fetches on the database in the python program.
cur.execute("""CREATE TABLE IF NOT EXISTS StudentDetails (StudentID INTEGER PRIMARY KEY,
            TeacherID INTEGER NOT NULL,
            DataID INTEGER NOT NULL,
            InformationID INTEGER NOT NULL,
            StudentUsername TEXT NOT NULL,
            StudentPassword TEXT NOT NULL,
            StudentName TEXT NOT NULL,
            StudentSurname TEXT NOT NULL,
            FOREIGN KEY(DataID) REFERENCES AcademicData(DataID) ON UPDATE CASCADE,
            FOREIGN KEY(InformationID) REFERENCES AcademicInformation(InformationID) ON UPDATE CASCADE
            FOREIGN KEY(TeacherID) REFERENCES TeacherLoginDetails(TeacherID) ON UPDATE CASCADE)""") 
cur.execute("""CREATE TABLE IF NOT EXISTS TeacherDetails (TeacherID INTEGER PRIMARY KEY,
            TeacherUsername TEXT NOT NULL,
            TeacherPassword TEXT NOT NULL,
            TeacherName TEXT NOT NULL,
            TeacherSurname TEXT NOT NULL)""")
cur.execute("""CREATE TABLE IF NOT EXISTS AcademicData (DataID INTEGER PRIMARY KEY,
            AverageTestScore INTEGER,
            StudentContextualData INTEGER,
            StudentParticipationGrade INTEGER,
            StudentClassParticipationGrade INTEGER,
            StudentBehaviourGrade INTEGER,
            AttendanceRate REAL,
            MaximumMarkAchieved INTEGER,
            MinimumMarkAchieved INTEGER,
            AmountOfMocksCompleted INTEGER)""")
cur.execute("""CREATE TABLE IF NOT EXISTS AcademicInformation (InformationID INTEGER PRIMARY KEY,
            TeacherFeedback TEXT,
            ComputerGeneratedFeedback TEXT,
            MedianMarkAchieved REAL,
            MeanMarkAchieved REAL,
            PredictedMark INTEGER,
            PredictedGrade INTEGER,
            StabilityOfCurrentGrade TEXT NOT NULL,
            StudentOverallEngagementGrade TEXT NOT NULL,
            StudentComment TEXT)""")
#creates all the tables needed for the program if they do not already exist.    

#creating fake student sample data
StudentSampleData = [
    (1,1,1,1,'','','John','Smith'),
    (0,2,2,2,'','','Lukas','Birgeris'),
    (1,3,3,3,'','','jamie','Culver'),
    (1,4,4,4,'','','Tom','French'),
    (2,5,5,5,'','','benjamin','Sanger')
]
#inserting student sample data into the StudentDetailsTable
cur.executemany("INSERT OR REPLACE INTO StudentDetails VALUES (?,?,?,?,?,?,?,?)", StudentSampleData)

TeacherSampleData = [
    (1,'','','Bob','ross'),
    (2,'','','jiachen','Lin'),
    (3,'','','Emily','Smith'),
    (4,'','','Fred','Chen')
]
#inserting data
cur.executemany("INSERT OR REPLACE INTO TeacherDetails VALUES (?,?,?,?,?)", TeacherSampleData)

AcademicSampleData = [
    (0,'50','','9','9','9','99','50','30','7'),
    (1,'40','','7','6','5','75','94','82','6'),
    (2,'60','','4','3','2','85','20','0','2'),
    (3,'75','','5','5','5','98','20','15','5'),
    (4,'70','','1','1','1','10','10','0','4')
]
cur.executemany("INSERT OR REPLACE INTO AcademicData VALUES(?,?,?,?,?,?,?,?,?,?)", AcademicSampleData)

#commit changes
con.commit()
#terminate connection
con.close()

# this is the TeacherGUI function, this will be executed if a Teacher sucessfully logins onto the system. 
def TeacherGUI(UsernameInput, PasswordInput):
    #defining the window
    TeacherName = ('SELECT TeacherName WHERE TeacherUsername =',UsernameInput)
    TeacherSurname = ('SELECT TeacherSurname WHERE TeacherUsername =',UsernameInput)
    Teacher = TeacherName + ' ' + TeacherSurname
    TeacherWindow = tk.Tk()
    TeacherWindow.attributes('-fullscreen', True)
    TeacherWindow.title(Teacher + ''''s student data''')   

    #defining the functions to be used as commands for the Next and Back Buttons
    def Page3():
        table2.pack_forget()
        NextButton2.pack_forget()
        BackButton.pack_forget()
        table3.pack(fill = tk.BOTH)
        BackButton2.pack(fill = tk.BOTH)

    def Page2():
        table3.pack_forget()
        BackButton2.forget()
        table1.pack_forget()
        NextButton.pack_forget()
        table2.pack(fill = tk.BOTH)
        NextButton2.pack(fill = tk.BOTH)
        BackButton.pack(fill = tk.BOTH)
    def Page1():
        table2.pack_forget()
        BackButton.pack_forget()
        NextButton2.pack_forget()
        table1.pack(fill = tk.BOTH)
        NextButton.pack(fill = tk.BOTH)



        
    #defining the widgets
    #creating the first page's table and formatting it
    table1 = ttk.Treeview(TeacherWindow, columns = ('StudentID','Name','Surname','AverageTestScore','StudentContextualData',
                                            'StudentParticipationGrade'), show = 'headings')
    table1.heading('StudentID', text = 'StudentID')
    table1.heading('Name', text='Name')
    table1.heading('Surname',text ='Surname')
    table1.heading('AverageTestScore',text='AverageTestScore')
    table1.heading('StudentContextualData',text= 'StudentContextualData')
    table1.heading('StudentParticipationGrade', text='StudentParticipationGrade')
    table1.pack(fill = tk.BOTH)

    #inserting data into the table 1
    conn = sqlite3.connect('AcademicTrackerDB.db')
    cur = conn.cursor()
    cur.execute('''SELECT StudentID, StudentName, StudentSurname,  
                AverageTestScore, StudentContextualData, StudentParticipationGrade  FROM StudentDetails     
                RIGHT JOIN AcademicData ON
                StudentDetails.DataID = AcademicData.DataID
                ''')
    #create a query for the first table
    Table1Data = cur.fetchall()
    for Table1Data in Table1Data:
        table1.insert('', tk.END, values=Table1Data)
        





    #creating the second page's table and formatting it
    table2 =ttk.Treeview(TeacherWindow, columns = ('ClassParticipationGrade','BehaviourGrade','AttendanceRate', 'MinimumMarkAchieved',
                                            'MaximumMarkAchieved','AmountOfMocksCompleted'), show = 'headings') 
    table2.heading('ClassParticipationGrade', text='ClassParticipationGrade')
    table2.heading('BehaviourGrade', text='BehaviourGrade')
    table2.heading('AttendanceRate', text='AttendanceRate')
    table2.heading('MinimumMarkAchieved', text='MinimumMarkAchieved')
    table2.heading('MaximumMarkAchieved', text='MaximumMarkAchieved')
    table2.heading('AmountOfMocksCompleted', text='AmountOfMocksCompleted')

    #creating the table 2 query
    cur.execute('''SELECT StudentClassParticipationGrade, StudentBehaviourGrade, AttendanceRate,
                MinimumMarkAChieved, MaximumMarkAchieved, AmountOfMocksCompleted FROM StudentDetails
                RIGHT JOIN AcademicData ON
                StudentDetails.DataID = AcademicData.DataID
                ''')
    Table2Data = cur.fetchall()
    for Table2Data in Table2Data:
        print(Table2Data)
        table2.insert('', tk.END, values=Table2Data)
    #creating third page's table and formatting
    table3 = ttk.Treeview(TeacherWindow, columns= ('TeacherFeedback', 'ComputerGeneratedFeedback','StudentComment', 'MedianMarkAchieved',
                                            'PredictedMark','PredictedGrade','StudentOverallEngagementGrade'), show = 'headings')
    table3.heading('TeacherFeedback', text= 'TeacherFeedback')
    table3.heading('ComputerGeneratedFeedback', text='ComputerGeneratedFeedback')
    table3.heading('StudentComment', text='StudentComment')
    table3.heading('MedianMarkAchieved', text='MedianMarkAchieved')
    table3.heading('PredictedMark', text='PredictedMark')
    table3.heading('PredictedGrade', text='PredictedGrade')
    table3.heading('StudentOverallEngagementGrade', text='StudentOverallEngagementGrade')

    cur.execute('''SELECT TeacherFeedback, ComputerGeneratedFeedback, StudentComment, MedianMarkAchieved,
                PredictedMark, PredictedGrade, StudentOverallEngagementGrade FROM StudentDetails
                RIGHT JOIN AcademicInformation ON
                StudentDetails.InformationID = AcademicInformation.InformationID''')
    Table3Data = cur.fetchall()
    for Table3Data in Table3Data:
        table3.insert('', tk.END, values=Table3Data)

    #Creating the Buttons:
    BackButton = tk.Button(TeacherWindow, text = 'back', command = Page1)
    BackButton2 = tk.Button(TeacherWindow, text = 'back',command = Page2)
    NextButton = tk.Button(text = 'next', command = Page2)
    NextButton.pack(fill = tk.X)
    NextButton2 = tk.Button(text = 'next', command = Page3)




    #creating a loop to register when buttons are clicked
    TeacherWindow.mainloop()

#This function contains the StudentGUI system, which will be executed if a student logins onto the program succesfully. 
def StudentGUI():
    StudentWindow = tk.Tk()
    StudentWindow.geometry('600x400')
    StudentWindow.title('treeview')

    table = ttk.Treeview(StudentWindow, columns = ('Subject', 'Feedback', 'OverallGrade', 'EffortGrade'), show = 'headings')
    table.heading('Subject', text = 'Subject')
    table.heading('Feedback', text = 'Feedback')
    table.heading('OverallGrade', text = 'OverallGrade')
    table.heading('EffortGrade', text = 'EffortGrade')
    table.grid(row = 0, column = 0)
    AIFeedbackTitleBox = tk.Label(text='AI revision tips and suggestions:',background = 'white',width = 40, height = 1, font=('calibri',15,'underline'))
    AIFeedbackTitleBox.grid(row = 1, column = 0)
    AIFeedbackBox = tk.Label(text='hi' , background = 'white', width = 115, height = 3)
    AIFeedbackBox.grid(row = 2, column = 0)
    ContextualDataTitle = tk.Label(background = 'white', text = '''Please detail contextual feedback you feel is relevant in
    the box below:''')
    ContextualDataTitle.grid(row = 3, column = 0)
    ContextualData = tk.Text(width = 40,height =5, font = 'Calibri')
    ContextualData.grid(row = 4, column = 0, padx = 10, pady = 10 )
    def EnterContextualData():
        ContextualDataInput = ContextualData.get('1.0', tk.END)
        ContextualData.delete('1.0', tk.END)
    ContextualDataEnterButton = tk.Button(text = 'enter', width = 50, background = 'green', foreground = 'white', command = EnterContextualData)
    ContextualDataEnterButton.grid(row = 5, column = 0)
    StudentCommentTitle = tk.Label(background = 'white', text = 'Please write your thoughts regarding your report below,')
    StudentCommentTitle.grid(row = 6, column = 0)
    StudentComment = tk.Text(width=40, height = 5, font = 'Calibri')
    StudentComment.grid(row = 7, column = 0)
    def EnterStudentComment():
        StudentCommentInput = StudentComment.get('1.0',tk.END)
        StudentComment.delete('1.0', tk.END)
    StudentCommentEnterButton = tk.Button(text = 'enter', width = 50, background = 'green', foreground = 'white', command = EnterStudentComment)
    StudentCommentEnterButton.grid(row = 8, column = 0)
    StudentWindow.mainloop()

# this function contains the LoginSystem itself, which will be run at the start of the program. 
def LoginSystem():
    con = sqlite3.connect('AcademicTrackerDB.db')
    cur = con.cursor()
    cur.execute('SELECT TeacherUsername FROM TeacherDetails WHERE TeacherID != ""')
    StoredTeacherUsernames = cur.fetchall()
    cur.execute('SELECT TeacherPassword FROM TeacherDetails WHERE TeacherID != ""')
    StoredTeacherPasswords = cur.fetchall()
    cur.execute('SELECT StudentUsername FROm StudentDEtails WHERE StudentID != ""')
    StoredStudentUsernames = cur.fetchall()
    cur.execute('SELECT StudentPassword FROm StudentDEtails WHERE StudentID != ""')
    StoredStudentPasswords = cur.fetchall()

    #defining widgets:
    LoginWindow = tk.Tk()
    LoginWindow.title('LoginSystem')
    LoginWindow.geometry('500x500')
    LoginWindowName = tk.Label(text = "Login System",width = 20, height =2, font = 'Calibri')
    UsernameLabel = tk.Label(text = "username", width = 20, padx = 5, font = 'Calibri')
    UsernameEntry = tk.Entry(font = 'Calibri')

    PasswordLabel = tk.Label(text = 'password', width = 20, font ='Calibri')
    PasswordEntry = tk.Entry(font = 'Calibri')

    def RunMainGUI(UsernameInput, PasswordInput):
        # checks if the UsernameInput is stored as a Teacher's Username on the database. If it is, UsernameInput is changed to the integer 1. 
        if UsernameInput in StoredTeacherUsernames and PasswordInput in StoredTeacherPasswords:
            TeacherGUI()
        # repeat process to check for a Student Username and Password, however if the value is valid, the variables are instead changed to the integer 2. 
        elif UsernameInput in StoredStudentUsernames and PasswordInput in StoredStudentPasswords:
            StudentGUI()
        else:
         print("The username or password entered is incorrect")
    #defining the function which will be binded to the login button as its command.     
    def RunMainGUICommand():
        UsernameInput = UsernameEntry.get()
        PasswordInput = PasswordEntry.get()
        RunMainGUI(UsernameInput,PasswordInput)
    loginbutton = tk.Button(text = "Login", width = 5, height = 1, bg= 'green', command = RunMainGUICommand, font = 'Calibri')
    #defining the exit button's command. 
    def exit():
        LoginWindow.destroy()
    exitbutton = tk.Button(text = 'exit',width = 5, height=1,bg='red',command=exit,font = 'Calibri')
    
    #placing widgets on screen:
    LoginWindowName.grid(row = 0, column = 0, columnspan = 2, sticky = 'news' )
    UsernameLabel.grid(row = 1, column = 0)
    UsernameEntry.grid(row = 1, column = 1)
    PasswordLabel.grid(row = 2, column = 0)
    PasswordEntry.grid(row = 2, column = 1)
    exitbutton.grid(row = 3, column = 0)
    loginbutton.grid(row = 3, column = 1)

    LoginWindow.mainloop()



# run the login system  
LoginSystem()