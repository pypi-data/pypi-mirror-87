# RowmaPy
[![Netlify Status](https://api.netlify.com/api/v1/badges/3de604a0-ad5f-4d29-abb2-37118c634482/deploy-status)](https://app.netlify.com/sites/condescending-murdock-e43f8e/deploys)

The Rowma SDK for Python.

## Usage

### Publish
```py
from rowmapy import Rowma
rowma = Rowma()
rowma.connect()

robot_uuid = 'xxxx-xxxx-xxxx'

rowma.publish(robot_uuid, '/chatter', { "data": "topic from python" })
```

### Subscribe
```py
from rowmapy import Rowma
rowma = Rowma()
rowma.connect()

robot_uuid = 'xxxx-xxxx-xxxx'
# Transfer /chatter topic in xxxx-xxxx-xxxx to this script
rowma.set_topic_route(robot_uuid, 'application', rowma.uuid, '/chatter')

def on_chatter(msg):
    print(msg)

rowma.subscribe('/chatter', on_chatter)
```

## Development
```
$ python setup.py sdist
$ pip install -U .
```

## Publish
```bash
rm -rf dist/*
python setup.py sdist
pip install wheel twine
twine upload dist/*
```
