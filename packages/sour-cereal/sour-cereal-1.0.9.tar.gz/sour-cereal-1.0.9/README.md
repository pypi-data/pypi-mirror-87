# sour-cereal

## About
An abstraction of connections to real data sources for extraction applications usage.  

It implements simple methods for extraction preparation, monitoring, execution and cleaning into a class, meant to be inherited.  

The goal of this project consists in creating a standardized API for communicating with data sources in applications written in Python.

## Installing 
You can simply install it using *pip* as follows:
```console
$ pip install sour-cereal
```

## Usage
```python
from sour_cereal import SourceConnection

class FooDataSource(SourceConnection):
    def get_status_of_extraction(self: 'FooDataSource', *args, **kwargs):
        return datetime.now()

    def check_availability_of_extraction(self: 'FooDataSource', status: datetime):
        return status.hour >= 7		# data is ready only after 7pm

    def execute_extraction(self: 'FooDataSource', *args, **kwargs):
		# Extract some data
        return ['file1', 'file2']
```

For more examples, please check the files inside the `sour_cereal/examples` folder.
