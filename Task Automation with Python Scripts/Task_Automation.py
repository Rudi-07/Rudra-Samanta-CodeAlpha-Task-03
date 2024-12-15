import os
import shutil
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import time
from datetime import datetime
import getpass 
def organize_files(source_directory):
    print("Organizing files...")
    categories = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
        'Documents': ['.pdf', '.txt', '.docx', '.xlsx', '.pptx'],
        'Videos': ['.mp4', '.mkv', '.avi', '.mov'],
        'Audio': ['.mp3', '.wav', '.aac'],
        'Others': []
    }

    for folder in categories:
        folder_path = os.path.join(source_directory, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    for filename in os.listdir(source_directory):
        file_path = os.path.join(source_directory, filename)
        if os.path.isfile(file_path):
            file_extension = os.path.splitext(filename)[1].lower()
            moved = False
            for folder, extensions in categories.items():
                if file_extension in extensions:
                    shutil.move(file_path, os.path.join(source_directory, folder, filename))
                    print(f"Moved: {filename} to {folder}")
                    moved = True
                    break
            if not moved:
                shutil.move(file_path, os.path.join(source_directory, 'Others', filename))
                print(f"Moved: {filename} to Others")
    print("File organization complete!")

def clean_data(input_file, output_file):
    print("Cleaning data...")
    try:
        data = pd.read_csv(input_file)
        data.dropna(inplace=True)  
        data.columns = [col.strip().lower() for col in data.columns] 
        data.to_csv(output_file, index=False)
        print(f"Cleaned data saved to {output_file}")
    except Exception as e:
        print(f"Error cleaning data: {e}")

def backup_files(source_directory, backup_directory):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_folder = os.path.join(backup_directory, f"backup_{timestamp}")
    os.makedirs(backup_folder, exist_ok=True)

    for filename in os.listdir(source_directory):
        file_path = os.path.join(source_directory, filename)
        if os.path.isfile(file_path):
            shutil.copy(file_path, os.path.join(backup_folder, filename))
            print(f"Backed up: {filename}")
    
    print(f"Backup complete! Files saved to {backup_folder}")

def send_email(subject, body, to_email, from_email, from_password, attachment=None):
    try:
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        if attachment:
            with open(attachment, 'rb') as file:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(attachment)}")
                msg.attach(part)
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def main():
    print("Choose a task to automate:")
    print("1. File Organization")
    print("2. Data Cleaning")
    print("3. File Backup")
    print("4. Send Automated Email")

    task_choice = input("Enter the task number (1-4): ")

    if task_choice == '1':
        source_directory = input("Enter the source directory for file organization: ")
        organize_files(source_directory)
    elif task_choice == '2':
        input_file = input("Enter the input CSV file path for data cleaning: ")
        output_file = input("Enter the output file path to save cleaned data: ")
        clean_data(input_file, output_file)
    elif task_choice == '3':
        source_directory = input("Enter the source directory for backup: ")
        backup_directory = input("Enter the backup directory: ")
        backup_files(source_directory, backup_directory)
    elif task_choice == '4':
        subject = input("Enter the email subject: ")
        body = input("Enter the email body: ")
        to_email = input("Enter the recipient's email address: ")
        from_email = input("Enter your email address: ")

        from_password = getpass.getpass(prompt="Enter your email password (or app-specific password): ")

        attachment = input("Enter the attachment file path (or press Enter to skip): ")
        if attachment == "":  
            attachment = None
        send_email(subject, body, to_email, from_email, from_password, attachment)
    else:
        print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
