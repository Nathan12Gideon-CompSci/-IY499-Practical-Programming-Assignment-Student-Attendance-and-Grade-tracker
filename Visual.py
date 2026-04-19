import matplotlib.pyplot as plt #ONE OF THE REQUIRED LIBARIES FOR THE VISUALIZATION COMPONENT

def generate_attendance_chart(students): #Function to generate a bar chart for student attendance.
     #It takes a list of student dictionaries as input, where each dictionary contains the student's name and attendance percentage.

   
    names = [s['name'] for s in students] #goes through the list of students and extracts their names to create a list of names for the x-axis of the bar chart.

    attendance = [s['attendance'] for s in students] #similarly, it extracts the attendance percentages for each student to create a list of attendance values for the y-axis of the bar chart.

    plt.figure(figsize=(10, 6))

    plt.bar(names, attendance, color='skyblue') #sets the color of the bars to sky blue for better visualization.

    plt.axhline(y=80, color='r', linestyle='--', label='At-Risk Threshold') #adds a horizontal dashed red line at the 80% attendance threshold to visually indicate which students are at risk based on their attendance. The label 'At-Risk Threshold' is added for the legend.

    plt.xlabel('Student Name')

    plt.ylabel('Attendance (%)')

    plt.title('Class Attendance Overview')

    plt.legend()

    plt.show()
