---
id: get-started
title: Get Started
sidebar_label: Get Started
---

## Prerequisites
You need Python >= 3.7. The [Anaconda Distribution](https://www.anaconda.com/) is a good choice.

## Install SOIL

```bash
pip install soil-sdk
```
Depending on your system settings you might need to run the above with root rights and replace pip by pip3, e.g.  _sudo pip3 install soil-sdk_

## Configure soil

```bash
soil configure
```
This will ask for your credentials. You will need a vpn key provided by the admins as well as an application id and an API key. Usually, one should leave the default URL provider. In case you enter some wrong input, run _soil configure --reset_ and reenter the required information again.

 You need to type in certain credentials provided by the admins. In particular the API key and app id.
  An example configuration file should look as follows:
 ```
 auth_api_key: ###################
auth_app_id: ###################
auth_url: https://auth.amalfianalytics.com
soil_url: https://soil.amalfianalytics.com/
```

## Start the VPN
First, one needs a vpn client. In Ubuntu one install it by
```
sudo apt install openvpn
```
Then one locally downloads a vpn key and a corresponding password provided by the admins and runs
```
sudo openvpn --config <local-path-to-vpn>
```

## Login to the platform

```bash
soil login
```

This will ask you your Amalfi credentials and store a token in the folder `$HOME/.soil`
Note that you always have to run login if you have made any changes in the steps above.

## Generate your first project

```bash
soil init your-project-name
```

This will generate a folder with the boilerplate elements and some example code.

![example-app](assets/example-app-dir.png)

## SOIL App Concepts

A SOIL Application has three main concepts:

* **[Scripts](../tutorial/scripts)**: these scripts won't run outside the SOIL platform and are the entry points to the application.
* **[Modules](../tutorial/modules)**: They run inside the SOIL platform and contain instructions to transform the data. They are decorated with `@modulify` and can be written or imported from the SOIL library.
* **[Data structures](../tutorial/data-structures)**: They contain the data, the metadata and instructions on how to serialize, deserialize and query it.

A SOIL application consists in a set of scripts that will upload or query some data, transform it and store it again.

To run a script you can do:
```bash
soil run example_script
```

## Running pipelines

A script will contain one or more pipelines that will look like this:
```python
import soil
from soil.modules.preprocessing.filters import row_filter
from soil.modules.simple_module import simple_mean

patients = soil.data('my_dataset')
women, = row_filter.RowFilter(patients, sex={'eql': '1'})
statistics, = simple_mean(women, aggregation_column='age')
print(statistics.data)
# { 'mean': 54 }
print(statistics.metadata)
```

Pipelines are lazily evaluated, this means that they are not ran until the data is needed. In the example the pipeline won't run until the line `print(statistics.data)`. This way the data transfer is minimized. The calls to a data structure that will trigger a pipleine run are `ds.data`, `ds.metadata` and `ds.get_data(**kwargs)`. The pipeline only runs with the first call to the data and it is blocking. This means that the line `print(statistics.data)` is blocking but `print(statistics.metadata)` is not.

Intermediate results are not stored, meaning that if we want to do for example `women.data` the partial pipeline will run even if we have computed the intermediate results before to get `statistics.data`.
