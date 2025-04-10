# Data exporter for shopping24 (s24.com)

## Introduction

This is a very basic python script to export data from the shopping24 API into a JSON file.

## Getting started

### Set enviroment variables

The template `.env` file defines the enviroment variables that need to be set. Start by renaming it from `.template.env` to `.env` and insert your `APP_ID` and `APP_KEY`.

### Install packages

Next, make sure to install the packages required to run the app:

```
pip install -r requirements.txt
```

### Run the app

```
python main.py
```

You should now see the total amount of entries found, the amount of pages and a progess count.

## Specifing target data

Using `TYPE` you can define the data that should be fetched using the API. Accepted values are `products`, `categories`, `brands` and `shops`.