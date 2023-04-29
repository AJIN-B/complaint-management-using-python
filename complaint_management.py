import mysql.connector
import tkinter as tk
from tkinter import Tk, Text, BOTH, W, N, E, S


HOST = '' # host name of your mysql ie name localhost
USER ='' # user name of your mysql ie root
PASSWORD ='' # Password for your mysql ie 12345

class Database_create():
    
    @staticmethod
    def create_database(db_name):
        mydb = mysql.connector.connect(host=HOST,user=USER,password=PASSWORD)
        mycursor = mydb.cursor()
        mycursor.execute('CREATE DATABASE {}'.format(db_name)) ##create database
        mydb.commit()
        mydb.close()
        
    @staticmethod
    def create_tabel(db_name,tabel_name='complaints'):
        mydb = mysql.connector.connect(host=HOST,user=USER, password=PASSWORD ,database =db_name )
        mycursor = mydb.cursor()
        mycursor.execute('SHOW TABLES') ##SHOW TABLES
        all_tabels =[i[0] for i in mycursor]
        if tabel_name not in all_tabels:
            mycursor.execute('CREATE TABLE {} (Name VARCHAR(255),Gender VARCHAR(255),EmployeeID VARCHAR(255),Complaint text)'.format(tabel_name)) ##CREATE TABLE
        mydb.commit()
        mydb.close()
    
    @staticmethod
    def Add_column(cl,db_name='complaint_management',tabel_name='complaints'):
        mydb = mysql.connector.connect(host=HOST,user=USER, password=PASSWORD ,database =db_name )
        mycursor = mydb.cursor()
        mycursor.execute('ALTER TABLE {} ADD {} VARCHAR(255)'.format(tabel_name,cl))
        mydb.commit()
        mydb.close()
    
    def check_columns(self,db_name='complaint_management',tabel_name='complaints'):
        req_col = ['Name' ,'Gender' ,'Complaint', 'EmployeeID' ]
        mydb = mysql.connector.connect(host=HOST,user=USER, password=PASSWORD ,database =db_name )
        mycursor = mydb.cursor()
        mycursor.execute('SELECT * FROM {}'.format(tabel_name))
        num_fields = len(mycursor.description)
        colu = mycursor.description
        field_names = [colu[i][0] for i in range(num_fields)]
        mydb.close()   
        for cl in req_col:
            if cl not in field_names:
                self.Add_column(cl)
        
    def check_databaseis(self,db_name='complaint_management'):
        mydb = mysql.connector.connect(host=HOST,user=USER,password=PASSWORD)
        mycursor = mydb.cursor()
        mycursor.execute('SHOW DATABASES') ##SHOW database
        database_names = [i[0] for i in mycursor]
        if db_name not in database_names:self.create_database(db_name);
        self.create_tabel(db_name,tabel_name='complaints')  
        mydb.commit()
        mydb.close()
        self.check_columns( db_name='complaint_management',tabel_name='complaints')


class compliant_management(Database_create):
    
    def __init__(self):
        self.check_databaseis()
    
    def load_database(self,db_name='complaint_management'):
        self.mydb = mysql.connector.connect(host=HOST,user=USER, password=PASSWORD ,database =db_name )
        self.mycursor = self.mydb.cursor()
        
    def dest(self):
        self.root.destroy()

    def val(self):
        
        cm = self.comment.get(1.0, 'end')
        if self.v.get() == 1:gen = 'Male'
        else :gen = 'Female'
                
        insert_stmt = ("INSERT INTO complaints(Name ,Gender ,Complaint, EmployeeID)"
                       "VALUES (%s, %s, %s, %s)")
        data = (self.name_var.get(),gen,cm,self.id_var.get())
        check = True
        for i in data:
            if len(i) == 0:
                tk.messagebox.showerror("showerror", "Invalid data")
                check = False
                break
        if check:
            self.mycursor.execute(insert_stmt, data)
            self.mydb.commit()
            self.mydb.close()
            self.dest()
            tk.messagebox.showinfo("showinfo", "Response Submitted thanks for the feedback")

        
    def run(self):
        
        self.load_database()
        
        self.root = tk.Tk()
        self.root.geometry('700x450')
        self.root.title('Complaint Management')
        self.root.configure(background='#AEB6BF')
        
        labels = ['Full Name   ', 'Gender  ','Employee ID   ', 'Comment']
        for i in range(len(labels)):
            if labels[i] != 'Comment': 
                tk.Label(self.root, text=labels[i],bg= "#AEB6BF", fg= "black", font=('Arial', 12)
                         ).grid(row=i, column=0, padx=15, pady=15, sticky=W)
            else :
                tk.Label(self.root, text=labels[i],bg= "#AEB6BF", fg= "black", font=('Arial', 12)
                         ).grid(row=i, column=0, padx=15, pady=15, sticky=W)
        
        self.name_var = tk.StringVar()
        self.id_var = tk.StringVar()
        self.v = tk.IntVar()

        fullname = tk.Entry(self.root, width=40, font=('Arial', 12),textvariable=self.name_var
                            ).grid(row=0, column=1, columnspan=2, sticky=W)
        tk.Radiobutton(self.root, text='Male', font=('Arial', 12), variable=self.v, value=1,height=1, width=5
                       ).grid(row=1, column=2, sticky=W)  
        tk.Radiobutton(self.root, text='Female', font=('Arial', 12), variable=self.v, value=0,height=1, width=5
                       ).grid(row=1, column=1, sticky=W)
        Employee_ID = tk.Entry(self.root, width=40, font=('Arial', 12),textvariable=self.id_var
                               ).grid(row=2, column=1, columnspan=2, sticky=W)

        self.comment = tk.Text(self.root, width=35, height=5, font=('Arial', 14))
        self.comment.grid(row=3, column=1, columnspan=2, padx=15, pady=15, sticky=W)
        
        BuSubmit = tk.Button(self.root, text='Submit Now',font=('Arial', 12),command=self.val
                             ).grid(row=6, column=1, padx=15, pady=15)

        self.root.mainloop()


if __name__ == "__main__":
    comp_mang = compliant_management()
    comp_mang.run()



