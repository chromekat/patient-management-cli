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

def greeting():
    # explaining the application to the user

    print("Welcome to the patient database management system")
    print("Here, you can enter information for patients and corresponding procedures.")
    print("--------------------------------------------------------------------------")


def main():

    INSERT_PATIENT_INFO = 1
    INSERT_PROCEDURE_INFO = 2
    EXIT = 3

    MIN_CHOICE = 1
    MAX_CHOICE = 3

    greeting()

    # connecting to the database we will create
    conn = sqlite3.connect("patient_management.db")

    cur = conn.cursor()

    # creating the patients table with the corresponding data columns
    cur.execute('''CREATE TABLE IF NOT EXISTS Patients(PatientID INTEGER PRIMARY KEY NOT NULL,
                                                FirstName TEXT,
                                                LastName TEXT,
                                                Street TEXT,
                                                City TEXT,
                                                State TEXT,
                                                ZipCode TEXT,
                                                Phone TEXT,
                                                EmergencyContact TEXT NULL,
                                                EmergencyPhone TEXT NULL)''')

    # creating the procedures table with the corresponding data columns
    cur.execute('''CREATE TABLE IF NOT EXISTS Procedures(ID INTEGER PRIMARY KEY NOT NULL,
                                                        ProcedureName TEXT,
                                                        ProcedureDate TEXT,
                                                        Practitioner TEXT,
                                                        Charge REAL)''')

    # displaying the menu to the user
    display_menu_options()

    # obtaining their selection
    menu_selection = int(input("Enter selection: "))

    # loop condition
    again_patient = "y"
    again_procedure = "y"

    while menu_selection != EXIT:

        if menu_selection == INSERT_PATIENT_INFO:
            while again_patient.lower() == "y":
                # get patient information
                patient_id = int(input("Patient ID: "))
                first_name = input("First name: ")
                last_name = input("Last name: ")
                street = input("Street: ")
                city = input("City: ")
                state = input("State: ")
                zip_code = input("Zip: ")
                phone = input("Phone number: ")
                emergency_contact = input("Emergency contact name: ")
                emergency_phone = input("Emergency contact phone: ")

                # insert the data accordingly
                cur.execute('''INSERT INTO Patients(PatientID, FirstName, LastName, Street, City, State, ZipCode, Phone, 
                                        EmergencyContact, EmergencyPhone)
                                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                            (patient_id, first_name, last_name, street, city, state, zip_code, phone,
                             emergency_contact, emergency_phone))

                # prompt the user to enter another patient record
                again_patient = input("Add another patient? (y/n): ")

            # saving the patient data to the database
            conn.commit()

        elif menu_selection == INSERT_PROCEDURE_INFO:
            while again_procedure.lower() == "y":
                # get procedure information
                patient_id = int(input("Patient ID: "))
                procedure_name = input("Procedure name: ")
                procedure_date = input("Date: ")
                practitioner = input("Practitioner name: ")
                charge_amount = float(input("Cost of procedure: "))

                # insert the data accordingly
                cur.execute('''INSERT INTO Procedures(ID, ProcedureName, ProcedureDate, Practitioner, Charge)
                                VALUES(?, ?, ?, ?, ?)''',
                            (patient_id, procedure_name, procedure_date, practitioner, charge_amount))

                # add another procedure
                again_procedure = input("Add another procedure? (y/n): ")

            # saving the procedure data
            conn.commit()

    # closing the database connection
    conn.close()


def display_menu_options():
    print("Select one of the following options:")
    print("1 - To insert patient info")
    print("2 - To insert procedure info")
    print("3 - To exit")

# def get_selection():
#     choice = int(input("Enter selection: "))
#
#     while choice < MIN_CHOICE


if __name__ == '__main__':
    main()

