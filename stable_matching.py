# Zora Che with adaptations from Gavin Brown
# CS330, Fall 2021
# Stable Matching Algorithm Starter Code

import sys
import time
import numpy as np 



def read_prefs(pref_1_filename, pref_2_filename):
    # This function reads preferences from two files
    # and returns two-dimensional preference lists and the length of a list.
    with open(pref_1_filename, 'r') as f:
        hospital_raw = f.read().splitlines()
    with open(pref_2_filename, 'r') as f:
        student_raw = f.read().splitlines()
    N = int(student_raw[0])
    hospital_prefs = [[int(id) for id in  x.split(',')] for x in hospital_raw[1:]]
    student_prefs = [[int(id) for id in  x.split(',')] for x in student_raw[1:]]
    return N,  hospital_prefs, student_prefs



# Converts the entire matrix of preference list into an inverse_preference_list (as stated in lecture)
# Has nested for loops to iterate over every single element of the 2D matrix of preferences
# Runs in O(n^2) because of the nested for loop

def inverse_prefs(N, prefs):   
       ############################################################
    # Implement inverse preference lists as described in lecture
    # EDIT: New Inverse pref list implemented below 
    ############################################################
    n = 0
    h = 0 
    ranks = N*[None]# You'll need to replace this.
    inversed_ranks = np.zeros((N, N), dtype=int)
    for one_student_preference in prefs:       
        for hospital in one_student_preference:            
            ranks[hospital] = h
            h = h + 1
        h = 0 
        inversed_ranks[n] = ranks
        n = n + 1   
    return inversed_ranks
    
    
    
    
def run_GS(N, hospital_prefs, student_prefs, out_name):
    free_hospital = list(range(N))
    count = N*[0]               # stores a pointer to each hospital's next unproposed student, going from the left of hospital's preference list 
    current = N*[None]          # stores current assignment; index -> student, value -> hospital

    # algorithm - Hospital giving offer to student
   
    # Calling rank before the while loop. helper function written above. 
    rank = inverse_prefs(N, student_prefs) 

    
    while free_hospital:  # returns True if list is nonempty
        #print('--------')
        #print('current:', current)
        #print('free hospital', free_hospital)
        hospital = free_hospital.pop(0)
        student = hospital_prefs[hospital][count[hospital]]
        #print(hospital, 'proposing to', student)
        count[hospital] += 1
        if current[student] is None:   # student is not paired 
            current[student] = hospital
            #print('student is not paired')
        else:
            # slow way to compute 
            
            if rank[student][current[student]] < rank[student][hospital]:   
                
                ############################################################
                # The code in the if statement runs in linear time!
                # Fix that...
                # EDIT: The above code is fixed 
                # The rutime for N=3000 reduces to around 7 seconds 
                ############################################################
                
                 free_hospital.append(hospital)
            else:
                # student switches to new hospital, old hospital becomes free
              # print('student prefers', hospital)
                free_hospital.append(current[student])
                current[student] = hospital
    # write out matches
    with open(out_name, 'w') as f:
        for student, hospital in enumerate(current):
            f.write(str(hospital)+','+str(student)+'\n')

############################################################
# PART 2 STARTER CODE
############################################################

def check_stable(N, hospital_prefs, student_prefs, match_file):
    # Implement checking of stable matches from output
    # ...
    
    # Helper function used to obtain inverse_list of hospital and student preferences: as given in lecture 
    actual_hospital_rank = inverse_prefs(N, hospital_prefs)
    actual_student_rank = inverse_prefs(N, hospital_prefs)
    
    #Creating a list with N elements
    paired_list = [0] * N 

    #Final value to print
    final_print_val = 1

    #reading from the given file and extracting a list where indices are students and the corresponding value is the hospital that     #they are matched to 
    with open(match_file, 'r') as file: 
        for val in list(file):
            #removing the brackets and commas to extract a list in the manner proposed before

            match = val.strip("()").split(',') 
            h_val = int(match[0])
            stu_val = int(match[1])

            #Line of code where the actual execution of the previously explained intention
            paired_list[stu_val] = h_val
            
            
            
        for student_match in range(N): 
            # Getting the hospital match of the student in range(N) from the list we created earlier
            hospital_match = paired_list[student_match]
            
            #Making sure that the student's first preference was not the hospital he was assigned to 
            if (actual_hospital_rank[hospital_match][student_match]>0): 
                # Iterating over every hospital that the students prefers more than his/her current assignemt
                for j in range(0, actual_hospital_rank[hospital_match][student_match]):
                    
                    # Checking whether the hospital which the student prefers to the current assigned hospital prefers this 
                    # particular student more than their currently assigned student. If this will be true, then the matching is 
                    # not stable. If this will be false then we continue the loop. If the loop terminates then we print 1. 
                    
                    if actual_student_rank[hospital_prefs[hospital_match][j]][hospital_match]<actual_student_rank[hospital_prefs[hospital_match][j]][paired_list[hospital_prefs[hospital_match][j]]]:
                        final_print_val = 0 
    
    print(final_print_val)
    
    return 

    # Note: Make the printing of stableness be the only print statement for submission!
    
############################################################
# PART 3 STARTER CODE
############################################################

def check_unique(N, hospital_prefs, student_prefs):
    # Implement checking of a unique stable matching for given preferences
    # ...
    print(1)     # if unique
    print(0)     # if not unique
    # Note: Make the printing of uniqueness be the only print statement for submission!
    
    #Assigning the final value to be printed
    final_val_to_be_printed = 1
    
    #Running the GS algorithm and assigning to variables matching_1 and matching_2
    matching_1 = run_GS(N, hospital_prefs, student_prefs, None)
    matching_2 = run_GS(N, student_prefs, hospital_prefs, None)
    
    #iterating over range(len(matching_1))
    for i in range(len(matching_1)):
        index_of_matching_1 = matching_1[i]
        index_of_matching_2 = matching_2[index_of_matching_1]
        if (i != index_of_matching_2):
            final_val_to_be_printed = 0
    print(final_val_to_be_printed)
    
        
############################################################
# Main function. (Do not modify for submission.)
############################################################

def main():
    # Do not modify main() other than using the commented code snippet for printing 
    # running time for Q1, if needed
    if(len(sys.argv) < 5):
        return "Error: the program should be called with four arguments"
    hospital_prefs_raw = sys.argv[1] 
    student_prefs_raw = sys.argv[2]
    match_file = sys.argv[3]
    # NB: For part 1, match_file is the file to which the *output* is wrtten
    #     For part 2, match_file contains a candidate matching to be tested.
    #     For part 3, match_file is ignored.
    question = sys.argv[4]
    N, hospital_prefs, student_prefs = read_prefs(hospital_prefs_raw, student_prefs_raw)
    if question=='Q1':
        start = time.time()
        run_GS(N, hospital_prefs,student_prefs,match_file)
        end = time.time()
        print(end-start)
    elif question=='Q2':
        check_stable(N, hospital_prefs, student_prefs, match_file)
    elif question=='Q3':
        check_unique(N, hospital_prefs, student_prefs)
    else:
        print("Missing or incorrect question identifier (it should be the fourth argument).")
    return

if __name__ == "__main__":
    # example command: python stable_matching.py pref_file_1 pref_file_2 out_name Q1
    
    # stable_matching.py: filename; do not change this
    # pref_file_1: filename of the first preference list (proposing side)
    # pref_file_2: filename of the second preference list (proposed side)
    # out_name: desired filename for output matching file
    # Q1: desired question for testing 
    main()
