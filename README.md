# Introduction
### The project has the objective to identify a leads hotlist suitable for food delivery channel in the city of London.

The analysis is best showed in notebook uber_notebook.ipynb

> **a.** Database of London Restaurants -> connect to UK Food Agency api and read in json.\
**b.** Clarity on food delivery business model to define criteria for leads\
**c.** Filter out outlets that are already in food delivery app\
**d.** Build package *leads* so we can use same framework for future analysis


# Model

- A Linear Regression was trained in 10,000 data points based on 7 features.
- The features are:
>>>a.pick up location(lat and long)\
>>>b.drop off location(lat and long)\
>>>c.number of passengers\
>>>d.time and day of the week

The model is already trained and available in gcp and is being used to predict the taxi fare in api.
However it can be trained again with new data if necessary.

# Package

The class leads was created to benefit from reuse of code and modularity.
This way we can create many objects as we want - london, manchester, etc. and manipulate them in similar or different ways but still have the same properties.
For example, in london we might want to have a leads list based on closest distance to existing Uber eats restaurants
in Manchester we might want to focus on chains. 

The two approaches are possible without rewriting any code.

Important: 
  - matching restaurants is being done using latitude and longitude.
  - Only possible for UK. Data based on website UK Food Agency

# API

The API was build using FastAPI and pushed as a Docker container into Google Cloud Run. This way the api is available at:

https:// taxifareapi-v75w2fyqhq-ew.a.run.app/127.0.0.1:8000/predict
