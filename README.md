# Introduction
### The project has the objective to identify a leads hotlist suitable for food delivery channel in the city of London.

The analysis is best showed in notebook uber_notebook.ipynb

> **a.** Database of London Restaurants -> connect to UK Food Agency api and read in json.\
**b.** Clarity on food delivery business model to define criteria for leads\
**c.** Filter out outlets that are already in food delivery app\
**d.** Build package *leads* so we can use same framework for future analysis


# Restaurants Leads List

- 1st decision was how to match Uber restaurant list and UK restaurant list. 
      a. Name : not a good option since the names are not exactly the same. It would require heavy string manipulation
      b. Location : latitude and longitude seems a good option because we do not have 'nas' in the dataframe. So this is our choice. 
      c. Address : not a good option. We are missing ~10% of addresses in UK list. And it would require a lot of string manipulation Linear Regression was trained in 
      
- 2nd decision is which criteria to prioritize in restaurant choice
     a. Uber revenue stream is directly proporcional to **volume** x **order ticket**. So we need to prioritize restaurants with high revenue.
     b. Only good and trustful restaurants are admitted in Uber Eats. We do not want any damage to the brand.
     
  In practice, with data we have:
     a. We do not have information on volume or order ticket. But we do have number of reviews and number of outlets. We will assume number of outlets is positively correlated with volume.
     c. We do have hygiene score. We will remove restaurants with score below 3. Meaning "urgent,major or some improvement is required"

  **In summary: we provide a list of restaurant chains with 4 or more outlets, with good hygiene standards and categories matching taste profile of Uber users.**

# Package - Scalable Solution

The class leads was created to benefit from reuse of code and modularity.
This way we can create many objects as we want - london, manchester, etc. and manipulate them in similar or different ways but still have the same properties.
For example, in london we might want to have a leads list based on closest distance to existing Uber eats restaurants
in Manchester we might want to focus on chains. 
The class is also buildable, meaning we could add as many methods as we want.

The two approaches are possible without rewriting any code.

Important: 
  - matching restaurants is being done using latitude and longitude.
  - Only possible for UK. Data based on website UK Food Agency

# Future and Next Steps

Data: get average meal ticket. Example: via TheFork - either scrapping or unnoficial api. statista, nielsen, restaurant.org. google
      

Package: add more methods on get_data in order to be able to retrieve information about restaurants in other countries.
