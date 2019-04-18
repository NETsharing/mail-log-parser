import os
import re
import argparse


def parse_log_file(file_name):
    logged_user_sessions = {}
    sent_emails_statuses = {}

    try:
        if not os.path.exists(file_name):
            raise FileNotFoundError
    except FileNotFoundError:
        print('Error: file does not exist')
        return
    
    with open(file_name) as log_file:
        for log in log_file:
            session_id = re.search(r'\:\s(\w+)\:', log)
            if session_id:
                session_id = session_id.group(1)
            else:
                continue

            if 'sasl_method=' in log:
                logged_user_sessions[session_id] = log.split('sasl_username=')[-1][:-1]

            elif 'to=<' in log:
                if session_id not in logged_user_sessions:
                    continue
                sender_email_address = logged_user_sessions[session_id]
                if sender_email_address not in sent_emails_statuses:
                    sent_emails_statuses[sender_email_address] = {'success': 0, 'errors': 0}
                if 'status=sent' in log:
                    sent_emails_statuses[sender_email_address]['success'] += 1
                else:
                    sent_emails_statuses[sender_email_address]['errors'] += 1

            elif 'removed' in log and session_id in logged_user_sessions:
                del logged_user_sessions[session_id]

    return sent_emails_statuses


def write_parse_data_in_file(parse_data: dict, file_output_path: str):
    with open(file_output_path, 'w') as file_output:
        if not parse_data:
            file_output.write('No data found.')
            return
        for mail_address, mail_status in parse_data.items():
            try:
                file_output.write(f'{mail_address} {mail_status["success"]} {mail_status["errors"]}\n')
            except KeyError:
                file_output.write('Warning: wrong data')


def create_arg_parser():
    parser = argparse.ArgumentParser(description='Parse the mail server log and collect mail statistics.')
    parser.add_argument('input_file_path', help='Path to the mail log file')
    parser.add_argument('-o', '--output_file_path', help='Path to the output file')
    return parser


def main():
    parser = create_arg_parser()
    namespace = parser.parse_args()

    input_file_path = namespace.input_file_path
    output_file_path = namespace.output_file_path or 'output.csv'

    sent_emails_statuses = parse_log_file(input_file_path)
    write_parse_data_in_file(sent_emails_statuses, output_file_path)


if __name__ == '__main__':
    main()