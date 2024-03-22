import json
import os
import requests

def load_users_from_file(file_path):
    with open(file_path, 'r') as file:
        users_data = json.load(file)
    return users_data

def generate_postman_messages(users_data):
    messages = []
    for user_id, user_info in users_data.items():
        message = {
            "user_id": user_id,
            "name": user_info["name"],
            "site_code": user_info["site_code"],
            "imsi": user_info.get("imsi", "")
        }
        messages.append(message)
    return messages

def send_postman_messages(messages, endpoint):
    for message in messages:
        response = requests.post(endpoint, json=message)
        if not response.status_code == 201:
            print(f"Failed to send message for user {message['user_id']}, status code: {response.status_code}")

def main():
    file_path = 'users_data.json'
    users_data = load_users_from_file(file_path)
    postman_messages = generate_postman_messages(users_data)
    postman_endpoint = 'http://10.152.183.41:83'  
    send_postman_messages(postman_messages, postman_endpoint)

if __name__ == "__main__":
    main()
