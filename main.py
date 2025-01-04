import os
from dotenv import load_dotenv
import csv
import json
import google.generativeai as genai
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from utils.templates import CORE_COLD_EMAIL, SOFTWARE_DEV_COLD_EMAIL

# Load the environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SMTP_HOST = os.getenv("SMTP_HOST")
PORT = int(os.getenv("PORT"))
NAME = os.getenv("NAME")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


# Paths configuration
CSV_DATA_PATH = "data/data.csv"
CV_FOLDER = "CV"


# Create a model
genai.configure(api_key=GEMINI_API_KEY)
generative_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}   # We choose less random and more consistent responses 
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-8b",
    generation_config=generative_config
)


def get_ai_response(prompt):
    response = model.generate_content(prompt)
    return response.text

def send_email(email: str,ai_response: str, focused_on: str) -> None:
    
    # Parse the ai response
    parsed_response = json.loads(ai_response)
    
    # Initialize the mailer object & attach contents
    mailer_object = MIMEMultipart()
    mailer_object['From'] = f"{NAME} <{EMAIL}>"
    mailer_object['To'] = f"{email}"
    mailer_object["Subject"] = parsed_response.get("subject")
    mailer_object.attach(MIMEText(parsed_response.get("body"), "plain"))
    
    # Attach resume
    with open(f"{CV_FOLDER}/{focused_on}.pdf", 'rb') as attachment:
        attachment_ = MIMEApplication(attachment.read())
        attachment_.add_header('Content-Disposition', 'attachment', filename=f"Manas_Resume.pdf")
        mailer_object.attach(attachment_)
        
    # Send mail
    try:
        connection = SMTP(host=SMTP_HOST,port=PORT ,timeout=50)
        connection.starttls()
        connection.login(user=EMAIL, password=PASSWORD)
        connection.sendmail(mailer_object["From"], mailer_object["To"], mailer_object.as_string())
        connection.quit()
        
        print(f"Successfully sent email to: {email}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Get the data from the csv
def get_data():
    # Get the  data abd store it in dataframe
    data_list = []

    with open(CSV_DATA_PATH, mode='r', newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            data_list.append(row)

    return data_list

# Main function
def main() :

    # Get the data from the csv
    data_list = get_data()
    # Run the loop and mail individually
    for data in data_list:

        # Get the type of CORE or Software DEV
        focused_on = data.get('type')

        if (focused_on == 'Chemical Engineer'):
            template_msg = CORE_COLD_EMAIL
        elif (focused_on == "Software Dev"):
            template_msg = SOFTWARE_DEV_COLD_EMAIL
        else:
            print(f"Skipping the data (invalid type: {focussed_on}): \n\n{data}\n\n")
            continue
        
        # Tailored prompt
        prompt = f'''You need to create a cold email. Use the template and the provided details to generate the email. Here's the process:

        1. The template with the structure of the email:
        {template_msg} 

        2. Details about the company, HR, or contact in JSON format, some information might not be there so don't take part of that component from the above template. Also some instruction might be there which you need to follow in the below data:
        {data}

        3. If the details are enough about the compnay or the contact person then include that otherwise don't, though you can include the company name in the subject always

        3. Ensure the email signature is exactly as follows:
    
        --
        Manas Poddar
        📧 Email: iamscientistmanas@gmail.com, manas@scienmanas.xyz
        🐙 Github: https://github.com/scienmanas
        🌐 Web: https://scienmanas.xyz

        4. Format the email response properly:
            - Use escape sequences (`\\n`) to break lines or paragraphs.
            - Do not split or break the lines improperly use as it in template

        The response must be in JSON format as described below:
        {{
            "subject": "Subject of the email with company name",
            "body": "Body of the email."
        }}

        5. The generated email should be ready to send without review, so ensure it's perfect, no typos, no grammatical errors, no formatting issues, no [fill it here] things. If information is not sufficient enough just ignore that part don't include it in email. Also if no information is mentioned about the company or contact then just ignore that part and don't include it in email.
        
        6. Keep the email length small and concise.

        Generate the email carefully by following these instructions.
        '''

        # Get email by ai
        ai_response = get_ai_response(prompt=prompt)
        send_email(email=data.get('email') ,ai_response=ai_response, focused_on=focused_on) 
        

# Start the system
print("Starting the system...")
main()
print("Execution completed!")