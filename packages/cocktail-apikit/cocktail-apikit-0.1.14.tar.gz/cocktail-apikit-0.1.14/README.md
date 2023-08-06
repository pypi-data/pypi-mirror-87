# Cocktail ApiKit

A collection of tools which will be used in all new API project, which including: Bottle, marshmallow, mongo and aws

![apikit structure](./doc/media/APIKIT.png)

## Dependencies

- pymongo: 3.7.2
- marshmallow: 2.16.3
- bottle: 0.12.16
- apispec: 0.39.0
- boto3: 1.9.115
- botocore: 1.12.115

## Usage Example

### 1. Install cocktail apikit

```shell
pip install cocktail-apikit
```

### 2. Create a demo project

#### 2.1 Recommend api project structure

```plain
example/
    __init__.py

    settings.py
    application.py

    config/
        database.ini
    api/
        __init__.py
        demo.py

    schema/
        __init__.py
        demo.py
```

#### 2.2 plain text configuration file **database.ini**

Use **$VAR_NAME** can support Environment variable, if API_ENV specified, then the corresponding API_ENV configuration
will overload the default configurations
**Be careful all the key defined in the ini file should be declared in the project level Settings class**

```ini
[default]
; Support Environment variable 
API_ENV=$API_ENV 
COLLECTION_NAME = example
API_DEFAULT_LIMIT = 40
BUCKET_NAME=dev.io
MONGODB_URI=localhost:27017

[development]
;DB_NAME = develop_db
DEMO_COLLECTION = demo_collection

[test]
;DB_NAME = test_db
DEMO_COLLECTION = demo_collection
```

### 2.3  content of project level setting file **settings.py** 

```python
import os
from cocktail_apikit import DefaultSettings
class Settings(DefaultSettings):

    # specify configuration file names to load configuration from file
    # Be aware, any configuration fields in configuration file should be 
    # declare in the settings class  or any its super class, just 
    # to make us have better IDE auto-complete help
    _config_files = ['config/database.ini']

    # **REQUIRED: for Settings class can find the files in the _config_files attribute in any situation**
    BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
```


#### 2.4  content of a demo Schema in schema/demo.py

```python
from marshmallow import fields 
from cocktail_apikit import BaseSchema 

class DemoSchema(BaseSchema):
    """
    BaseSchema included some common fields: id, created_at, updated_at, deleted_at;
    Also contains some util method from SchemaMongoMixin for communicate with mongo db
    """
    name = fields.Str()

```

#### 2.5 content of a endpoint Resource in api/demo.py

```python
from settings import Settings
from bottle import request 
from schema.demo import DemoSchema

from cocktail_apikit import (
    ResourcePlugin,  route_mark,  ValidationError,  MongoDBManager,  enable_cors,
    BottleMongoQueryBuilder, Pagination, HTTP_DELETE_OK, HTTP_UPDATE_OK, HTTP_OK
)


demo_db = MongoDBManager(Settings.mongo_config_for_collection('demo')) # specify a Config option name or be the given name
demo_schema = DemoSchema()

class DemoResource(ResourcePlugin):

    # a simple demo endpoint
    @route_mark('/index')
    def index(self):
        return 'hello cocktail apikit'

    @route_mark('/demos')
    @enable_cors # allow cors for endpoint
    def list_demo(self):

        mongo_query_builder = BottleMongoQueryBuilder(request, demo_schema)
        mongo_query = mongo_query_builder.to_mongo_query()
        results, count = demo_db.filter(mongo_query)
        pagination = Pagination(mongo_query, results, count)
        return pagination.serialize(demo_schema)


    @route_mark('/demos', 'POST')
    def create_demo(self):
        payload = request.json
        cleaned_obj, errors = demo_schema.load(payload)
        if errors:
            raise ValidationError(errors)

        created_ids, errors = demo_db.create(cleaned_obj)

        if errors:
            raise ValidationError(errors)

        return {
            "ids": created_ids 
        }

    @route_mark('/demos/<demo_id>', 'DELETE')
    def soft_delete_demo(self, demo_id):
        delete_condition = {'_id':demo_id}

        result, errors = demo_db.delete(delete_condition)

        if errors:
            raise ValidationError(errors)

        if not result.raw_result['updatedExiting']:
            raise ValidationError({
                'msg': 'Object does not exist or already deleted!'
            })
        return {
            'msg':HTTP_DELETE_OK
        }


    @route_mark('/demos/<demo_id>', ['PUT','PATCH'])
    def update_demo(self, demo_id):
        payload = request.json
        condition = {'_id':demo_id}

        result, errors = demo_db.update(condition, payload)
        if errors:
            raise ValidationError(errors)
        if not result.raw_result['updatedExisting']:
            raise ValidationError({
                'msg': 'Does not found any thing to udpate'
            })
        return {'msg':HTTP_UPDATE_OK}
        
        
    @route_mark('/auth', auth=True) # Specify endpoint is authentication needed
    def auth_demo(self):
        return {'msg':HTTP_OK}

```

#### 2.6 content of main application.py

```python
from bottle import Bottle
from cocktail_apikit import FlexibleJsonPlugin, CorsPlugin, APP_ERROR_HANDLER
from api.demo import DemoResource

app  = Bottle()

# install FlexibleJsonPlugin to enable handle more data type
app.install(FlexibleJsonPlugin())

# install endpoint resource class`s instance
app.install(DemoResource())

app.install(CorsPlugin())

#config application object's error handlers
app.error_handler = APP_ERROR_HANDLER

if __name__ == "__main__":
    app.run(port=8000, debug=True, reloader=True)
```

#### 2.7  Then we can run 'python application.py', and access 

```http request
### Create a demo
POST http://localhost:8000/demos

{
  "name": "test1"
}


### list all demos
GET  http://localhost:8000/demos

### update a demo
PUT http://localhost:8000/demos/<demo_id>

### delete a demo
DELETE http://localhost:8000/demos/<demo_id>

```

### 3. Endpoint Authentication

If you want to create an endpoint with authentication need, you can follow the following example:

```python
from bottle import request
from cocktail_apikit import Authentication, ResourcePlugin, route_mark, HTTP_OK

class MyAuthentication(Authentication):
    def is_authenticated(self, *args, **kwargs):
        authentcation_data = request.headers.get('authorization')
        return authentcation_data == 'authorization'
    

class AuthDemoResource(ResourcePlugin):
    
    authentication = MyAuthentication()

    @route_mark('/auth', auth=True) #Default auth=False which means does not need authentication
    def auth_endpoint(self):
        return {'msg':HTTP_OK}
        
```

When you do request `http://localhost:80000/auth` without authorization data will raise Unauthorized error
When do request above with `Authorization=authorization` will return `{ "msg": "OK" }`
