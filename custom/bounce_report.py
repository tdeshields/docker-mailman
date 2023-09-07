import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pickle
import argparse
import subprocess
import json



# creating command line options for running different parts of the script
parser = argparse.ArgumentParser(description='Bounce report script')
parser.add_argument('-r', '--report', action='store_true', help='Send bounce report to list owners, if any.')
parser.add_argument('-p', '--purge', action='store_true', help='Purge emails from lists that have bounced. Requires --report or --noaction to be ran beforehand. Bounce data is wiped following the purge.')
parser.add_argument('-n', '--noaction', action='store_true', help='Build the binary data file without performing any actions with it. Also prints out the bounce data to terminal for viewing. This is mainly for testing purposes')
args = parser.parse_args()

# API variables
api_url = 'http://mailman-core:8001/3.1/'
apiuser = 'restadmin'
apipass = 'restpass'
auth = (apiuser, apipass)

# declaring dictionary for keeping api data
result = {}
bouncefile = 'bounces.pk'

# Email config
email_server = 'smtp.usm.edu'
email_port = 25
from_address = 'itech-helpdesk@usm.edu'
to_address = 'tony.deshields@usm.edu'



# function to send email alert
def send_email(subject, body, from_address, to_address):
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = ', '.join(to_address)
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(email_server, email_port)
        server.starttls()
        server.sendmail(from_address, to_address, msg.as_string())
        server.quit()
        # print('Email sent successfully')
    except Exception as e:
        print(f"Failed to send email alert: {str(e)}")



# function to parse API for list_id, bounce_score, and email addresses that were bounced
def get_list_id():
    response = requests.get(api_url + "members", auth=auth)
    if response.status_code == 200:
        members = response.json()

        for i in members["entries"]:
            list_id = i.get("list_id")
            bounce_score = i.get("bounce_score")
            email = i.get("email")
            if bounce_score > 0:
                if list_id not in result:
                    result[list_id] = {'list_email': '', 'owners': [], 'bouncee': []}
                if i.get("role") == "member":
                    result[list_id]['bouncee'].append({'email': email, 'bounce_score': bounce_score})
    else:
        message = f'Failed to connect to mailman API: \n{response.status_code} {response.text}'
        send_email("API Request Failure", message, 'root@lists.usm.edu', 'tony.deshields@usm.edu')



# retrieving owners for each list that has bounces
def get_owner():
        for i in result.keys():
            response = requests.get(api_url + f"lists/{i}/roster/owner", auth=auth)
            if response.status_code == 200:

                data = response.json()
                owners = []

                for j in data.get("entries", []):
                    owner_email = j.get('email')
                    owners.append(owner_email)
                result[i]['owners'] = owners

            else:
                message = f'Failed to connect to mailman API: \n{response.status_code} {response.text}'
                send_email("API Request Failure", message, 'root@lists.usm.edu', 'tony.deshields@usm.edu')



# retrieving the actual email address of the list 
def get_list():

    response = requests.get(api_url + "lists", auth=auth)
    if response.status_code == 200:
        data = response.json()

        for i in data["entries"]:
            list_id = i.get("list_id")
            if list_id in result:
                result[list_id]["list_email"] = i.get('fqdn_listname')
    else:
        message = f'Failed to connect to mailman API: \n{response.status_code} {response.text}'
        send_email("API Request Failure", message)



# building report structure and inserting data from dictionary
def send_report():
    for i, j in result.items():
        list_email = j['list_email']
        owners = j['owners']
        bouncee = j['bouncee']

        subject = f"Bounce report for {list_email}"
        body = f"You are receiving this email because you are an owner of {list_email}.\n\n"
        body += f"The following emails have bounced in the past 30 days:\n\n"

        for k in bouncee:
            email = k['email']
            bounce_score = k['bounce_score']
            body += f"     {email}\n"

        body += f"\nYou may login at lists.usm.edu to fix these email addresses or they will be purge after 7 days.\n\nPlease contact the iTech Help-Desk @ 601.266.HELP(4357) for further assistance."

    for i in owners:
        send_email(subject, body, from_address, [i])



# creating pickle file to store result data in binary file
def persist_data():
    with open(bouncefile, 'wb') as f:
        pickle.dump(result, f)



# wiping the data in the pickle file. this is called once the purging process is completed error free 
def wipe_data():
    reset = {}
    with open(bouncefile, 'wb') as f:
        pickle.dump(reset, f)



# function to print the result data in json for viewing in terminal
def print_data():
    print(json.dumps(result, indent=4))



# purging the bounced emails from the system and resetting the binary file
def purge():
    errors = []
    # cmd = f'mailman --run-as-root delmembers -m {email} --fromall'
    with open(bouncefile, 'rb') as f:
        pkdata = pickle.load(f)
        # print(json.dumps(pkdata, indent=4))
        for i, j in pkdata.items():
            list_email = j['list_email']
            bouncee_list = j['bouncee']

            for k in bouncee_list:
                email = k['email']
                cmd = f'mailman --run-as-root delmembers -m {email} --fromall'
                # print(email)
                try:
                    subprocess.run(cmd, shell=True, check=True)
                except subprocess.CalledProcessError as e:
                    errors.append(f'Failed to purge {email} from {list_email}. Error: {str(e)}')
                except Exception as e:
                    errors.append(f'An unexpected error occurred while purging {email} from {list_email}. Error: {str(e)}')
    if errors:
        error_message = '\n'.join(errors)
        send_email('bounce purge errors', error_message, 'root@lists.usm.edu', 'tony.deshields@usm.edu')
    else:
        wipe_data()    

            

# main function to call all the functions we have defined.
def main():
        # runs the below code block if we give the -n argument
        if args.noaction:
            get_list_id()
            get_owner()
            get_list()
            if result:
                print_data()
                persist_data()
            else:
                print("no data found")
        elif args.report:
            get_list_id()
            get_owner()
            get_list()
            if result:
                persist_data()
                send_report()
            else:
                print("no data found")
        elif args.purge:
            purge()
            wipe_data()
        else:
            print('Please provide a valid option. See --help.')

        # print(json.dumps(result, indent=4))



if __name__ == "__main__":
        main()
