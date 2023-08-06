# Simio
[![Build Status](https://travis-ci.com/RB387/Simio.svg?branch=main)](https://travis-ci.com/RB387/Simio)  

Small, simple and async python rest api web framework based on aiohttp.
Supports auto swagger generation and background workers. All you need to do is configure config!  

You can see example of application with simio [here](https://github.com/RB387/Simio-app-example).  
## Start with simio:
1. Install simio
    ```
    pip install simio
    ```
2. Start project
    ```
    mkdir my-project && cd my-project
    simio create-app
    >>> Your project name: myproj
    ```

# Tutorial:
Simio is very simple! Here is some examples:
## Run your application
All you need to run your application is:
* Get config
    ```python
    config = get_config()
    ```
* Create app builder
    ```python
    from simio.app.builder import AppBuilder
    builder = AppBuilder(config)
    ```
* Build and run app
    ```python
    app = builder.build_app(config)
    app.run()
    ```
## Handler
Just add `route` decorator to your handler inherited from BaseHandler
```python
import trafaret as t

from simio.handler.base import BaseHandler
from simio.handler.utils import route


RequestSchema = t.Dict({
    t.Key("some_number"): t.ToInt(gte=0)
})


@route(path="/v1/hello/{user_id}/")
class ExampleHandler(BaseHandler):
    async def post(self, example: RequestSchema, user_id: int):
        return self.response({"id": user_id, "some_number": example["some_number"],})

    async def get(self, user_id: int):
        return self.response(f"Your id is {user_id}!")

```

## Swagger
Just run your app and open:
```
0.0.0.0:8080/api/doc
```
![Example of swagger](https://raw.githubusercontent.com/RB387/Simio/main/git_images/swagger.png)
  
You can find raw json file in your project directory
Swagger generation can be disabled in config

## Worker
```python
async def ping_worker(sleep_time):
    print('Work')
    await asyncio.sleep(sleep_time)

def get_config():
    return {
        APP: {
            APP.name: "simio_app",
        },
        WORKERS: {
            ping_worker: {
                "sleep_time": 5
            }
        },
    }
```

## Clients
To register your client all you need to do is ...  
Ofc! Just add them to config
```python
def get_config():
    return {
        APP: {
            APP.name: "simio_app",
        },
        CLIENTS: {
            MongoClient: {
                "host": "mongodb://localhost:27017"
            }
        },
    }
```
They can be accessed in handler like this:
```python
from simio.handler.base import BaseHandler
from simio.handler.utils import route
from simio.app.config_names import CLIENTS

@route(path="/v1/hello_with_client/{user_id}/")
class HandlerWithClient(BaseHandler):
    @property
    def mongo_client(self):
        return self.app[CLIENTS][MongoClient]

    async def post(self, user_id: int):
        await self.mongo_client.db.coll.insert_one({"user": user_id})
        return self.response({"id": user_id})

```
And that's all!


!! This is 0.x version, so be ready for major updates in minor version !!