import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3 as sql
#function to add tasks to the list  
def add_task():   
    task_string = task_field.get()    #to getstring from the entry field  
    if len(task_string) == 0:         #to check whether the string is empty or not  
        messagebox.showinfo('Error', 'Field is Empty.') #msg to print for an empty string 
    else:    
        tasks.append(task_string)     #to add tasks to list
        the_cursor.execute('insert into tasks values (?)', (task_string ,))  #function to execute SQL statement
        list_update()                 #to update the list
        task_field.delete(0, 'end')   #to delete entered task from entry field  
  
#function to update the list  
def list_update():   
    clear_list()                      # calling method to clear the list  
    for task in tasks:  
        task_listbox.insert('end', task)  #insert() method to insert the tasks  
  
#function to delete a task from the list  
def delete_task():  
    try:  
        #to get the selected entry from the list box  
        the_value = task_listbox.get(task_listbox.curselection())  
        # checking if the stored value is present in the tasks list  
        if the_value in tasks:  
            tasks.remove(the_value)   #to remove task  
            list_update()             #to update task list
            the_cursor.execute('delete from tasks where title = ?', (the_value,))  
    except:  
        messagebox.showinfo('Error','Please Select Task First.' )   #to display message box for an exception       
  
#function to delete all tasks from the list  
def delete_all_tasks():  
    message_box = messagebox.askyesno('Want to Delete All', 'Are you sure?')  #to get user confirmation  
    if message_box == True:  
        while(len(tasks) != 0):  
            tasks.pop()                #to pop out the elements from the list   
        the_cursor.execute('delete from tasks')  #to execute SQL statemaent  
        list_update()  
  
#function to clear the list  
def clear_list():   
    task_listbox.delete(0, 'end')      #to delete all tasks
  
#function to close the application 
def close():  
    print(tasks)                       # printing the elements from list   
    guiWindow.destroy()                #destroy() method to close the application 
  
# function to retrieve data from database  
def retrieve_database():    
    while(len(tasks) != 0):             #to iterate through the elements in the tasks list  

        tasks.pop()  
    for row in the_cursor.execute('select title from tasks'):   #iterate through the rows in the database table
        tasks.append(row[0])            #to insert the titles from table in the list  
  
#main function  
if __name__ == "__main__":  
    guiWindow = tk.Tk()  
    guiWindow.title("To-Do List Application")#Tile of window 
    guiWindow.geometry("500x450+750+250")  #setting dimensions 
    guiWindow.resizable(0, 0)            #disabling resizable option   
    guiWindow.configure(bg = "#FAEBD7")   
    the_connection = sql.connect('listOfTasks.db') #to connect to the database  
    # creating the cursor object of the cursor class  
    the_cursor = the_connection.cursor()    
    the_cursor.execute('create table if not exists tasks (title text)')   #to execute a SQL statement
    # defining empty list  
    tasks = []  
    # defining frames using the tk.Frame() widget  
    header_frame = tk.Frame(guiWindow, bg = "#737CA1")  
    functions_frame = tk.Frame(guiWindow, bg = "#737CA1")  
    listbox_frame = tk.Frame(guiWindow, bg = "#737CA1")  
    header_frame.pack(fill = "both")       #to place the frames
    functions_frame.pack(side = "left", expand = True, fill = "both")  
    listbox_frame.pack(side = "right", expand = True, fill = "both")  
    # defining a label using the ttk.Label() widget  
    header_label = ttk.Label(  
        header_frame,  
        text = "To-Do List",   
        font = ("Concolas","30"),
        foreground = "#FFFFFF",
        background = "#737CA1" 
    )  
    #to place the label in the application  
    header_label.pack(padx = 20, pady = 20)   
    task_label = ttk.Label(  
        functions_frame,  
        text = "Enter the Task:",  
        font = ("Consolas", "16","bold"),  
        background = "#737CA1",  
        foreground = "#000000"  
    )  
    #to place the label in the application  
    task_label.place(x = 30, y = 40)  
    # defining an entry field  
    task_field = ttk.Entry(  
        functions_frame,  
        font = ("Consolas", "17",),
        width = 18,  
        background = "#FFF8DC",  
        foreground = "#A52A2A"  
    )  
    task_field.place(x = 30, y = 80)        #to place the entry field in the window
    # adding buttons to the application  
    add_button = ttk.Button(  
        functions_frame,  
        text = "Add Task",  
        width = 24,  
        command = add_task  
    )
    del_button = ttk.Button(
        functions_frame,  
        text = "Delete Task(select from list)",
        width = 24,  
        command = delete_task  
    )  
    del_all_button = ttk.Button(  
        functions_frame,  
        text = "Delete All Tasks",  
        width = 24,  
        command = delete_all_tasks  
    )  
    exit_button = ttk.Button(  
        functions_frame,  
        text = "Exit",  
        width = 24,  
        command = close  
    )  
    #to set the position of the buttons in the application  
    add_button.place(x = 32,y = 125 )
    del_button.place(x = 32,y = 165 )
    del_all_button.place(x = 32,y = 200)
    exit_button.place(x = 32,y = 250)   
    task_listbox = tk.Listbox(  
        listbox_frame,  
        width = 26,  
        height = 13,  
        selectmode = 'SINGLE',  
        background = "#FFFFFF",  
        foreground = "#000000",  
        selectbackground = "#CD853F",  
        selectforeground = "#FFFFFF"  
    )   
    task_listbox.place(x = 10, y = 20)   #to place the list box
    retrieve_database()  
    list_update()  
    #to run the application  
    guiWindow.mainloop()  
    # get ection with database  
    the_connection.commit()  
    the_cursor.close()