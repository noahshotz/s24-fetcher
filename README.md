# Data exporter for shopping24 (s24.com)

## Introduction

A lightweight Python script to export data from the Shopping24 API into a JSONL (JSON Lines) file.

## Getting started

### Set enviroment variables

The template `.env` file contains the environment variables needed. Rename `.template.env` to `.env` and add your `APP_ID` and `APP_KEY` credentials.

### Install packages

Next, make sure to install the packages required to run the app:

```
pip install -r requirements.txt
```

### Run the app

```
python main.py
```

You'll see information about the total number of entries found, the number of pages, and a progress indicator.

## Configuration Options

### Target Data Type

Use the `TYPE` variable in the script to specify which data to fetch from the API. Supported values:
- `products`
- `categories`
- `brands`
- `shops`.

### Output Location

By default, data is exported to `data/products.jsonl`. You can change this by modifying the `output_file` parameter in the `fetch_all_products()` function call.