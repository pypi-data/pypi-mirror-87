# Getting started

This is a sample server Petstore server.  You can find out more about Swagger at [http://swagger.io](http://swagger.io) or on [irc.freenode.net, #swagger](http://swagger.io/irc/).  For this sample, you can use the api key `special-key` to test the authorization filters.

## How to Build


You must have Python ```2 >=2.7.9``` or Python ```3 >=3.4``` installed on your system to install and run this SDK. This SDK package depends on other Python packages like nose, jsonpickle etc. 
These dependencies are defined in the ```requirements.txt``` file that comes with the SDK.
To resolve these dependencies, you can use the PIP Dependency manager. Install it by following steps at [https://pip.pypa.io/en/stable/installing/](https://pip.pypa.io/en/stable/installing/).

Python and PIP executables should be defined in your PATH. Open command prompt and type ```pip --version```.
This should display the version of the PIP Dependency Manager installed if your installation was successful and the paths are properly defined.

* Using command line, navigate to the directory containing the generated files (including ```requirements.txt```) for the SDK.
* Run the command ```pip install -r requirements.txt```. This should install all the required dependencies.

![Building SDK - Step 1](https://apidocs.io/illustration/python?step=installDependencies&workspaceFolder=Swagger%20Petstore-Python)


## How to Use

The following section explains how to use the Apimaticswaggerpetstore SDK package in a new project.

### 1. Open Project in an IDE

Open up a Python IDE like PyCharm. The basic workflow presented here is also applicable if you prefer using a different editor or IDE.

![Open project in PyCharm - Step 1](https://apidocs.io/illustration/python?step=pyCharm)

Click on ```Open``` in PyCharm to browse to your generated SDK directory and then click ```OK```.

![Open project in PyCharm - Step 2](https://apidocs.io/illustration/python?step=openProject0&workspaceFolder=Swagger%20Petstore-Python)     

The project files will be displayed in the side bar as follows:

![Open project in PyCharm - Step 3](https://apidocs.io/illustration/python?step=openProject1&workspaceFolder=Swagger%20Petstore-Python&projectName=apimaticswaggerpetstore)     

### 2. Add a new Test Project

Create a new directory by right clicking on the solution name as shown below:

![Add a new project in PyCharm - Step 1](https://apidocs.io/illustration/python?step=createDirectory&workspaceFolder=Swagger%20Petstore-Python&projectName=apimaticswaggerpetstore)

Name the directory as "test"

![Add a new project in PyCharm - Step 2](https://apidocs.io/illustration/python?step=nameDirectory)
   
Add a python file to this project with the name "testsdk"

![Add a new project in PyCharm - Step 3](https://apidocs.io/illustration/python?step=createFile&workspaceFolder=Swagger%20Petstore-Python&projectName=apimaticswaggerpetstore)

Name it "testsdk"

![Add a new project in PyCharm - Step 4](https://apidocs.io/illustration/python?step=nameFile)

In your python file you will be required to import the generated python library using the following code lines

```Python
from apimaticswaggerpetstore.apimaticswaggerpetstore_client import ApimaticswaggerpetstoreClient
```

![Add a new project in PyCharm - Step 4](https://apidocs.io/illustration/python?step=projectFiles&workspaceFolder=Swagger%20Petstore-Python&libraryName=apimaticswaggerpetstore.apimaticswaggerpetstore_client&projectName=apimaticswaggerpetstore&className=ApimaticswaggerpetstoreClient)

After this you can write code to instantiate an API client object, get a controller object and  make API calls. Sample code is given in the subsequent sections.

### 3. Run the Test Project

To run the file within your test project, right click on your Python file inside your Test project and click on ```Run```

![Run Test Project - Step 1](https://apidocs.io/illustration/python?step=runProject&workspaceFolder=Swagger%20Petstore-Python&libraryName=apimaticswaggerpetstore.apimaticswaggerpetstore_client&projectName=apimaticswaggerpetstore&className=ApimaticswaggerpetstoreClient)


## How to Test

You can test the generated SDK and the server with automatically generated test
cases. unittest is used as the testing framework and nose is used as the test
runner. You can run the tests as follows:

  1. From terminal/cmd navigate to the root directory of the SDK.
  2. Invoke ```pip install -r test-requirements.txt```
  3. Invoke ```nosetests```

## Initialization

### Authentication
In order to setup authentication and initialization of the API client, you need the following information.

| Parameter | Description |
|-----------|-------------|
| o_auth_client_id | OAuth 2 Client ID |
| o_auth_redirect_uri | OAuth 2 Redirection endpoint or Callback Uri |



API client can be initialized as following.

```python
# Configuration parameters and credentials
o_auth_client_id = 'o_auth_client_id' # OAuth 2 Client ID
o_auth_redirect_uri = 'o_auth_redirect_uri' # OAuth 2 Redirection endpoint or Callback Uri

client = ApimaticswaggerpetstoreClient(o_auth_client_id, o_auth_redirect_uri)
```



# Class Reference

## <a name="list_of_controllers"></a>List of Controllers

* [PetController](#pet_controller)
* [StoreController](#store_controller)
* [UserController](#user_controller)

## <a name="pet_controller"></a>![Class: ](https://apidocs.io/img/class.png ".PetController") PetController

### Get controller instance

An instance of the ``` PetController ``` class can be accessed from the API Client.

```python
 pet_controller = client.pet
```

### <a name="upload_file"></a>![Method: ](https://apidocs.io/img/method.png ".PetController.upload_file") upload_file

> uploads an image

```python
def upload_file(self,
                    pet_id,
                    additional_metadata=None,
                    file=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| petId |  ``` Required ```  | ID of pet to update |
| additionalMetadata |  ``` Optional ```  | Additional data to pass to server |
| file |  ``` Optional ```  | file to upload |



#### Example Usage

```python
pet_id = 130
additional_metadata = 'additionalMetadata'
file = open("pathtofile", 'rb')

result = pet_controller.upload_file(pet_id, additional_metadata, file)

```


### <a name="add_pet"></a>![Method: ](https://apidocs.io/img/method.png ".PetController.add_pet") add_pet

> Add a new pet to the store

```python
def add_pet(self,
                body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Required ```  | Pet object that needs to be added to the store |



#### Example Usage

```python
body = Pet()

pet_controller.add_pet(body)

```

#### Errors

| Error Code | Error Description |
|------------|-------------------|
| 405 | Invalid input |




### <a name="update_pet"></a>![Method: ](https://apidocs.io/img/method.png ".PetController.update_pet") update_pet

> Update an existing pet

```python
def update_pet(self,
                   body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Required ```  | Pet object that needs to be added to the store |



#### Example Usage

```python
body = Pet()

pet_controller.update_pet(body)

```

#### Errors

| Error Code | Error Description |
|------------|-------------------|
| 400 | Invalid ID supplied |
| 404 | Pet not found |
| 405 | Validation exception |




### <a name="find_pets_by_status"></a>![Method: ](https://apidocs.io/img/method.png ".PetController.find_pets_by_status") find_pets_by_status

> Multiple status values can be provided with comma separated strings

```python
def find_pets_by_status(self,
                            status)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| status |  ``` Required ```  ``` Collection ```  | Status values that need to be considered for filter |



#### Example Usage

```python
status = [Status2Enum.AVAILABLE]

result = pet_controller.find_pets_by_status(status)

```

#### Errors

| Error Code | Error Description |
|------------|-------------------|
| 400 | Invalid status value |




### <a name="find_pets_by_tags"></a>![Method: ](https://apidocs.io/img/method.png ".PetController.find_pets_by_tags") find_pets_by_tags

> Multiple tags can be provided with comma separated strings. Use tag1, tag2, tag3 for testing.

```python
def find_pets_by_tags(self,
                          tags)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| tags |  ``` Required ```  ``` Collection ```  | Tags to filter by |



#### Example Usage

```python
tags = ['tags']

result = pet_controller.find_pets_by_tags(tags)

```

#### Errors

| Error Code | Error Description |
|------------|-------------------|
| 400 | Invalid tag value |




### <a name="get_pet_by_id"></a>![Method: ](https://apidocs.io/img/method.png ".PetController.get_pet_by_id") get_pet_by_id

> Returns a single pet

```python
def get_pet_by_id(self,
                      pet_id)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| petId |  ``` Required ```  | ID of pet to return |



#### Example Usage

```python
pet_id = 130

result = pet_controller.get_pet_by_id(pet_id)

```

#### Errors

| Error Code | Error Description |
|------------|-------------------|
| 400 | Invalid ID supplied |
| 404 | Pet not found |




### <a name="update_pet_with_form"></a>![Method: ](https://apidocs.io/img/method.png ".PetController.update_pet_with_form") update_pet_with_form

> Updates a pet in the store with form data

```python
def update_pet_with_form(self,
                             pet_id,
                             name=None,
                             status=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| petId |  ``` Required ```  | ID of pet that needs to be updated |
| name |  ``` Optional ```  | Updated name of the pet |
| status |  ``` Optional ```  | Updated status of the pet |



#### Example Usage

```python
pet_id = 130
name = 'name'
status = 'status'

pet_controller.update_pet_with_form(pet_id, name, status)

```

#### Errors

| Error Code | Error Description |
|------------|-------------------|
| 405 | Invalid input |




### <a name="delete_pet"></a>![Method: ](https://apidocs.io/img/method.png ".PetController.delete_pet") delete_pet

> Deletes a pet

```python
def delete_pet(self,
                   pet_id,
                   api_key=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| petId |  ``` Required ```  | Pet id to delete |
| apiKey |  ``` Optional ```  | TODO: Add a parameter description |



#### Example Usage

```python
pet_id = 130
api_key = 'api_key'

pet_controller.delete_pet(pet_id, api_key)

```

#### Errors

| Error Code | Error Description |
|------------|-------------------|
| 400 | Invalid ID supplied |
| 404 | Pet not found |




[Back to List of Controllers](#list_of_controllers)

## <a name="store_controller"></a>![Class: ](https://apidocs.io/img/class.png ".StoreController") StoreController

### Get controller instance

An instance of the ``` StoreController ``` class can be accessed from the API Client.

```python
 store_controller = client.store
```

### <a name="create_place_order"></a>![Method: ](https://apidocs.io/img/method.png ".StoreController.create_place_order") create_place_order

> Place an order for a pet

```python
def create_place_order(self,
                           body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Required ```  | order placed for purchasing the pet |



#### Example Usage

```python
body = Order()

result = store_controller.create_place_order(body)

```

#### Errors

| Error Code | Error Description |
|------------|-------------------|
| 400 | Invalid Order |




### <a name="get_order_by_id"></a>![Method: ](https://apidocs.io/img/method.png ".StoreController.get_order_by_id") get_order_by_id

> For valid response try integer IDs with value >= 1 and <= 10. Other values will generated exceptions

```python
def get_order_by_id(self,
                        order_id)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| orderId |  ``` Required ```  | ID of pet that needs to be fetched |



#### Example Usage

```python
order_id = 130

result = store_controller.get_order_by_id(order_id)

```

#### Errors

| Error Code | Error Description |
|------------|-------------------|
| 400 | Invalid ID supplied |
| 404 | Order not found |




### <a name="delete_order"></a>![Method: ](https://apidocs.io/img/method.png ".StoreController.delete_order") delete_order

> For valid response try integer IDs with positive integer value. Negative or non-integer values will generate API errors

```python
def delete_order(self,
                     order_id)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| orderId |  ``` Required ```  | ID of the order that needs to be deleted |



#### Example Usage

```python
order_id = 130

store_controller.delete_order(order_id)

```

#### Errors

| Error Code | Error Description |
|------------|-------------------|
| 400 | Invalid ID supplied |
| 404 | Order not found |




### <a name="get_inventory"></a>![Method: ](https://apidocs.io/img/method.png ".StoreController.get_inventory") get_inventory

> Returns a map of status codes to quantities

```python
def get_inventory(self)
```

#### Example Usage

```python

result = store_controller.get_inventory()

```


[Back to List of Controllers](#list_of_controllers)

## <a name="user_controller"></a>![Class: ](https://apidocs.io/img/class.png ".UserController") UserController

### Get controller instance

An instance of the ``` UserController ``` class can be accessed from the API Client.

```python
 user_controller = client.user
```

### <a name="create_users_with_array_input"></a>![Method: ](https://apidocs.io/img/method.png ".UserController.create_users_with_array_input") create_users_with_array_input

> Creates list of users with given input array

```python
def create_users_with_array_input(self,
                                      body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Required ```  ``` Collection ```  | List of user object |



#### Example Usage

```python
body = [User()]

user_controller.create_users_with_array_input(body)

```

#### Errors

| Error Code | Error Description |
|------------|-------------------|
| 0 | successful operation |




### <a name="create_users_with_list_input"></a>![Method: ](https://apidocs.io/img/method.png ".UserController.create_users_with_list_input") create_users_with_list_input

> Creates list of users with given input array

```python
def create_users_with_list_input(self,
                                     body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Required ```  ``` Collection ```  | List of user object |



#### Example Usage

```python
body = [User()]

user_controller.create_users_with_list_input(body)

```

#### Errors

| Error Code | Error Description |
|------------|-------------------|
| 0 | successful operation |




### <a name="get_user_by_name"></a>![Method: ](https://apidocs.io/img/method.png ".UserController.get_user_by_name") get_user_by_name

> Get user by user name

```python
def get_user_by_name(self,
                         username)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| username |  ``` Required ```  | The name that needs to be fetched. Use user1 for testing. |



#### Example Usage

```python
username = 'username'

result = user_controller.get_user_by_name(username)

```

#### Errors

| Error Code | Error Description |
|------------|-------------------|
| 400 | Invalid username supplied |
| 404 | User not found |




### <a name="update_user"></a>![Method: ](https://apidocs.io/img/method.png ".UserController.update_user") update_user

> This can only be done by the logged in user.

```python
def update_user(self,
                    username,
                    body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| username |  ``` Required ```  | name that need to be updated |
| body |  ``` Required ```  | Updated user object |



#### Example Usage

```python
username = 'username'
body = User()

user_controller.update_user(username, body)

```

#### Errors

| Error Code | Error Description |
|------------|-------------------|
| 400 | Invalid user supplied |
| 404 | User not found |




### <a name="delete_user"></a>![Method: ](https://apidocs.io/img/method.png ".UserController.delete_user") delete_user

> This can only be done by the logged in user.

```python
def delete_user(self,
                    username)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| username |  ``` Required ```  | The name that needs to be deleted |



#### Example Usage

```python
username = 'username'

user_controller.delete_user(username)

```

#### Errors

| Error Code | Error Description |
|------------|-------------------|
| 400 | Invalid username supplied |
| 404 | User not found |




### <a name="get_login_user"></a>![Method: ](https://apidocs.io/img/method.png ".UserController.get_login_user") get_login_user

> Logs user into the system

```python
def get_login_user(self,
                       username,
                       password)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| username |  ``` Required ```  | The user name for login |
| password |  ``` Required ```  | The password for login in clear text |



#### Example Usage

```python
username = 'username'
password = 'password'

result = user_controller.get_login_user(username, password)

```

#### Errors

| Error Code | Error Description |
|------------|-------------------|
| 400 | Invalid username/password supplied |




### <a name="get_logout_user"></a>![Method: ](https://apidocs.io/img/method.png ".UserController.get_logout_user") get_logout_user

> Logs out current logged in user session

```python
def get_logout_user(self)
```

#### Example Usage

```python

user_controller.get_logout_user()

```

#### Errors

| Error Code | Error Description |
|------------|-------------------|
| 0 | successful operation |




### <a name="create_user"></a>![Method: ](https://apidocs.io/img/method.png ".UserController.create_user") create_user

> This can only be done by the logged in user.

```python
def create_user(self,
                    body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Required ```  | Created user object |



#### Example Usage

```python
body = User()

user_controller.create_user(body)

```

#### Errors

| Error Code | Error Description |
|------------|-------------------|
| 0 | successful operation |




[Back to List of Controllers](#list_of_controllers)



