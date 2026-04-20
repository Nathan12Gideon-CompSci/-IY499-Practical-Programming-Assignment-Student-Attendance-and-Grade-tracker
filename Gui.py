import tkinter as tk #Primary library for building the GUI.
from tkinter import messagebox # Displaying error and success messages to the user in a pop-up format.
import File_Handler as file_handler # Custom module for handling file operations related to student records and configuration settings. 
import Logic as logic # same here, the import module is quite a neat tool to modulaize code.
import Visual as visual

class TrackerApp: #Main application class that encapsulates all the functionality of the student tracker. 
    def __init__(self, root): #Initializes the main application window and sets up the initial state of the GUI. 
        self.root = root 
        self.root.title("Student Attendance and Grade Tracker") #Sets the title of the main application window to "Student Attendance and Grade Tracker".
        self.root.geometry("600x650") #adquetely sized for the various screens and components of the application.
        
       
        self.blue_bg = "#005eb8" #A consistent blue background color for buttons and other UI elements, defined as a hex color code. 
        self.white_fg = "#ffffff"
        self.thresholds = file_handler.load_thresholds()#loads the grade and attendance thresholds from the configuration file.
        
        self.container = tk.Frame(self.root)#A container frame that will hold all the different screens of the application. 
        self.container.pack(fill="both", expand=True) #This line ensures that the container frame fills the entire window and expands as needed when the window is resized.
        self.show_login()

    def clear(self):#A utility method to clear all widgets from the container frame. 
        for w in self.container.winfo_children(): w.destroy() #This method iterates through all the child widgets of the container frame and destroys them, effectively clearing the screen before displaying a new screen or set of widgets. 

    # --- LOGIN ---
    def show_login(self):
        self.clear()
        tk.Label(self.container, text="Student Tracker Login", font=("Arial", 16, "bold")).pack(pady=40) #A label widget that serves as the title for the login screen, with a specific font and padding for visual appeal.
        
        tk.Label(self.container, text="Username:").pack() #A label for the username entry field.
        self.u_entry = tk.Entry(self.container, font=("Arial", 14), width=25) #An entry widget for the user to input their username, with a specified font and width for better usability.
        self.u_entry.pack(pady=10)

        tk.Label(self.container, text="Password:").pack()#A label for the password entry field. 
        self.p_entry = tk.Entry(self.container, show="*", font=("Arial", 14), width=25)
        self.p_entry.pack(pady=10)

        tk.Button(self.container, text="Login", bg=self.blue_bg, fg=self.white_fg, #A button widget that the user clicks to attempt to log in, with a background color, foreground color, and specific dimensions for better aesthetics. 
                  
                  width=13, height=2, font=("Arial", 10, "bold"),
                  command=self.handle_login).pack(pady=20) #When the button is clicked, it calls the handle_login method to validate the credentials entered by the user.

    def handle_login(self): #This method checks the credentials entered by the user against hardcoded values
        if self.u_entry.get() == "admin" and self.p_entry.get() == "york2026": #you can change these to whatever you like, themematically
            self.show_main_menu() #If the credentials are correct, it calls the show_main_menu method to transition to the main menu of the application. 
        else:
            messagebox.showerror("Error", "Invalid Credentials") #Error handling

    # --- MAIN MENU ---
    def show_main_menu(self):
        self.clear()
        tk.Label(self.container, text="Main Menu", font=("Arial", 18, "bold")).pack(pady=30) #A label that serves as the title for the main menu screen, with a specific font and padding for visual appeal.
        
        row = tk.Frame(self.container)
        # The main menu has three primary buttons: "Change Threshold", "Add Details", and "View Students". 
        # These buttons allow the user to navigate to different sections of the application.
        row.pack(pady=20)
        
        btns = [("Change Threshold", self.show_threshold_menu),  #When the "Change Threshold" button is clicked, it calls the show_threshold_menu method,
                 ("Add Details", self.show_add_name), 
                 ("View Students", self.show_view_students)]
        
        for text, cmd in btns: #This loop iterates through the list of button configurations and creates a button for each one, setting the text and command accordingly. 
            tk.Button(row, text=text, width=15, height=2, command=cmd).pack(side="left", padx=10)

        tk.Button(self.container, text="Log out", bg=self.blue_bg, fg=self.white_fg, #made the logout button more visually distinct by giving it a background color, foreground color, and specific dimensions.
                  font=("Arial", 10, "bold"),
                  width=13, height=2, command=self.show_login).pack(pady=50)

    # --- THRESHOLD WINDOWS ---
    def show_threshold_menu(self): #This method displays the threshold settings menu, allowing the user to choose whether they want to change the grade threshold or the attendance threshold. 
        self.clear()
        # Displays a label at the top of the screen indicating that this is the "Threshold Settings" menu, with a specific font and padding for visual appeal.      
        tk.Label(self.container, text="Threshold Settings", font=("Arial", 14, "bold")).pack(pady=20)
        tk.Button(self.container, text="Change Grade Threshold", width=25, height=2, command=lambda: self.show_slider("grade")).pack(pady=5)
        tk.Button(self.container, text="Change Attendance Threshold", width=25, height=2, command=lambda: self.show_slider("attendance")).pack(pady=5)
        tk.Button(self.container, text="Back", bg=self.blue_bg, fg=self.white_fg, width=13, height=2, command=self.show_main_menu).pack(pady=30)

    def show_slider(self, mode):
        self.clear()
        tk.Label(self.container, text=f"Change {mode.capitalize()} Threshold", font=("Arial", 12, "bold")).pack(pady=10)#A label that indicates which threshold the user is currently adjusting (either "Grade Threshold" or "Attendance Threshold"), with a specific font and padding for visual appeal.
        
        val_label = tk.Label(self.container, text=f"Value: {self.thresholds[mode]}%", font=("Arial", 12))
        val_label.pack()#A label that displays the current value of the threshold being adjusted, which updates in real-time as the user moves the slider. The text is formatted to show the value as a percentage, and it has a specific font for better readability.

        s = tk.Scale(self.container, from_=100, to=0, orient="vertical", length=300, tickinterval=10,
                     command=lambda v: val_label.config(text=f"Value: {v}%")) #A vertical slider (Scale widget) that allows the user to adjust the threshold value. The slider ranges from 0 to 100, with tick marks every 10 units. As the user moves the slider, the command updates the val_label to reflect the current value of the slider in real-time.
        s.set(self.thresholds[mode])#When the slider is displayed, it is set to the current value of the threshold being adjusted (either the grade threshold or the attendance threshold) by calling the set method on the Scale widget. This ensures that the slider starts at the correct position corresponding to the existing threshold value, providing a better user experience.
        s.pack(pady=10)

        def save():
            self.thresholds[mode] = int(s.get())
            file_handler.save_thresholds(self.thresholds)#When the user clicks the "Enter" button, the save function is called. This function retrieves the current value from the slider using s.get(), converts it to an integer, and updates the corresponding threshold in the self.thresholds dictionary. It then calls file_handler.save_thresholds(self.thresholds) to save the updated thresholds to the configuration file, ensuring that the new settings are persisted across sessions. Finally, it displays a success message to the user and returns to the main menu.
            messagebox.showinfo("Success", "Threshold changed")
            self.show_main_menu()

        tk.Button(self.container, text="Enter", width=13, height=2, command=save).pack()#A button that the user clicks to save the new threshold value. When clicked, it calls the save function defined above, which updates the threshold settings and saves them to the configuration file. The button has specific dimensions for better aesthetics.
        tk.Button(self.container, text="Back", bg=self.blue_bg, fg=self.white_fg, width=13, height=2, command=self.show_threshold_menu).pack(pady=5)

    # --- ADD DETAILS FLOW ---
    def show_add_name(self):
        self.clear()

        tk.Label(self.container, text="Enter the name of student (Text Only):").pack(pady=20)#A label that prompts the user to enter the name of the student they want to add or edit, with specific padding for visual appeal.
        e = tk.Entry(self.container, font=("Arial", 14), width=25)#An entry widget where the user can input the name of the student. The entry has a specific font and width for better usability, and it is packed with padding to ensure it is visually separated from the label above.
        e.pack(pady=10)

        def go_next():
            name = e.get().strip()#When the user clicks the "Enter" button, the go_next function is called. This function retrieves the text entered in the entry widget, removes any leading or trailing whitespace using strip(), and checks if the name is valid (only contains alphabetic characters and is not empty). 
            #If the name is valid, it calls self.show_student_options(name) to proceed to the next screen where the user can add grades or attendance for that student. If the name is invalid, it displays an error message to the user indicating that names must only contain characters.
            if name.replace(" ","").isalpha() and name: self.show_student_options(name)

            else: messagebox.showerror("Error", "Names must only contain characters.")#This error handling checks if the name entered by the user is valid by ensuring that it only contains alphabetic characters (after removing spaces) and is not empty. If the name is invalid, it displays an error message to the user using messagebox.showerror, informing them that names must only contain characters. This helps maintain data integrity and prevents invalid entries in the student records.

        tk.Button(self.container, text="Enter", width=13, height=2, command=go_next).pack()
        #displays an "Enter" button that the user clicks to proceed after entering the student's name. When clicked, it calls the go_next function defined above, which validates the input and transitions to the student options screen if the name is valid. The button has specific dimensions for better aesthetics.
        tk.Button(self.container, text="Back", bg=self.blue_bg, fg=self.white_fg, width=13, height=2, command=self.show_main_menu).pack(pady=5)

    def show_student_options(self, name):
        self.clear()#This method displays the options for a specific student, allowing the user to add grades or attendance records for that student. It takes the student's name as a parameter and uses it to personalize the screen.
        tk.Label(self.container, text=f"Editing: {name}", font=("Arial", 14, "bold")).pack(pady=20)
        tk.Button(self.container, text="Add Grade", width=25, height=2, command=lambda: self.show_grade_input(name)).pack(pady=5)
        tk.Button(self.container, text="Add Attendance", width=25, height=2, command=lambda: self.show_att_input(name)).pack(pady=5)
        tk.Button(self.container, text="Back", bg=self.blue_bg, fg=self.white_fg, width=13, height=2, command=self.show_add_name).pack(pady=20)

    def show_grade_input(self, name):
        self.clear()
        tk.Label(self.container, text="Subject (Text Only):").pack()#A label that prompts the user to enter the subject for which they want to add a grade, with specific padding for visual appeal.
        s_e = tk.Entry(self.container)#An entry widget where the user can input the subject name. This entry is used to specify which subject the grade being added corresponds to. It is packed with padding to ensure it is visually separated from the label above.
        s_e.pack()
        tk.Label(self.container, text="Grade (0-100):").pack()
        g_e = tk.Entry(self.container)#An entry widget where the user can input the grade for the specified subject. This entry is used to capture the grade value that will be added to the student's record. It is packed with padding to ensure it is visually separated from the label above.
        g_e.pack()

        def save():
            sub, grd = s_e.get(), g_e.get()#When the user clicks the "Enter" button, the save function is called. This function retrieves the values entered in the subject and grade entry widgets. It first checks if the subject name is valid (only contains alphabetic characters). If the subject name is invalid, it displays an error message to the user indicating that only letters are allowed for the subject. If the subject name is valid, it then attempts to convert the grade input into a float and checks if it falls within the valid range of 0 to 100. If the grade is valid, it updates the student's record with the new grade using file_handler.update_student_data and displays a success message. If the grade is invalid (not a number or out of range), it displays an error message prompting the user to enter a number between 0 and 100.
            if not sub.isalpha(): return messagebox.showerror("Error", "Letters only for subject.") #(w3Schools, n.d.) for the isalpha() method, which checks if the subject name consists only of alphabetic characters. If the subject name is invalid, it returns early from the function and displays an error message to the user.
            try:
                val = float(grd)
                if 0 <= val <= 100: #magically worked
                    file_handler.update_student_data(name, "grade", {"subject": sub, "score": val}) #updates the student's record with the new grade for the specified subject. It calls the update_student_data function from the file_handler module, passing in the student's name, the data type ("grade"), and a dictionary containing the subject and score. This allows the application to keep track of grades for different subjects for each student.
                    messagebox.showinfo("Success", "Grade Added")
                    self.show_student_options(name)
                else: raise ValueError
            except: messagebox.showerror("Error", "Enter a number 0-100.")

        tk.Button(self.container, text="Enter", width=13, height=2, command=save).pack(pady=10)
        tk.Button(self.container, text="Back", bg=self.blue_bg, fg=self.white_fg, width=13, height=2, command=lambda: self.show_student_options(name)).pack() #A button that the user clicks to save the new grade. When clicked, it calls the save function defined above, which validates the input and updates the student's record if the input is valid. The button has specific dimensions for better aesthetics. There is also a "Back" button that allows the user to return to the previous screen without saving any changes.

    def show_att_input(self, name):

        self.clear()
        #
        tk.Label(self.container, text="Attendance Selection").pack(pady=10) #A label that serves as the title for the attendance input screen, with specific padding for visual appeal.
        s = tk.Scale(self.container, from_=0, to=100, orient="horizontal", length=300) #A horizontal slider (Scale widget) that allows the user to select the attendance percentage for the student. The slider ranges from 0 to 100, and it is packed with padding to ensure it is visually separated from the label above.
        s.pack()
        def save():
            file_handler.update_student_data(name, "attendance", s.get())
            messagebox.showinfo("Success", "Attendance Updated")
            self.show_student_options(name)
        tk.Button(self.container, text="Enter", width=13, height=2, command=save).pack(pady=10)
        tk.Button(self.container, text="Back", bg=self.blue_bg, fg=self.white_fg, width=13, height=2, command=lambda: self.show_student_options(name)).pack()
        
    #--- VIEW STUDENTS button ---
    def show_view_students(self):
        self.clear()
        data = file_handler.load_records()#Loads the student records from the data file using the load_records function from the file_handler module. This retrieves the current student data, which will be displayed in the view students screen.
        sorted_names = logic.bubble_sort_students(data)
        
        tk.Label(self.container, text="Full Student Records", font=("Arial", 16, "bold")).pack(pady=10) #A label that serves as the title for the view students screen, with a specific font and padding for visual appeal. It indicates that the user is viewing the full student records.
        # the following code creates a scrollable area within the GUI to display the list of students and their details. This is necessary because there may be many students, and a scrollable area allows the user to navigate through the list without overwhelming the screen space.
        #(Tutorials Point, n.d.) helped in understanding and implementing scrollbar
        # 1. Create a container for the Canvas and Scrollbar
        scroll_container = tk.Frame(self.container)
        scroll_container.pack(fill="both", expand=True, padx=10)

        # 2. Create the Canvas and Scrollbar
        canvas = tk.Canvas(scroll_container)
        scrollbar = tk.Scrollbar(scroll_container, orient="vertical", command=canvas.yview)
        
        # 3. Create the frame that will actually hold the student labels
        scrollable_frame = tk.Frame(canvas)

        # 4. Configure the canvas to update the scroll area whenever the frame size changes
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # 5. Place the frame inside the canvas window
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack the canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 6. Populate the scrollable_frame with student data
        grade_thresh = self.thresholds.get('grade', 40)
        att_thresh = self.thresholds.get('attendance', 80)

        for name in sorted_names:
            #For each student name in the sorted list of names, it retrieves the student's record from the data dictionary. 
            student = data[name]
            avg = logic.calculate_average(student['grades'])
            att = student.get('attendance', 0)
            
            # Formatting logic for "At-Risk" students
            header_text = f"Student: {name.upper()} | Avg: {avg:.1f}% | Att: {att}%"
            color = "red" if avg < grade_thresh or att < att_thresh else "black"
            
            tk.Label(scrollable_frame, text=header_text, font=("Arial", 11, "bold"), fg=color).pack(anchor="w", pady=(10, 0))
            #If the student has any grades recorded, it creates a list of details for each grade.
            if student['grades']:
                details = []
                for g in student['grades']:
                    if isinstance(g, dict): #This checks if the grade entry is a dictionary (which would contain both subject and score) or just a simple value.
                        details.append(f"{g['subject']}: {g['score']}")
                    else:
                        details.append(f"Grade: {g}")
                
                tk.Label(scrollable_frame, text=f"   Details: {', '.join(details)}", font=("Arial", 9), fg="gray").pack(anchor="w")

        # Control Buttons at the bottom
        bottom_frame = tk.Frame(self.container)
        bottom_frame.pack(pady=10)

        tk.Button(bottom_frame, text="Show Attendance Chart", width=20, 
                  command=lambda: visual.generate_attendance_chart(data, att_thresh)).pack(side="left", padx=5) #A button that, when clicked, generates an attendance chart using the generate_attendance_chart function from the visual module. 
        

        tk.Button(bottom_frame, text="Back", bg=self.blue_bg, fg=self.white_fg, 
                  width=10, font=("Arial", 10, "bold"), command=self.show_main_menu).pack(side="left", padx=5) #A "Back" button 
if __name__ == "__main__": #This line checks if the script is being run directly (as the main program) rather than imported as a module. 
    root = tk.Tk() #If the script is run directly, it creates a new Tkinter root window and initializes the TrackerApp with that root. 
    app = TrackerApp(root) #This line creates an instance of the TrackerApp class, passing the root window as an argument. 
    root.mainloop() #Finally, it calls root.mainloop() to start the Tkinter event loop, which keeps the application running and responsive to user interactions until the window is closed.
