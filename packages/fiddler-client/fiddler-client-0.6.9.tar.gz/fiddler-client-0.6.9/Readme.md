Fiddler Client
=============

Python client for interacting with Fiddler. Provides a user-friendly interface to our REST API and enables event
publishing for use with our monitoring features.

Requirements
------------
Requires python >= python-3.6.3.

Installation
------------

    $ pip3 install fiddler-client


API Example Usage
-------------
For examples of interacting with our APIs, please check out the tutorial notebooks:

[Tutorial 01: Uploading Datasets and Models](https://gist.github.com/lukemerrick/bec58454502ec82984bfbded505cc78f)

[Tutorial 02: Controlling Fiddler from the Notebook](https://gist.github.com/lukemerrick/76a6e8ce383431c0c6f9ad076ca087bd)

[Tutorial 03: Advanced Model Uploading](https://gist.github.com/lukemerrick/6441c77b329d2b6cea7e0f6ddfe0eda5)

* [Tutorial 03b: Advanced Model Uploading Shown in Keras](https://gist.github.com/lukemerrick/475047c6b9a7960a2810e7b603c403af)


Event Publisher Example Usage
-------------
To use the Fiddler package to publish events for monitoring, please adapt the example below to fit your needs.


    import fiddler as fdl

    fiddler_publisher = fiddler.Fiddler(token, org, project, model)

    # Publish and event. An event is a dictionary of fields where fields correspond to
    # input and output schema of the model.
    fiddler_publisher.publish({
        "feature_a": 10.5,
        "feature_b": 3.2,
        "prediction": 0.72
    })
