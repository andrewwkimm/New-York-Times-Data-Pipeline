# Table of Contents
1. [Introduction](README.md#introduction)
2. [Architecture Diagram](README.md#Architecture_Diagram)
3. [Prerequisites](README.md#prerequisites)
4. [Contact](README.md#contact)

# Introduction
**New York Times Dashboard**

I pass by the New York Public Library (NYPL) every work day by Bryant Park and always wondered in the back of my head how vast their collection of books is—I plan on diving deeper into just that. Using NYPL's publically available API, I will build a pipeline that extracts the data from it, load it into a database (BigQuery), transform it via dbt, then finally visualize it through Tableau. Tentatively, the visualization will answer how the growth of the total available books is over time as well as deeper granularities into which genre is the most popular.

# Architecture Diagram

![pipeline](image/)

1. Pull the data from the API using Python, then transforming it into tabular form
2. Connect to BigQuery and load the data into it
3. Create the data models in dbt
4. Visualize the data using Tableau
5. Schedule this process to repeat through Airflow

# Prerequisites

**Languages**
* Python 3.8
* pandas

**Technologies**
* Airflow
* dbt
* Tableau

**Database**
* BigQuery

# Contact

Feel free to get in touch about anything! [Andrew Kim](https://www.linkedin.com/in/andrew-sungsoo-kim/)
