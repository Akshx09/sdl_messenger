from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import pandas as pd
import re
import pywhatkit as kit
import os

# Add the function to generate the invalid students Excel
def generate_invalid_excel(request):
    # Check if the invalid_students.xlsx file exists
    file_path = 'invalid_students.xlsx'
    if os.path.exists(file_path):
        with open(file_path, 'rb') as excel_file:
            response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename={file_path}'
            return response
    else:
        return render(request, 'messenger/upload.html', {'error': 'Invalid students report not found. Please process files first.'})

# Your existing views...

def validate_phone_number(phone):
    # Indian phone numbers should be 10 digits long and start with 7, 8, or 9
    return bool(re.match(r'^[789]\d{9}$', phone))

def process_files(marks_file, phone_file):
    # Load the Excel files into DataFrames
    marks_df = pd.read_excel(marks_file)
    phone_df = pd.read_excel(phone_file)

    # Check for valid columns
    if not all(col in marks_df.columns for col in ['Student Name', 'Enrollment No', 'Marks']):
        return None, "Marks file must contain 'Student Name', 'Enrollment No', and 'Marks'.", None, None

    if not all(col in phone_df.columns for col in ['Student Name', 'Enrollment No', 'Phone No']):
        return None, "Phone numbers file must contain 'Student Name', 'Enrollment No', and 'Phone No'.", None, None

    # Merge DataFrames to find students present in only one file
    merged_df = pd.merge(marks_df, phone_df, on=['Student Name', 'Enrollment No'], how='outer', indicator=True)

    # Filter students with invalid or missing phone numbers
    invalid_phone_df = merged_df[
        (merged_df['_merge'] == 'right_only') |
        (merged_df['Phone No'].isnull()) |
        (merged_df['Phone No'].apply(lambda x: not validate_phone_number(str(x).replace('+91', '').strip())))
    ][['Student Name', 'Enrollment No']]

    return invalid_phone_df, None, marks_df, phone_df

def send_whatsapp_message(phone, name, enrollment_no, marks):
    message = f"Hello {name}, your marks are {marks}. Enrollment No: {enrollment_no}"
    try:
        kit.sendwhatmsg_instantly(f"+91{phone}", message, 15)
        print(f"Message sent to {name} at {phone}.")
    except Exception as e:
        print(f"Failed to send message to {name} at {phone}: {str(e)}")

def upload_files(request):
    if request.method == 'POST' and request.FILES:
        marks_file = request.FILES['marks_file']
        phone_file = request.FILES['phone_file']
        
        fs = FileSystemStorage()
        marks_path = fs.save(marks_file.name, marks_file)
        phone_path = fs.save(phone_file.name, phone_file)
        
        # Process files and generate report
        invalid_students_df, error_message, marks_df, phone_df = process_files(marks_path, phone_path)
        if error_message:
            return render(request, 'messenger/upload.html', {'error': error_message})
        
        # Save invalid students report
        invalid_students_df.to_excel('invalid_students.xlsx', index=False)

        # Send WhatsApp messages to valid students
        for _, row in marks_df.iterrows():
            student_name = row['Student Name']
            enrollment_no = row['Enrollment No']
            marks = row['Marks']
            phone_no_row = phone_df.loc[phone_df['Student Name'] == student_name]

            if not phone_no_row.empty:
                phone_no = phone_no_row['Phone No'].values[0]
                if validate_phone_number(str(phone_no).replace('+91', '').strip()):
                    send_whatsapp_message(phone_no, student_name, enrollment_no, marks)

        return render(request, 'messenger/upload.html', {'message': 'Process completed. Report saved as invalid_students.xlsx'})

    return render(request, 'messenger/upload.html')

