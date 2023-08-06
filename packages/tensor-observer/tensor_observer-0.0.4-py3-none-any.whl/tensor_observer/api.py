from urllib.request import Request, urlopen
from time import time
import json
import sys

class TensorObserver():
    """A class which handles all API calls to a TensorObserver Server."""

    API = 'http://localhost:8080'

    def __init__(self, endpoint='http://localhost:8080'):
        """all api calls will be made to the defined endpoint"""
        self.API = endpoint

    def scalar(self, scalar, run, tag, step, wall_time=None):
        """performs a http post request to save a scalar value from the training process
        Args:
            * scalar: number that should be saved
            * run: run identifier
            * tag: tag of the scalar
            * step: step id
            * wall_time: if not specified, current time is taken
        """
        if wall_time is None:
            wall_time = time()

        if type(scalar) != float:
            print('TensorObserver: SCALAR needs to be of type <float>', file=sys.stderr)
            return
        if type(run) != str or run == '':
            print('TensorObserver: RUN needs to be of type <str> and not empty', file=sys.stderr)
            return
        if type(tag) != str or tag == '':
            print('TensorObserver: TAG needs to be of type <str> and not empty', file=sys.stderr)
            return
        if type(step) != int:
            print('TensorObserver: STEP needs to be of type <int>', file=sys.stderr)
            return
        if type(wall_time) != float:
            print('TensorObserver: WALL_TIME needs to be of type <float>', file=sys.stderr)
            return

        data = {
            'type': 'scalar',
            'scalar': scalar,
            'run': run,
            'tag': tag,
            'step': step,
            'wall_time': wall_time
        }

        self._post(data)

    def exception(self, err, run, wall_time=None):
        """performs a http post request to notify that an exception happend
        Args:
            * err: Exception message string
            * run: run identifier
            * wall_time: if not specified, current time is taken
        """
        if wall_time is None:
            wall_time = time()

        if type(err) != str or err == '':
            print('TensorObserver: err needs to be of type <str>', file=sys.stderr)
            return
        if type(run) != str or run == '':
            print('TensorObserver: RUN needs to be of type <str> and not empty', file=sys.stderr)
            return
        if type(wall_time) != float:
            print('TensorObserver: WALL_TIME needs to be of type <float>', file=sys.stderr)
            return

        data = {
            'type': 'exception',
            'exception': err,
            'run': run,
            'wall_time': wall_time
        }

        self._post(data)

    def end_signal(self, run, wall_time=None):
        """performs a http post request to notify that the run terminated
        Args:
            * run: run identifier
            * wall_time: if not specified, current time is taken
        """
        if wall_time is None:
            wall_time = time()

        if type(run) != str or run == '':
            print('TensorObserver: RUN needs to be of type <str> and not empty', file=sys.stderr)
            return
        if type(wall_time) != float:
            print('TensorObserver: WALL_TIME needs to be of type <float>', file=sys.stderr)
            return
        
        data = {
            'type': 'end_signal',
            'run': run,
            'wall_time': wall_time
        }

        self._post(data)

    def _post(self, data):
        try:
            request = Request(
                self.API,
                data=json.dumps(data).encode('utf8'),
                headers={'content-type': 'application/json'}
            )
            urlopen(request)
        except Exception as e:
            print('TensorObserver for API <%s>:' % self.API, e, file=sys.stderr)
            pass

if __name__ == '__main__':
    from time import sleep
    from random import random, randint

    api = TensorObserver()

    runs = ['a_cool_net', 'another_one', 'some_exp', 'nice']
    tags = ['accuracy', 'loss']
    exceptions = ['broke', 'smth went wrong', 'cool error dude!']

    for i in range(100):
        if random() < 0.5:
            api.scalar(
                random(),
                runs[randint(0,3)],
                tags[randint(0,1)],
                i,
                time()
            )
        else:
            api.exception(
                exceptions[randint(0,2)],
                runs[randint(0,3)],
                time()
            )
        sleep(1)
    
    api.end_signal(
        runs[randint(0,3)]
    )
