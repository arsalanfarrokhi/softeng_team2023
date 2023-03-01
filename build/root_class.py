#===================================Library Definitions
from tkinter import *
from tkinter import Tk, messagebox
from login_class import homeFrame
from sign_class import signFrame
from options_class import optionsFrame
from skills_class import skillsFrame
from undone_class import undoneFrame
from job_class import jobFrame
from post_class import postFrame
import config
import sqlite3

class windows(Tk):
        def __init__(self, user = "", first = "", last = "", *args, **kwargs):
            Tk.__init__(self, *args, **kwargs)

            #Variables
            self.USERNAME = StringVar()  
            self.PASSWORD = StringVar()
            self.FIRST = StringVar()
            self.LAST = StringVar()
            self.JOBTITLE = StringVar()
            self.DESCRIPTION = StringVar()
            self.EMPLOYER = StringVar()
            self.LOCATION = StringVar()
            self.SALARY = StringVar()
            self.USERFRIEND = StringVar()

            #Configuring default window
            self.wm_title("InCollege")
            self.geometry("829x654")
            self.configure(bg = "#FFFFFF")

            #Creating a default frame and assigning it to a container
            container = Frame(self)
            container.pack(side="top", fill="both", expand=True)

            #Allows window to be resizable
            self.resizable(False, False)            

            #Creating a ditionary of frames
            self.frames = {}

            #Adding the potential frames to the dictionary
            for F in (homeFrame, optionsFrame, skillsFrame, undoneFrame, signFrame, jobFrame, postFrame):            
                frame = F(container, self)
                self.frames[F] = frame
                frame.grid(row=0,column=0, sticky='nsew')

            self.nextPage(homeFrame)
            
        def nextPage(self, cont):
            frame = self.frames[cont]
            # raises the current frame to the top
            frame.tkraise()

        def changePage(self, cont: str):
            if (cont == "homeFrame"):
                self.nextPage(homeFrame)
            if (cont == "optionsFrame"):
                self.nextPage(optionsFrame)
            if (cont == "skillsFrame"):
                self.nextPage(skillsFrame)
            if (cont == "undoneFrame"):
                self.nextPage(undoneFrame)
            if (cont == "signFrame"):
                self.nextPage(signFrame)
            if (cont == "jobFrame"):
                self.nextPage(jobFrame)
            if (cont == "postFrame"):
                self.nextPage(postFrame)
    
        def Database(self):
            global conn, cursor
            conn = sqlite3.connect("pythontut.db")
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER NOT NULL PRIMARY KEY  AUTOINCREMENT, username TEXT, password TEXT)")       
            cursor.execute("SELECT * FROM `member` WHERE `username` = 'admin' AND `password` = 'admin'")
            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO `member` (username, password) VALUES('admin', 'admin')")
                conn.commit()

        def Login(self):
            self.Database()
            if (self.USERNAME).get() == "" or (self.PASSWORD).get() == "":
                print("Please complete the required field!")
            else:
                cursor.execute("SELECT * FROM `member` WHERE `username` = ? AND `password` = ?", (self.USERNAME.get(), self.PASSWORD.get()))
                if cursor.fetchone() is not None:
                    self.nextPage(optionsFrame)
                    #config.username = self.USERNAME.get()
                    optionsFrame.changeUSER(self, user = self.USERNAME.get(), first = self.FIRST.get(), last = self.LAST.get())
                    '''
                    (self.USERNAME).set("")
                    (self.PASSWORD).set("")
                    '''
                    lambda: print("")
                else:
                    print("Invalid username or password")
                    (self.USERNAME).set("")
                    (self.PASSWORD).set("")   
            cursor.close()
            conn.close()

        def Signup(self):
            self.Database()
            cursor.execute("SELECT * FROM member")
            rows = cursor.fetchall()
            if (len(rows) < 10):
                for row in rows:
                    username, password, first, last = row
                    if(username == self.USERNAME.get()):
                        cursor.close()
                        conn.close()
                        messagebox.showerror(title="Error", message="Username already exists")
                        return
                if (self.USERNAME.get() == "" or self.FIRST.get() == "" or self.LAST.get() == ""):
                    messagebox.showwarning(title="Empty Input", message="Please complete the required field!")
                else:
                    if (self.isSignupInfoValid()):
                        sql = ''' INSERT INTO member(username, first, last, password) VALUES (?,?,?, ?) '''
                        task = (self.USERNAME.get(), self.FIRST.get(), self.LAST.get(), self.PASSWORD.get())
                        cursor.execute(sql, task)
                        conn.commit()
                        messagebox.showinfo(title="Success", message="Account successfully created.")
                        self.nextPage(homeFrame)
                cursor.close()
                conn.close()
            else:
                messagebox.showerror(title="Error", message="Maximum number of users.")
                cursor.close()
                conn.close()

        def PostJob(self):
            self.Database()
            cursor.execute("SELECT * FROM jobs")
            rows = cursor.fetchall()
            if (len(rows) < 5):
                if (self.JOBTITLE.get() == "" or self.DESCRIPTION.get() == "" or self.EMPLOYER.get() == "" or
                    self.LOCATION.get() == "" or self.SALARY.get() == ""):
                    print("Please complete the required field!")
                else:
                    sql = ''' INSERT INTO jobs(title, description, employer, location, salary) VALUES (?,?,?,?,?) '''
                    task = (self.JOBTITLE.get(), self.DESCRIPTION.get(), self.EMPLOYER.get(), self.LOCATION.get(), self.SALARY.get())
                    cursor.execute(sql, task)
                    conn.commit()
                cursor.close()
                conn.close()
            else:
                print("Maximum number of records in database \n")
                
        ''' def addFriend(self):
            user, friend = self.USERNAME, self.USERFRIEND
            self.Database()
        '''
        def isSignupInfoValid(self):
            
            password = self.PASSWORD.get()
            containsUpper = False
            containsNumber = False
            containsSpecialCharacter = False
            finalBool = False

            for letter in password:
                if letter.isupper():
                    containsUpper = True
                if letter.isdigit():
                    containsNumber = True
                if letter.isalnum() != True:
                    containsSpecialCharacter = True

            if len(password) < 8 or len(password) > 12:
                print('Password is either too long or too short')
                finalBool = False
            if containsUpper != True:
                print('Password must contain uppercase letter')
                finalBool = False
            if containsNumber != True:
                print('Passowrd must contain a number')
                finalBool = False
            if containsSpecialCharacter != True:
                print('Password doesn\'t contain a special character')
                finalBool = False

            #  return finalBool // Enabled when the SignUp option has a password field added
            return True 
        def getUser(self):
            return self.USERNAME.get()

#==============================================Main Method
if __name__ == '__main__':
    currentObject = windows()
    currentObject.mainloop()



