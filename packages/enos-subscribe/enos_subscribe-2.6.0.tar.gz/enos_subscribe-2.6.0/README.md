# Using EnOS Data Subscription SDK for Python

Table of Contents

* [Installation](#install)
    * [Prerequisites](#pre)
    * [Installing from Pip](#pip)
    * [Building From Source](#obtaining)
* [Feature List](#feature)
* [Sample Codes](#sample)
* [Related Information](#information)
* [Release Notes](#releasenotes)


EnOS Data Subscription Service improves the API calling efficiency of applications with active data push, which supports subscription to real-time asset data, offline asset data, asset alert data, and asset event data.

After configuring and starting data subscription jobs on the EnOS Management Console, you can use the Data Subscription SDK for Python to develop applications for consuming the subscribed data.


<a name="install"></a>

## Installation

<a name="pre"></a>

### Prerequisites

The Data Subscription SDK for Python supports Python 2.7, Python 3.4, and newer versions.


You can install the SDK from pip, or build from source.

<a name="pip"></a>

### Installing from pip

The latest version of EnOS Data Subscription SDK for Python is available in the Python Package Index (PyPi) and can be installed using:

```
pip install enos-subscribe
```

<a name="obtain"></a>

### Building From Source

1. Obtain the source code of Data Subscription SDK for Python.
   - From GitHub:
    ```
    git clone https://github.com/EnvisionIot/enos-subscription-service-sdk-python.git
    ```
   - From EnOS SDK Center. Click **SDK Center** from the left navigation of EnOS Console, and obtain the SDK source code by clicking the GitHub icon in the **Obtain** column.


2. From the directory where the source code is stored, run the following command:

   ```
   python setup.py install
   ```

The EnOS Data Subscription SDK for Python has the following dependency modules:
- six
- google.protobuf
- websocket_client


<a name="feature"></a>

## Feature List

EnOS Enterprise Data Platform supports subscribing to asset time series data and alert data and pushing the subscribed data to applications, thus improving the data query efficiency of applications.

The features supported by this SDK include:
- Consuming subscribed real-time asset data
- Consuming subscribed alert data
- Consuming subscribed offline asset data
- Consuming subscribed event data


<a name="sample"></a>

## Sample Codes

### Code Sample for Consuming Subscribed Real-time Data

```
from enos_subscribe import DataClient

if __name__ == '__main__':
    client = DataClient(host='sub-host', port='sub-port',
                        access_key='Your Access Key of this subscription',
                        access_secret='Your Access Secret of this subscription')

    client.subscribe(sub_id='Your subscription Id')

    for message in client:
        print(message)
```

### Code Sample for Consuming Subscribed Alert Data

```
from enos_subscribe import AlertClient

if __name__ == '__main__':
    client = AlertClient(host='sub-host', port='sub-port',
                        access_key='Your Access Key of this subscription',
                        access_secret='Your Access Secret of this subscription')

    client.subscribe(sub_id='Your subscription Id')

    for message in client:
        print(message)
```

### Code Sample for Consuming Subscribed Advanced Alert Data

```
from enos_subscribe import AdvancedAlertClient

if __name__ == '__main__':
    client = AdvancedAlertClient(host='sub-host', port='sub-port',
                        access_key='Your Access Key of this subscription',
                        access_secret='Your Access Secret of this subscription')

    client.subscribe(sub_id='Your subscription Id')

    for message in client:
        print(message)
```


### Code Sample for Consuming Subscribed Offline Data

```
from enos_subscribe import OfflineClient

if __name__ == '__main__':
    client = OfflineClient(host='sub-host', port='sub-port',
                        access_key='Your Access Key of this subscription',
                        access_secret='Your Access Secret of this subscription')

    client.subscribe(sub_id='Your subscription Id')

    for message in client:
        print(message)
```

### Code Sample for Consuming Subscribed Event Data

```
from enos_subscribe import EventClient

if __name__ == '__main__':
    client = EventClient(host='sub-host', port='sub-port',
                        access_key='Your Access Key of this subscription',
                        access_secret='Your Access Secret of this subscription')

    client.subscribe(sub_id='Your subscription Id')

    for message in client:
        print(message)
```


<a name="information"></a>

## Related Information

To learn more about the Data Subscription feature of EnOS Enterprise Data Platform, see [Data Subscription Overview](https://support.envisioniot.com/docs/data-asset/en/latest/learn/data_subscription_overview.html).


<a name="releasenotes"></a>

## Release Notes

- 2020/03/03 (2.4.1): Initial release
- 2020/04/08 (2.5.0): Added the feature of event data subscription
- 2020/11/24 (2.6.0): Added the feature of advanced alert subscription 
