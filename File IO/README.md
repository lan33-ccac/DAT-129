# 311.py

### Purpose: 
Analyzes records in the Western PA Regional Data Center (WPRDC) 311 dataset. (<https://data.wprdc.org/dataset>).  This dataset contains service calls to the 311 hotline for the city of Pittsburgh from 2015-2019.  The program helps to answer the following questions:

* What types of requests tend to remain in an open status?  A non-new request might remain open because it is:
	* A low-priority request
	* Difficult or resource/intensive to resolve
	* Involve a lot of red tape to resolve (e.g., court action)
	* Shear volume of the type of request
<p>
* For each of the top types of open requests, what is the likely cause of the open status?

### Design:
Reads the 311 CSV file into a Pandas DataFrame, and manipulates it to display:

* Basic statistics gathered from the data
* A list of request types, the count of those types remaining in the 'Open' status, and the percentage of total open status records each type represents.
* A bar graph to represent the data

The program also writes the contents of the dataframe to an Excel file for further graphical analysis.

### Notes: 

* The program initialization values can be set to collect and analyze data for all requests, open requests, closed requests or new requests.  The number of records returned can also be customized to limit the amount of data shown.

* See the 311.doc file for an analysis of the 311 data.
