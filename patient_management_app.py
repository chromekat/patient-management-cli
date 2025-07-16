# --------------------------------------------------
# Class: CS 2742 PYTHON PROGRAMMING
# Term: SPRING 2024
# Instructor: Jianmin Wang
# Description: Term Project - Patient Management System
# Due: 04/29/2024
# Author: Ansley Bray
# Python version 3.0
#
# By turning in this code I pledge:
#   1. That I have completed the programming assignment independently
#   2. I have not copied the code from a student or any source
#   3. I have not given my code to any student
# ---------------------------------------------------
#


import sqlite3

# creating minimum and maximum choice constants for validating user selection
MIN_CHOICE = 1
MAX_CHOICE = 9

# creating the constants for each menu option
ADD_PATIENT = 1
ADD_PROCEDURE = 2
DISPLAY_PATIENT_INFO = 3
DISPLAY_PROCEDURE_INFO = 4
CHANGE_PATIENT_INFO = 5
CHANGE_PROCEDURE_DATE = 6
DELETE_PROCEDURE = 7
DELETE_PATIENT_INFO = 8
EXIT_PROGRAM = 9

# creating a constant variable for referencing the patient management database
PATIENT_MANAGEMENT_DATABASE = "patient_management.db"

# creating a main method that will reference the logic for the rest of the program
def main():

    # displaying an initial message to the user
    greeting()

    # initializing the menu choice to zero
    menu_selection = 0

    # as long as the user isn't quitting the program, then the menu will display with each loop iteration when needed
    while menu_selection != EXIT_PROGRAM:
        # display the menu to the user
        display_menu()

        # obtaining the user's choice
        menu_selection = get_menu_selection()

        # determining which function to call based on user's selection
        if menu_selection == ADD_PATIENT:
            add_patient()
        elif menu_selection == ADD_PROCEDURE:
            add_procedure()
        elif menu_selection == DISPLAY_PATIENT_INFO:
            display_patient_info()
        elif menu_selection == DISPLAY_PROCEDURE_INFO:
            display_procedure_info()
        elif menu_selection == CHANGE_PATIENT_INFO:
            update_patient_info()
        elif menu_selection == CHANGE_PROCEDURE_DATE:
            update_procedure_date()
        elif menu_selection == DELETE_PROCEDURE:
            delete_procedure_from_system()
        elif menu_selection == DELETE_PATIENT_INFO:
            delete_patient()


# this function displays an initial message to the user
def greeting():
    print("Welcome to the patient management application")

# providing a menu of options to the user
def display_menu():
    print("PLEASE SELECT ONE OF THE FOLLOWING OPTIONS: ")
    print("1 - TO ADD A NEW PATIENT")
    print("2 - TO ADD A NEW PROCEDURE")
    print("3 - TO DISPLAY PATIENT INFORMATION")
    print("4 - TO DISPLAY PROCEDURE INFORMATION")
    print("5 - TO UPDATE PATIENT INFORMATION")
    print("6 - TO UPDATE PROCEDURE DATE")
    print("7 - TO DELETE PROCEDURE")
    print("8 - TO DELETE PATIENT INFORMATION")
    print("9 - TO EXIT PROGRAM")
    print("--------------------------------------------")

# obtaining the user's menu selection and returning it to the main() function to then maneuver through the program
def get_menu_selection():
    while True:
        try:
            # asking the user to enter the appropriate menu response
            menu_choice = int(input("Enter your choice here: "))

            # if the user enters a number beyond the scope of the options, they receive an invalid input message
            if menu_choice < MIN_CHOICE or menu_choice > MAX_CHOICE:
                print("Invalid selection. Please try again.")

            else:
                # if the number entered by the user is recognized, it is returned to be used in the main method
                return menu_choice
        except ValueError:
            # this message appears if the user attempts to enter a non-integer value
            print("You can only enter an integer. Try again.")

# the following function is called when the user wishes to add a patient to the system
def add_patient():
    # informing the user of what they have selected
    print("You selected Add a New Patient")

    move_forward = verify_menu_selection()

    if move_forward:
        # obtain the relevant patient information from the user
        patient_id = int(input("Enter patient ID: "))
        first_name = input("Enter patient's first name: ")
        last_name = input("Enter patient's last name: ")
        street = input("Enter street name and number: ")
        city = input("Enter city: ")
        state = input("Enter state/province: ")
        zipcode = input("Enter zipcode: ")
        patient_phone = input("Enter patient's phone number: ")
        emergency_contact = input("Enter emergency contact's first and last name: ")
        emergency_phone = input("Enter emergency contact's phone number: ")

        # insert the information collected from the user
        insert_patient_info(patient_id, first_name, last_name, street, city, state, zipcode, patient_phone, emergency_contact,
                            emergency_phone)

# the following function inserts patient data input by the user
def insert_patient_info(id_num, fname, lname, street, city, state, zipcode, patphone, econtact,
                        ephone):

    conn = None

    # using a try/except statement the function attempts to insert data
    try:
        # attempting to connect with the database
        conn = sqlite3.connect(PATIENT_MANAGEMENT_DATABASE)
        cur = conn.cursor()

        # inserting patient data
        cur.execute('''INSERT INTO Patients (PatientID, FirstName, LastName, Street, City, State, ZipCode, Phone,
                            EmergencyContact, EmergencyPhone)
                            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (id_num, fname, lname, street, city, state, zipcode, patphone,
                                econtact, ephone))
        # saving the insertion
        conn.commit()
        print("Patient added.")
    except sqlite3.Error as err:
        print("Database Error", err)
    finally:
        # ending the database connection
        if conn != None:
            conn.close()


# the following function changes some part of the patient's information
def update_patient_info():
    # creating constants for general sub-menu options of what the user wishes to update about the patient
    UPDATE_BIOGRAPHICAL_INFORMATION = 1
    UPDATE_ADDRESS = 2
    UPDATE_EMERGENCY_CONTACT = 3
    UPDATE_ALL = 4
    GO_BACK = 5


    # utilizing the lookup patient function to ensure they exist in the database before making changes
    lookup_patient()

    # if the patient does exist, then the user enters their ID to begin the updating process
    id_number = int(input("Enter the patient's ID number (see above): "))

    display_update_info_menu()

    selection = get_update_selection()

    while selection != GO_BACK:
        if selection == UPDATE_BIOGRAPHICAL_INFORMATION:
            update_biographical_info(id_number)
            break
        elif selection == UPDATE_ADDRESS:
            update_address(id_number)
            break
        elif selection == UPDATE_EMERGENCY_CONTACT:
            update_emergency_contact(id_number)
            break
        elif selection == UPDATE_ALL:
            update_all(id_number)
            break


# this menu is displayed initially when the user opts to update patient info
def display_update_info_menu():
    print("Which category of information would you like to update? ")
    print("1 - BIOGRAPHICAL INFORMATION")
    print("2 - ADDRESS")
    print("3 - EMERGENCY CONTACT")
    print("4 - ALL")
    print("5 - GO BACK")

# this function obtains the user's choice as to what part of patient data they wish to update
def get_update_selection():
    LOWEST_CHOICE = 1
    HIGHEST_CHOICE = 5

    while True:
        try:
            choice = int(input("Enter your choice here: "))
            if choice < LOWEST_CHOICE or choice > HIGHEST_CHOICE:
                print("Invalid selection. Please try again.")
            else:
                return choice
        except ValueError:
            print("You can only enter an integer. Please try again.")

def update_biographical_info(id):
    UPDATE_FIRST_NAME = 1
    UPDATE_LAST_NAME = 2
    UPDATE_BOTH = 3

    print("Which would you like to update?")
    print("1 - First Name")
    print("2 - Last Name")
    print("3 - Both")

    # obtain user input
    while True:
        try:
            update_selection = int(input("Enter selection: "))
            if update_selection == UPDATE_FIRST_NAME:
                first_name = input("Enter new first name: ")
                update_first_name(id, first_name)
                break
            elif update_selection == UPDATE_LAST_NAME:
                last_name = input("Enter new last name: ")
                update_last_name(id, last_name)
                break
            elif update_selection == UPDATE_BOTH:
                first_name = input("Enter new first name: ")
                last_name = input("Enter new last name: ")
                update_both_names(id, first_name, last_name)
                break
            else:
                print("Invalid input. Try again.")
        except ValueError:
            print("Must enter an integer. Try again.")

def update_first_name(id, fname):
    conn = None
    try:
        conn = sqlite3.connect(PATIENT_MANAGEMENT_DATABASE)
        cur = conn.cursor()
        cur.execute('''UPDATE Patients SET FirstName == ? WHERE PatientID == ?''',
                    (fname, id))

        conn.commit()
        print("First name updated.")
    except sqlite3.Error as err:
        print("Database Error", err)
    finally:
        if conn != None:
            conn.close()



def update_last_name(id, lname):
    conn = None
    try:
        conn = sqlite3.connect(PATIENT_MANAGEMENT_DATABASE)
        cur = conn.cursor()
        cur.execute('''UPDATE Patients SET LastName == ? WHERE PatientID == ?''',
                    (lname, id))
        conn.commit()
        print("Last name updated.")
    except sqlite3.Error as err:
        print("Database error", err)
    finally:
        if conn != None:
            conn.close()

def update_both_names(id, fname, lname):
    conn = None
    try:
        conn = sqlite3.connect(PATIENT_MANAGEMENT_DATABASE)
        cur = conn.cursor()
        cur.execute('''UPDATE Patients SET FirstName == ? AND LastName == ? WHERE PatientID == ?''',
                    (fname, lname, id))
        conn.commit()
        print("Full name updated.")
    except sqlite3.Error as err:
        print("Database error", err)
    finally:
        if conn != None:
            conn.close()

def update_address(id):
    print("You selected update address.")
    print()
    street = input("Enter the new street name and number: ")
    city = input("Enter the new city: ")
    state = input("Enter the new state/province: ")
    zip_code = input("Enter the new zipcode: ")
    insert_new_address(id, street, city, state, zip_code)


def update_emergency_contact(id):
    print("You selected update emergency contact.")
    print("--------------------------------------")

    contact_name = input("Enter emergency contact's full name: ")
    contact_phone = input("Enter the emergency contact's phone: ")
    insert_new_emergency_contact(id, contact_name, contact_phone)



def update_all(id):
    print("You selected update all info")
    print("----------------------------")

    print("BIOGRAPHICAL INFO")
    print("-----------------")
    first_name = input("Enter new first name: ")
    last_name = input("Enter new last name: ")
    patient_phone = input("Enter new phone number: ")
    print()

    print("ADDRESS")
    print("--------")
    street = input("Enter new street name and number: ")
    city = input("Enter new city: ")
    state = input("Enter new state/province: ")
    zipcode = input("Enter new zipcode: ")
    print()

    print("EMERGENCY CONTACT INFORMATION")
    print("-----------------------------")
    emergency_contact = input("Enter new emergency contact's first and last name: ")
    emergency_phone = input("Enter new emergency contact's phone number: ")

    insert_all_info(id, first_name, last_name, patient_phone, street, city, state, zipcode, emergency_contact, emergency_phone)



def insert_all_info(id, fname, lname, patient_phone, street, city, state, zipcode, econtact, ephone):
    conn = None
    try:
        conn = sqlite3.connect(PATIENT_MANAGEMENT_DATABASE)
        cur = conn.cursor()
        cur.execute('''UPDATE Patients
                        SET FirstName = ?, LastName = ?, Street = ?, City = ?, State = ?,
                        ZipCode = ?, Phone = ?, EmergencyContact = ?, EmergencyPhone = ?
                        WHERE PatientID = ?''',
                    (fname, lname, street, city, state, zipcode, patient_phone, econtact, ephone, id))

        conn.commit()
        print("Patient info updated.")
    except sqlite3.Error as err:
        print("Database Error", err)
    finally:
        if conn != None:
            conn.close()



def insert_new_emergency_contact(id_number, name, phone):
    conn = None
    try:
        conn = sqlite3.connect(PATIENT_MANAGEMENT_DATABASE)
        cur = conn.cursor()
        cur.execute('''UPDATE Patients
                        SET EmergencyContact = ?, EmergencyPhone = ? 
                        WHERE PatientID = ?''',
                    (name, phone, id_number))

        conn.commit()
        print("Emergency contact updated.")
    except sqlite3.Error as err:
        print("Database error", err)
    finally:
        if conn != None:
            conn.close()



def insert_new_address(id, street, city, state, zip_code):
    conn = None
    try:
        conn = sqlite3.connect(PATIENT_MANAGEMENT_DATABASE)
        cur = conn.cursor()
        cur.execute('''UPDATE Patients
                        SET Street = ?, City = ?, State = ?, ZipCode = ?
                        WHERE PatientID == ?''',
                    (street, city, state, zip_code, id))

        conn.commit()
        print("Address updated.")
    except sqlite3.Error as err:
        print("Database Error", err)
    finally:
        if conn != None:
            conn.close()


def update_procedure_date():
    # first lookup patient to make sure they exist in the system

    lookup_patient()

    # obtain the patient ID number from lookup info
    id_num = int(input("Enter the ID of the patient whose procedure date you wish to change (see above): "))

    print("Are you sure you wish to alter the date of the procedure?")
    if verify_menu_selection():
        new_date = input("Enter the new appointment date (MM-DD-YYYY): ")
        update_procedure(id_num, new_date)


def update_procedure(id_num, date):
    conn = None
    try:
        conn = sqlite3.connect(PATIENT_MANAGEMENT_DATABASE)
        cur = conn.cursor()
        cur.execute('''UPDATE Procedures
                        SET ProcedureDate = ? 
                        WHERE ID == ?''',
                    (date, id_num))

        conn.commit()
        print("Procedure updated.")
    except sqlite3.Error as err:
        print("Database Error", err)
    finally:
        if conn != None:
            conn.close()

def delete_procedure_from_system():
    # first lookup the patient to ensure they exist
    lookup_patient()

    # obtain the id number of the patient to ensure a successful deletion of the matching procedure record
    id_num = int(input("Enter the ID of the patient you wish to delete the procedure for: "))

    # verify the user wants to delete the procedure
    print("Are you sure you want to delete this scheduled procedure?")
    if verify_menu_selection():
        delete_procedure(id_num)


def delete_procedure(id):
    conn = None
    try:
        conn = sqlite3.connect(PATIENT_MANAGEMENT_DATABASE)
        cur = conn.cursor()
        cur.execute('''DELETE FROM Procedures WHERE ID == ?''',
                    (id,))

        conn.commit()
        print("Procedure deleted.")
    except sqlite3.Error as err:
        print("Database Error", err)
    finally:
        if conn != None:
            conn.close()





def delete_patient():
    # first lookup the patient to make sure they exist in the system
    lookup_patient()

    # obtaining the ID number of the entry we want to delete (in case someone has a duplicate name)
    id_num = int(input("Enter the ID of the patient you wish to delete (see above data): "))

    # verify that the user does wish to delete the entry
    print(f"Are you sure you wish to delete this patient?")
    if verify_menu_selection():
        num_deleted = delete_entry(id_num)

        print(f"{num_deleted} patient(s) deleted")


# the following function will search for a patient to determine if they are in the database
def lookup_patient():
    # get the name of the patient we want to find
    first_name = input("Enter the patient's first name: ")
    last_name = input("Enter the patient's last name: ")

    # creating a variable to hold the result of the lookup
    patient_found = find_patient(first_name, last_name)

    print(f"{patient_found} patient(s) found")


# the following function allows you to add a procedure to the patient management system
def add_procedure():
    print("You selected Add a New Procedure")

    move_forward = verify_menu_selection()

    if(move_forward):
        # obtain the relevant procedure information from the user
        patient_id = int(input("Enter the ID for the patient: "))
        procedure_name = input("Enter the name of the procedure: ")
        procedure_date = input("Enter the date of the procedure (MM-DD-YYYY): ")
        practitioner_name = input("Enter the name of the practitioner performing the procedure: ")
        cost = float(input("Enter the amount to be charged to the patient: "))

        # insert the data into the database
        insert_procedure_info(patient_id, procedure_name, procedure_date, practitioner_name, cost)



# the following function displays the patient information
def display_patient_info():
    conn = None

    # creating an array to store the results fetched by the database
    results = []

    try:
        conn = sqlite3.connect(PATIENT_MANAGEMENT_DATABASE)
        cur = conn.cursor()
        cur.execute('''SELECT * FROM Patients''')

        # obtaining the results
        results = cur.fetchall()

        print()

        print(f"Patient ID: \t First Name: \t \t Last Name: \t \t Street: \t \t \t \t \t \t \t City: \t \t \t \t"
              f"State/Province: \t Zipcode: \t Phone Number: \t \t Emergency Contact: \t Emergency Phone: ")

        print("--------------------------------------------------------------------------------------------------"
              "--------------------------------------------------------------------------------------------------"
              "---------")

        # showing the results of the table
        for row in results:
            # print(f"Patient ID: {row[0]:<10} First name: {row[1]:<10}"
            #       f"Last Name: {row[2]:<10} Street: {row[3]:<30}"
            #       f"City: {row[4]:<20} State/Province: {row[5]:<20}"
            #       f"Zipcode: {row[6]:<20} Emergency Contact: {row[7]:<20}"
            #       f"Emergency Phone: {row[8]:<20}")


            print(f"{row[0]:<10} \t \t {row[1]:<10} \t \t {row[2]:<10} \t \t {row[3]:<30} \t {row[4]:<15}"
                  f"\t{row[5]:<15} \t {row[6]:<7} \t {row[7]:<15} \t {row[8]:<20} \t {row[9]:<20}")

            # print()
            print("--------------------------------------------------------------------------------------------------"
                  "--------------------------------------------------------------------------------------------------"
                  "---------")

    except sqlite3.Error as err:
        print("Database Error", err)

    finally:
        # close database connection
        if conn != None:
            conn.close()

    return len(results)


# the following function displays information related to procedures that have been input into a databse
def display_procedure_info():
    conn = None

    # creating an array to hold the procedure table rows
    results = []

    try:
        conn = sqlite3.connect(PATIENT_MANAGEMENT_DATABASE)
        cur = conn.cursor()
        cur.execute('''SELECT * FROM Procedures''')

        # importing the results
        results = cur.fetchall()

        print()

        print(f"Patient ID: \t \t Procedure Name: \t \t Procedure Date: \t \t Practitioner: \t \t \t Cost: ")

        print("--------------------------------------------------------------------------------------------------"
              "---------------------")

        for row in results:

            print(f"{row[0]:<15} \t {row[1]:<20} \t {row[2]:<20} \t {row[3]:<20} \t ${row[4]:<10}")

            print("--------------------------------------------------------------------------------------------------"
                  "---------------------")

        print()

    except sqlite3.Error as err:
        print("Database Error", err)

    finally:
        if conn != None:
            conn.close()

    return len(results)



def verify_menu_selection():
    while True:
        try:
            verified_selection = input("Continue? (y/n): ")
            if verified_selection.lower() == "y":
                return True
            elif verified_selection.lower() == "n":
                return False
        except ValueError:
            print("Invalid input. Please try again.")



# the following function inserts procedure data input by the user
def insert_procedure_info(id, procedure_name, date, practitioner, cost):
    conn = None

    # using a try/except statement to attempt to insert data
    try:
        conn = sqlite3.connect(PATIENT_MANAGEMENT_DATABASE)
        cur = conn.cursor()

        # inserting the procedural data
        cur.execute('''INSERT INTO Procedures(ID, ProcedureName, ProcedureDate, Practitioner, Charge)
                        VALUES(?, ?, ?, ?, ?)''',
                    (id, procedure_name, date, practitioner, cost))

        # saving the insertion
        conn.commit()
        print("Procedure added.")
    except sqlite3.Error as err:
        print("Database Error", err)
    finally:
        # ending the database connection
        if conn != None:
            conn.close()

def find_patient(first_name, last_name):
    conn = None

    # array for holding search results that match
    try:
        conn = sqlite3.connect(PATIENT_MANAGEMENT_DATABASE)
        cur = conn.cursor()
        cur.execute('''SELECT PatientID, FirstName, LastName 
                        FROM Patients 
                        WHERE lower(FirstName) == ? AND lower(LastName) == ?''',
                    (first_name.lower(), last_name.lower()))

        results = cur.fetchall()

        for row in results:
            print(f"Patient ID: {row[0]:<3} First Name: {row[1]:<10} Last Name: {row[2]}")

    except sqlite3.Error as err:
        print("Database Error", err)
    finally:
        if conn != None:
            conn.close()

    return len(results)

def delete_entry(id):
    conn = None
    try:
        conn = sqlite3.connect(PATIENT_MANAGEMENT_DATABASE)
        cur = conn.cursor()

        cur.execute('''DELETE FROM Patients WHERE PatientID == ?''',
                    (id,))

        cur.execute('''DELETE FROM Procedures WHERE ID == ?''',
                    (id,))

        conn.commit()
        print("Patient deleted.") 

    except sqlite3.Error as err:
        print("Database Error", err)
    finally:
        if conn != None:
            conn.close()





if __name__ == '__main__':
    main()