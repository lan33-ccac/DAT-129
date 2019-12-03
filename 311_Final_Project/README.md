# 311.py Program

### Purpose: 
Analyzes records in the Western PA Regional Data Center (WPRDC) 311 dataset. (<https://data.wprdc.org/dataset>).  This dataset contains service calls to the 311 system for the city of Pittsburgh from 2015-2019.  The program helps to provide insight into the nature of requests in the 311 dataset.  It helps to answer the following questions:

* Which types of requests represent the highest volumes of 311 requests?
* Which departments are assigned to the highest volumes of service requests?
* Which types of requests represent the highest volumes of OPEN requests?
* Which departments are assigned to the highest volumes of OPEN requests?
* How long on average have different types of requests remained OPEN?
* Which departments have the longest standing OPEN requests?
* Which types of requests represent the highest volumes of CLOSED requests?
* Which departments are assigned to the highest volumes of CLOSED requests?
* What is the ratio of open to closed requests for a given request type or department?  (This ratio might help identify requests that are relatively difficult to close.)
* Which types of requests represent the highest volumes of NEW requests?
* How long on average have different types of requests remained in the NEW status?
* Which departments have the longest standing NEW requests?


### Design:
Reads the 311 CSV file into a Pandas DataFrame, and manipulates it to display:

* Basic statistics gathered from the data
* A list of matching data
* A bar graph to represent the data

If desired, the program also writes the contents of the dataframe to an Excel or CSV file for further analysis.

#### Sample Output of 311.py

---
![SampleOutput1](Capture1.jpg)
![SampleOutput2](Capture2.jpg)
![SampleOutput3](Capture3.jpg)
---

Another sample program run:

---
![SampleOutput4](Capture4.jpg)
![SampleOutput5](Capture5.jpg)
![SampleOutput6](Capture6.jpg)
---

#### Initialization Parameters: 

The program prompts for the following initialization values from console input:
	
* Display request counts vs. elapsed days:  The program can either display counts of requests that match selection criteria or the number of elapsed days requests have either been in an OPEN or NEW status.
* Display info about all requests, OPEN requests, CLOSED requests, or NEW requests.  Note that in "elapsed days" mode, OPEN and NEW requests are the only available choices (i.e., ALL and CLOSED are not available.)
* Group the data by request type, department, or both.  Note that records will always be sorted by either request counts or elapsed days (in descending order).
* Enter the number of records to return.  Use 999 to return all records. 
<p>

#### Notes:
* The program was written in Python version 3.6, so it's not guaranteed to work under previous versions. 
* The program requires the Pandas library to be installed. 
* The 311 input csv file should be located in the same directory as the program file.  The output file, if selected, will be written to the same directory.
* The program will plot the results in a bar chart if the number of records selected is less than 30, the upper limit of what would be readable in a chart format.
* See the Analysis of 311 Open Requests.docx file for an analysis of the 311 data and its limitations.


## preprocessor.py Program
The preprocessor.py program is a supplemental program that translates request types into categories defined in the 311 codebook.  It helps to consolidate requests into a much smaller list of categories for the purpose of analysis.  The program uses a translation file called "Catagory\_Translation.csv" to map the request types into categories.  To use the program, run it before running 311.py, and use its output as the input file to this program.  

#### Initialization Parameters
The program reads in the following initialization values from console input.  Note that all files should be located in the program directory:

* The name of the 311 csv file.
* The name of the preprocessed output file (which can be used as the input file to the 311.py program)
* The name of the file to be used for deleted records (see Notes section)
* The name of the csv file containing the category translation records (see Notes section)

Sample initialization parameter values:

--- 
![SampleOutput7](Capture7.jpg)
---

#### Preprocessor Output File as Input to 311.py

The following screen shots show sample output from the 311.py program when it uses the output of the preprocessor.py program as its input file:

---
![SampleOutput9](Capture9.jpg)
![SampleOutput10](Capture10.jpg)
![SampleOutput11](Capture11.jpg) 
---

#### Notes:
* A sample Category\_Translation.csv file is provided with this program.  It can be customized as needed to map request types to categories.  However, it must have a "Category" and "Issue" column.  (The Issue column corresponds with the input file's REQUEST TYPE values.)  The contents of this file should be reviewed and modified as needed to ensure that request types are being mapped into the most accurate categories.  It does not matter whether the columns are sorted by Category or by Issue.  Sample Category\_Translation.csv file snippet:

---
![SampleOutput8](Capture8.jpg)

---

* The preprocessor program reads each row in the 311 input file, looking for a match between the input file's "REQUEST TYPE" value and the values contained in the "Category Translation" csv file (under the "Issue" column).  If it finds a match, the program substitutes the corresponding value for "Category" as the new "REQUEST TYPE" value.  If it doesn't find a match, the program uses the original REQUEST TYPE value.
* If the value of the Category column in the Category Translation csv file is blank or "Unknown", the program uses the original REQUEST TYPE value.
* If the value of the Category column contains "DELETE", the input file row is deleted and written out to the deletion log file.  The sample Category\_Translation.csv file used the "DELETE" keyword to delete records having REQUEST TYPE values containing the words, "DO NOT USE".
* The 311 "Issue and Category Codebook" csv file should not be used as the Category Translation file because it is outdated (2016) and is missing many request types.  It also had an "In database, but not on 311 Web Submission Form" category that was replaced in the sample category translation file with more meaningful categories. 
* Because the 311 input file is very large, the preprocessor program may take several minutes to run.

## neighborhoods.py Program
This is a supplemental program that calculates request counts by neighborhood.  This data can be used as input to the QGIS mapping software.  The following is sample output from the program:

---
![SampleOutput12](Capture12.jpg)
--- 


A sample output file is provided with this project.  This file, called "Neighborhood 311 Counts per Capita.csv", combines output of the neighborhoods.py program with neighborhood population data from the 2010 US Census.  This data can be imported into QGIS and joined to a Pittsburgh Neighborhoods layer, which is available as a WPRDC dataset (shapefile).  The join fields are "Neighborhood" (in the .csv file) and "hood" in the neighborhoods layer.  QGIS can then be used to show a choropleth of request counts per capita for each Pittsburgh neighborhood.
  