import pytest
import requests

# Get stocks_list from root directory
from stocks_list import *
# Define stocks to perform operations on
# URL of docker container for stocks and capital-gains
STOCKS_URL = 'http://localhost:5001/'
CAPITAL_GAINS_URL = 'http://localhost:5003/'

# Post stocks to the stocks service
def post_stock(stock):
    # Post stocks to the stocks service
    response = requests.post(STOCKS_URL + 'stocks', json=stock)
    # Return response and status code
    return [response.json(), response.status_code]

# Update a specific stock
def put_stock(stock, id):
    # add "id" label to copy of stock
    deepcopy_stock = stock.copy()
    deepcopy_stock['id'] = id
    # Put the stock
    response = requests.put(STOCKS_URL + 'stocks/' + id, json=deepcopy_stock)
    return [response.json(), response.status_code]

# get specific stock
def get_stock(id):
    response = requests.get(STOCKS_URL + 'stocks/' + id)
    return [response.json(), response.status_code]

# get all stocks
def get_stocks():
    response = requests.get(STOCKS_URL + 'stocks')
    # assert response.status_code == 200
    return [response.json(), response.status_code]

# Delete specific stock
def delete_stock(id):
    response = requests.delete(STOCKS_URL + 'stocks/' + id)
    return response.status_code

# Delete all stocks that were posted
def delete_all():
    response = get_stocks()[0]
    for stock in response:
        id = stock['id']
        response = requests.delete(STOCKS_URL + 'stocks/' + id)
        assert response.status_code == 204

# Get all ids of stocks
def get_all_ids():
    response = get_stocks()
    all_stocks = response[0]
    global_id = [stock['id'] for stock in all_stocks]
    return global_id

global global_id
global_id = []
stock_value = []

def test_1():
    # Execute three post requests on stock1-3
    stock1_result = post_stock(stock1)
    stock2_result = post_stock(stock2)
    stock3_result = post_stock(stock3)
    # Check if the status code is 201 for all
    assert stock1_result[1] == 201
    assert stock2_result[1] == 201
    assert stock3_result[1] == 201
    # assert all three have unique ids
    assert stock1_result[0]['id'] != stock2_result[0]['id']
    assert stock1_result[0]['id'] != stock3_result[0]['id']
    assert stock2_result[0]['id'] != stock3_result[0]['id']
    # add all three ids to a global list
    global_id = [stock1_result[0]['id'], stock2_result[0]['id'], stock3_result[0]['id']]

def test_2():
    # Execute a get stocks/id request for stock1
    stock1_get = get_stock(global_id[0])
    # Check if the status code is 200
    assert stock1_get[1] == 200
    # Check if the stock symbol is NVDA
    assert stock1_get[0]['symbol'] == 'NVDA'

def test_3():
    # Execute a get stocks request
    all_stocks = get_stocks()
    # Check if the status code is 200
    assert all_stocks[1] == 200
    # Check if the length of the list is 3
    assert len(all_stocks[0]) == 3
    # store all three ids in a list
    global_id = [stock['id'] for stock in all_stocks[0]]
def test_4():
    symbol_fields = ['NVDA', 'AAPL', 'GOOG']
    # execute 3 stock get requests for the three ids of stock1-3
    for id in global_id:
        stock = get_stock(id)
        # Check if the status code is 200
        assert stock[1] == 200
        # Check if the symbol equals its corresponding symbol in symbol_fields
        assert stock[0]['symbol'] == symbol_fields[global_id.index(id)]
        # Store all three stock values in a list
        stock_value.append(stock[0]['stock value'])

def test_5():
    # Execute a get portfolio value request
    portfolio_value = requests.get(STOCKS_URL + 'portfolio-value')
    # Check if the status code is 200
    assert portfolio_value.status_code == 200
    # Assert that portfolio value is within bounds
    total_value = sum(stock_value)
    assert portfolio_value.json()['portfolio value']*0.97 <= total_value 
    assert portfolio_value.json()['portfolio value']*1.03 >= total_value

def test_6():
    # Execute a post request with stock 7
    stock7_result = post_stock(stock7)
    # Is succesful if status code is 400 (symbol not provided)
    assert stock7_result[1] == 400

def test_7():
    # Delete stock2 
    del_status = delete_stock(global_id[1])
    # Check if the status code is 204
    assert del_status == 204

def test_8():
    # Execute a get request for stock2
    stock2_get = get_stock(global_id[1])
    # Check if the status code is 404
    assert stock2_get[1] == 404

def test_9():
    # Execute a post request with stock 8
    stock8_result = post_stock(stock8)
    # Is succesful if status code is 400 (purchase date format)
    assert stock8_result[1] == 400












# # post stock and get it
# def test_post_get():
#     # Delete all stocks
#     delete_all()
#     # Post Google Stock
#     post_result = post_stock(google_stock)
#     # Test if the stock was posted
#     assert post_result[1] == 201
#     # Get the id of the stock  
#     id = post_result[0]['id']
#     # Get all stocks
#     get_result = get_stocks()
#     # Check if the get request was successful
#     assert get_result[1] == 200
#     # Get all stocks
#     all_stocks = get_result[0]
#     # Check if the stock is in the list
#     for stock in all_stocks:
#         if stock['id'] == id:
#             assert stock["symbol"] == google_stock["symbol"]
#     # Attempt to post same stock symbol again
#     post_status = post_stock(google_stock)
#     assert post_status[1] == 400

# def test_put():
#     # Replace the google stock with tesla
#     id = get_stocks()[0][0]['id']
#     put_status = put_stock(tesla_stock, id)
#     # print this log
#     assert put_status[1] == 200
#     # Ensure id is the same
#     assert put_status[0]['id'] == id
#     # Get Stocks and ensure the new symbol is tesla symbol
#     for stock in get_stocks()[0]:
#         if stock['id'] == 3:
#             assert stock['symbol'] == tesla_stock['symbol']
#     # Attempt to put stock with invalid id
#     put_status = put_stock(tesla_stock, '123')
#     assert put_status[1] == 404

# def test_del_stock():
#     id = get_stocks()[0][0]['id']
#     del_status = requests.delete(STOCKS_URL + 'stocks/' + id)
#     assert del_status.status_code == 204


# def test_stock_value():
#     google = post_stock(google_stock)
#     apple = post_stock(apple_stock)
#     nvidia = post_stock(nvidia_stock)

#     # Get the stock value of google
#     value_status = requests.get(STOCKS_URL + 'stock-value/' + google[0]['id'])
#     assert value_status.status_code == 200
#     # Get the stock value of apple
#     value_status = requests.get(STOCKS_URL + 'stock-value/' + apple[0]['id'])
#     assert value_status.status_code == 200
#     # Get the stock value of nvidia
#     value_status = requests.get(STOCKS_URL + 'stock-value/' + nvidia[0]['id'])
#     assert value_status.status_code == 200

#     # Assert that the value are over 0
#     assert value_status.json()['stock value'] > 0

# def test_portfolio_value():
#     # get portfolio value
#     value = requests.get(STOCKS_URL + 'portfolio-value')
#     assert value.status_code == 200
#     # Assert total value is greater than 200
#     assert value.json()['portfolio value'] > 1000

# def test_capital_gains():
#     # get capital gains
#     gains = requests.get(CAPITAL_GAINS_URL + 'capital-gains')
#     assert gains.status_code == 200
#     # Assert total gains is greater than 200
#     assert gains.json()['total gains'] > 200
    

# Run all tests
if __name__ == "__main__":
    print("Running tests")
    pytest.main()


