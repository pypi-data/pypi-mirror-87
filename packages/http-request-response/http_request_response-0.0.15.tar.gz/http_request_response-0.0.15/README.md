<h6 align="left">
    <img src="https://cdnquakingaspen.s3.eu-central-1.amazonaws.com/quaking+aspen+logo+teal+full-02.png"  />
</h6>

# http_request_response
[Introduction](#Introduction)\
[Getting Started](#Started)\
[Contributors](#Contributors)\
[License](#License)
<h2 id="Introduction">Introduction</h2>
The main target of this library is to standardize the request response in case of using flask-restplus library.
 
<h2 id="Started">Getting Started</h2>
In order to install, open the command prompt and type ✌️:

```
pip install http-request-response
```

In order to import:
```
from http_request_response import RequestUtilities
```
Mainly this library has two classes:
 
 - RequestResponse
 - RequestUtilities

The response when it is used is like the following:

*Response body*
```
{
  "status_code": ,
  "data": ,
  "message": ""
}
```
In order to use,  the endpoint-function should be decorated with try_except decorartors:
```
@cls.api.route('/')
class ItemPost(Resource):
    ##### Post
    @RequestUtilities.try_except
    def post(self):
        """ Create a new record  """
        return business_obj.create(request.body_args)
```
You have to make sure that the function returns two items:

 - The first one is an object of status code (refer to http_status_code library)
 - JSON serializable data

<h2 id="">Contributors</h2>

This project exists thanks to all the people who contribute. [[Contribute](CONTRIBUTING.md)].
<a href="https://github.com/Quakingaspen-codehub/http_request_response/graphs/contributors">
""
</a>

<h2 id="License">License</h2>

This library is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details.
