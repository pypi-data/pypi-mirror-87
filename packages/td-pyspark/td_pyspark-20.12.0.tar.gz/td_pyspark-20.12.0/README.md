td_pyspark
==

[Treasure Data](https://treasuredata.com) extension for using [pyspark](https://spark.apache.org/docs/latest/api/python/index.html).

```sh
$ pip install td-pyspark
```

This document is only for internal developers, see also [README_public.md](README_public.md) for further usage.

# For Developers

Running pyspark with td_pyspark:

```bash
$ ${SPARK_HOME}/bin/spark-submit --master "local[4]"  --driver-class-path td-spark-assembly.jar  --properties-file=td-spark.conf --py-files td_pyspark.py your_app.py
```

## How To Publish td_pyspark 

### Prerequisites 

[Twine](https://pypi.org/project/twine/) is a secure utility to publish the python package. It's commonly used to publish Python package to PyPI.
First you need to install the package in advance.

```bash
$ pip install twine
```

Having the configuration file for PyPI credential may be useful.

```
$ cat << 'EOF' > ~/.pypirc 
[distutils]
index-servers =
  pypi
  pypitest

[pypi]
repository=https://upload.pypi.org/legacy/
username=<your_username>
password=<your_password>

[pypitest]
repository=https://test.pypi.org/legacy/
username=<your_username>

password=<your_password>
EOF
```

The credentials for TD account of [pypi.org](https://pypi.org/user/treasure_data/) and [test.pypi.org](https://test.pypi.org/user/treasure_data/) is stored in the [Box note](https://treasure-data.app.box.com/notes/560859904521).

### Build Package

Build the package in the raw source code and wheel format.

```
$ make package
```

For Spark 3.0.1, we need to change the project name to td_pyspark_ea and set SPARK_VERSION to 3.0.1:
```
$ PROJECT_NAME=td_pyspark_ea SPARK_VERSION=3.0.1 make package
```

If you need to force setting version, set VERSION env. For example:
```
$ VERSION=20.6.1 PROJECT_NAME=td_pyspark_ea SPARK_VERSION=3.0.1 make package
```

### Publish Package

Upload the package to the test repository first.

```
$ make clean upload-test
```

If you do not find anything wrong in the test repository (
https://test.pypi.org/project/td-pyspark/ or
https://test.pypi.org/project/td-pyspark-ea/), then it's time to publish the package.


```
$ make clean upload
```

- For Spark 2.4.x: https://pypi.org/project/td-pyspark/
- For Spark 3.0.1: https://pypi.org/project/td-pyspark-ea/


To upload td-pyspark for Spark 3.0.1, use the following commands:
```
$ PROJECT_NAME=td_pyspark_ea SPARK_VERSION=3.0.1 make upload-test
$ PROJECT_NAME=td_pyspark_ea SPARK_VERSION=3.0.1 make upload
```

## Customize API endpoints


Use `TDSparkContextBuilder` to specify different API endpoints (e.g., development API):
```python
import td_pyspark
from pyspark.sql import SparkSession

builder = SparkSession\
    .builder\
    .appName("td-pyspark-app")
    
td = td_pyspark.TDSparkContextBuilder(builder)\
    .apikey("XXXXXXXXXXXXXX")\
    .api_endpoint("api.treasuredata.com")\
    .build()

# Read the table data within -1d (yesterday) range as DataFrame
df = td.table("sample_datasets.www_access")\
    .within("-1d")\
    .df()
    
df.show()
```

## Build documentation

You need to install Sphinx and it's extensions for documentation as follows:

```sh
pip install td-pyspark[docs]
```

or install dependencies in the td_pyspark directory after clone the repository.

```sh
pip install -e .[docs]
```

After installation of dependent Python packages, you can build the document as:

```sh
make doc
```

This command will generate the document under `docs/_build/html` directory.
