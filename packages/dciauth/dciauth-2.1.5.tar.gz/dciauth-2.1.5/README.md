# python-dciauth

DCI authentication module used by dci-control-server and python-dciclient

This section shows example programs written in python that illustrate how to work with Signature Version 2 in DCI. The algorithm used by dciauth is identical to [Signature Version 4 in AWS](http://docs.aws.amazon.com/general/latest/gr/sigv4-signed-request-examples.html).


## Authentication example:

GET

```python
import requests

from dciauth.v2.headers import generate_headers

headers = generate_headers(
    {"endpoint": "/api/v1/jobs"},
    {"access_key": "remoteci/client_id", "secret_key": "secret"},
)
requests.get("http://api.distributed-ci.io/api/v1/jobs", headers=headers)
```

POST

```python
import requests

from dciauth.v2.headers import generate_headers

payload = {"name": "user 1"}
headers = generate_headers(
    {
        "method": "POST",
        "endpoint": "http://api.distributed-ci.io/api/v1/users",
        "payload": payload,
    },
    {"access_key": "remoteci/client_id", "secret_key": "secret"},
)
requests.post("http://api.distributed-ci.io/api/v1/users", headers=headers, json=payload)
```

## Validation example

```python
    from flask import request

    from dciauth.v2.headers import parse_headers
    from dciauth.v2.signature import is_valid

    valid, error_message = is_valid(
        {
            "method": request.method,
            "endpoint": request.path,
            "data": request.data,
            "params": request.args.to_dict(flat=True),
        },
        {"secret_key": "secret"},
        parse_headers(request.headers),
    )
    if not valid:
        raise Exception("Authentication failed: %s" % error_message)
```

## Using POSTMAN

If you are using POSTMAN to discover DCI API you can use the following parameters with the AWS Signature authorization header:

    GET https://api.distributed-ci.io/api/v1/identity
    AccessKey=<DCI_CLIENT_ID>
    SecretKey=<DCI_API_SECRET>
    AWS Region="BHS3"
    Service Name="api"

## License

Apache 2.0

## Author Information

Distributed-CI Team <distributed-ci@redhat.com>
