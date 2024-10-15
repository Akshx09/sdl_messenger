# sdl_messenger
The purpose of this project is to develop an application that allows educational institutions to validate student information by comparing data from two different Excel files. Additionally, it enables sending WhatsApp messages to students with information about their marks. The application will identify discrepancies in student data, such as incorrect or missing phone numbers, and generate reports.
The objectives of the project are:
- To automate the validation of student data from multiple Excel files.
- To generate a report of discrepancies.
- To send WhatsApp messages to students with their marks using valid phone numbers

the input for files are students name, enrollment no and marks whereas for file 2 is name, enrollment no and marks. the output file generated has name and phone no along with enrollment no.
Usage

Upload Excel Files Navigate to http://127.0.0.1:8000/messenger/upload/. Upload two Excel files: Marks File: Contains columns Student Name, Enrollment No, and Marks. Phone Numbers File: Contains columns Student Name, Enrollment No, and Phone No.
Send WhatsApp Messages Once the files are uploaded, the app:
Validates phone numbers based on Indian standards (10 digits, starting with 7, 8, or 9). Sends WhatsApp messages to students with valid phone numbers about their marks. Messages will be sent using WhatsApp Web via the pywhatkit library.

Generate Invalid Students Report The app also generates an Excel report called invalid_students.xlsx containing:
Students with missing or invalid phone numbers. Students present in one file but missing in the other (marks or phone numbers file). 4. Download the Invalid Students Excel A separate button is available to generate and download the invalid_students.xlsx report if needed.
