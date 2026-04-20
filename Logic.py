
def calculate_average(grades_list): #This function calculates the average score from a list of grade entries, which can be either simple numeric values or dictionaries containing subject and score information. It first
    
    # Calculates the average from a list of dictionaries: [{'subject': 'Math', 'score': 85}, ...]

    if not grades_list:
        return 0
    
    # Extract only the 'score' values into a new list
    scores = [item['score'] for item in grades_list]
    
    # Standard average formula: $Average = \frac{\sum scores}{n}$
    return sum(scores) / len(scores)

def bubble_sort_students(student_dict):
    #Sorts student names alphabetically for the View Student screen.
    names = list(student_dict.keys()) 
    n = len(names)
    for i in range(n): #This is the outer loop that iterates through each element in the list of student names. 
        # The inner loop compares adjacent names and swaps them if they are in the wrong order (i.e., if the current name is greater than the next name in alphabetical order).
        for j in range(0, n - i - 1):
            # The comparison is done using the lower() method to ensure that the sorting is case-insensitive.
            if names[j].lower() > names[j+1].lower():
                names[j], names[j+1] = names[j+1], names[j]
    return names
