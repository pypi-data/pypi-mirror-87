[![CodeFactor](https://www.codefactor.io/repository/github/vwt-digital/gobits/badge)](https://www.codefactor.io/repository/github/vwt-digital/gobits)
# Description

Gobits is a very small module, which acts as a metadata carrier within an event-driven architecture on the Google Cloud Platform (GCP).
It automatically adds fields that may be useful downstream to determine the origin of a message.

# Usage

Class attributes:

```python
class Gobits:
    """
    A small class that gathers information (bits) for a pub/sub message payload.

    Attributes:
        _request                Holds information about the cloud function request.
        _context                Holds information about the cloud function context.
        envelope                The envelope containing a pub/sub message.
        message                 The pub/sub message to be processed.
        processed               Time of processing (UTC).
        gcp_project             The source GCP project.
        execution_id            The id of the execution.
        execution_type          Type of the service processing the message.
        execution_trigger_type  Type of the trigger invoking the processor.
        function_name           Name of the processing cloud function.
        function_version        Version of the processing cloud function.
        event_id                The id of the trigger event.
        message_id              The pub/sub message id.
        message_publish_time    Time of publishing to pub/sub (UTC).
        source_subscription     The originating pub/sub subscription.
    """
```

Cloud function with HTTP trigger:

```python
from gobits import Gobits


def handler(request):

    metadata = Gobits.from_request(request=request)

    message = {
      'gobits': [metadata.to_json()],
      'data': []
    }

```

Cloud function with other trigger:

```python
from gobits import Gobits


def handler(data, context):

    metadata = Gobits.from_context(context=context)

    message = {
      'gobits': [metadata.to_json()],
      'data': []
    }

```
