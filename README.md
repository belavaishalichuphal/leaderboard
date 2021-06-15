#Installation-
>virtualenv --python=python3 venv
>source venv/bin/activate
>pip install -r requirements.txt 


##Running the project-
>cd leaderboard
>python run.py

##Testcase Execution-
>python -m unittest -v tests.py

#API's
### 1. Add user
#### API Endpoint - http://localhost:5000/user/
#### HTTP Method - POST
#### Body - 
{
    "name": <required:str>,
    "age": <required:str/int>,
    "address": <required:str>
}
#### Response
{
    "response": "Successfully Added User"
}

### 2. Get sorted user list
#### API Endpoint - http://localhost:5000/user/
#### HTTP Method - GET
### Response - 
{
    "response": [
        {
            "1": {
                "address": "goa, india",
                "age": "19",
                "name": "XYZ",
                "points": 0
            }
        },
    ]
}

### 3. Increase/Decrease score
#### API Endpoint - http://localhost:5000/score/<id:int>/?operation=minus
#### HTTP Method - Patch
#### Query Params - operation=minus/plus
#### Body - { "points": 10} 
Note - If body is passed then it will take precedence
#### Response -
{
    "response": "Updated score for user 2 , score - -20"
}

### 4. Delete user
#### API Endpoint - http://localhost:5000/user/<id:int>
#### HTTP Method - DELETE
### Response - 
{
    "response": "XYZ User Removed"
}


##API's response when no data is found
{
    "error": "Not found message"
}

##API's response on error
{
    "error": "error message"
}

Note - All API's have Basic Authentication with below credentials
username - "api-key"
password - "generatesomesecurekeyforthis"