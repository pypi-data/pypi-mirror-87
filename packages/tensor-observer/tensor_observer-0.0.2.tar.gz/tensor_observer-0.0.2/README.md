# tensor-observer
Simple PHP Server to keep track of current machine learning trainings.

1. Install a little api library
```
    pip install tensor-observer
```

2. push the following files to your server and maintain the folder structure
* index.php
* php/*
* assets/*
* and create a "data" folder

2. create an object of the API
```python
from tensor-observer import TensorObserver

to_api = TensorObserver('http://localhost:8080')
```

4. push your scalars during training by
```python
to_api.scalar(self, scalar, run, tag, step, wall_time=None)
```
This method performs a http post request to save a scalar value from the training process.

Args:
* scalar: number that should be saved
* run: run identifier
* tag: tag of the scalar
* step: step id
* wall_time: if not specified, current time is taken

5. wrap your script in a try catch block to push exceptions
```python
to_api.exception(self, e, run, wall_time=None)
```

This method performs a http post request to notify that an exception happend.

Args:
* e: Exception object
* run: run identifier
* wall_time: if not specified, current time is taken

6. send a end signal at the end to mark a run as terminated
```python
to_api.end_signal(self, run, wall_time=None)
```

This method performs a http post request to notify that the run terminated

Args:
* run: run identifier
* wall_time: if not specified, current time is taken

7. have fun!