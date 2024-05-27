import requests
import json

BASE_URL = 'http://127.0.0.1:5000'

def test_register():
    url = f'{BASE_URL}/auth/register'
    payload = {
        'username': 'testuser',
        'password': 'testpassword'
    }
    response = requests.post(url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    print(f'Register: {response.json()}')

def test_get_stocks():
    url = f'{BASE_URL}/stocks/'
    response = requests.get(url)
    try:
        stocks = response.json()
    except requests.exceptions.JSONDecodeError:
        print('Get Stocks: Response is not valid JSON')
        print(f'Response text: {response.text}')
        return
    print(f'Get Stocks: {stocks}')

def fetch_user_id(username):
    url = f'{BASE_URL}/auth/get_user_id'
    params = {'username': username}
    response = requests.get(url, params=params)
    try:
        user_data = response.json()
        print(f"Fetched user ID for {username}: {user_data.get('_id')}")
        return user_data.get('_id')
    except requests.exceptions.JSONDecodeError:
        print('Fetch User ID: Response is not valid JSON')
        print(f'Response text: {response.text}')
        return None

def test_buy_stock():
    user_id = fetch_user_id('testuser')
    if not user_id:
        print("User ID not found, cannot proceed with test_buy_stock")
        return

    print(f"User ID for buying stock: {user_id}")

    url = f'{BASE_URL}/transactions/buy'
    payload = {
        'user_id': user_id,
        'stock_symbol': 'SFCM',
        'quantity': 10
    }
    response = requests.post(url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    print(f'Buy Stock: {response.json()}')

def test_sell_stock():
    user_id = fetch_user_id('testuser')
    if not user_id:
        print("User ID not found, cannot proceed with test_sell_stock")
        return

    print(f"User ID for selling stock: {user_id}")

    url = f'{BASE_URL}/transactions/sell'
    payload = {
        'user_id': user_id,
        'stock_symbol': 'SFCM',
        'quantity': 5
    }
    response = requests.post(url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    print(f'Sell Stock: {response.json()}')

def test_get_portfolio():
    user_id = fetch_user_id('testuser')
    if not user_id:
        print("User ID not found, cannot proceed with test_get_portfolio")
        return

    print(f"User ID for fetching portfolio: {user_id}")

    url = f'{BASE_URL}/portfolio/'
    params = {'user_id': user_id}
    response = requests.get(url, params=params)
    try:
        portfolio = response.json()
    except requests.exceptions.JSONDecodeError:
        print('Get Portfolio: Response is not valid JSON')
        print(f'Response text: {response.text}')
        return
    print(f'Get Portfolio: {portfolio}')

def test_verify_transaction():
    url = f'{BASE_URL}/transactions/'
    response = requests.get(url)
    try:
        transactions = response.json()
    except requests.exceptions.JSONDecodeError:
        print('Get Transactions: Response is not valid JSON')
        print(f'Response text: {response.text}')
        return
    print(f'Get Transactions: {transactions}')

if __name__ == '__main__':
    test_register()
    test_get_stocks()
    test_buy_stock()
    test_sell_stock()  # Add this line to test selling stock
    test_get_portfolio()
    test_verify_transaction()
