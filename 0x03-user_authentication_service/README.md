# 0x03-user_authentication_service

### Declaring API Routes in Flask

To declare API routes in Flask, you can use the `@app.route()` decorator with a specific endpoint:

```python
@app.route('/api/data', methods=['GET'])
def get_data():
    # Route logic here
    return {'message': 'Data retrieved successfully'}
```

Key points:
- Specify the endpoint (e.g., '/api/data')
- Define allowed HTTP methods (e.g., ['GET', 'POST'])

### Getting and Setting Cookies

To set cookies:

```python
from flask import make_response

@app.route('/')
def set_cookie():
    resp = make_response('Cookie set')
    resp.set_cookie('username', 'John Doe')
    return resp
```

To get cookies:

```python
from flask import request

@app.route('/get-cookie')
def get_cookie():
    username = request.cookies.get('username')
    return f'Cookie value: {username}'
```

### Retrieving Request Form Data

To retrieve form data from a POST request:

```python
@app.route('/process_form', methods=['POST'])
def process_form():
    name = request.form.get('name')
    email = request.form.get('email')
    # Process form data
    return 'Form processed successfully'
```

### Returning Various HTTP Status Codes

There are two main ways to set status codes:

1. Using `make_response()`:

```python
from flask import make_response

@app.route('/api/data')
def get_data():
    resp = make_response('Data retrieved')
    resp.status_code = 200
    return resp
```

2. Directly returning the status code:

```python
@app.route('/api/data')
def get_data():
    return {'message': 'Data retrieved'}, 200
```

For other common status codes:

```python
# 404 Not Found
return '', 404

# 500 Internal Server Error
return '', 500
