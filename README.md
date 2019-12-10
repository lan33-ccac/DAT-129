# DAT-129 Repository

### Purpose
This repository consists of Python scripts written to fulfill assignments in my DAT-129 Python 2 programming class at the Community College of Allegheny County (CCAC) in the Fall 2019 semester.

### 311_Final\_Project
Includes 3 programs to help analyze the 311 dataset, which is published by the Western Pennsylvania Regional Data Center (WPRDC):

* ***311.py:*** Uses Pandas to group and sort a large volume of 311 data so it can be more easily analyzed.
* ***preprocessor.py:*** Consolidates 311 Request Types into Categories defined by the 311 Department's Issue and Category Codebook.
* ***neighborhoods.py:*** Uses Pandas to count 311 requests by originating neighborhood in the city of Pittsburgh. 

### API
Includes the following program:

* ***pubmedAPI.py:*** Uses the Entrez API to search for ketamine-related publications in the Pubmed medical database and export the data to a .csv file.

### Crash\_Data
Includes two programs to help analyze data in the Pennsylvania Department of Transportation's crash dataset:

* ***pacrashes\_load.py:***  Loads the crash dataset (a .csv file) into a SQL Server Database via the Pandas package.
* ***pacrashes\_process.py:*** Uses Pandas to help answer several questions about the nature of accidents on Pennsylvania roads.

### DB_Interaction
Provides sample code to demostrate how Python can interact with databases for the purpose of peer teaching:

* ***dbdemo1.py:*** A very simple script that extracts the version number from SQLite.
* ***dbdemo2.py:*** Demonstrates the execution of different database operations (CREATE TABLE, INSERT, UPDATE, SELECT, and DELETE) using an SQLite database.
* ***connection_strings.py*** Provides sample connection strings for a variety of databases.

### DataEditor
Includes the following script:

* ***dataeditor.py:*** Allows a user to edit (modify, add to, delete from) a multi-level dictionary read in from a text schema file.  Demonstrates the use of recursion to handle unlimited dictionary levels.

### File IO
Includes class exercises in reading and writing data in various formats:

* ***IOnumbers.py:*** Formats a list of numbers and writes them out to a text file.
* ***IOnames.py:*** Builds a list of names from a text file and prints an appropriate greeting to the console.
* ***IOjail.py:*** Reads in an Allegheny County jail dataset from a .csv file and computes and displays statistics about it.
* ***IOjailpandas.py:*** Same as IOjail.py, but uses Pandas to generate the statistics.
* ***jsonexercises.py:*** Reads in a JSON file containing Pittsburgh capital project data into a list of dictionaries, prints info about the projects, and writes the data out to a file in JSON format.

### FileTree
Includes the following script for traversing a directory tree structure:

* ***filetree.py:*** Uses the os.walk method to traverse a directory structure, calculating statistics such as the maximum breadth and depth of a given file tree.  It uses Pandas to display statistics for all traversed trees.

### JSON Project
Includes two versions of a mini project that read in Pittsburgh capital project data from a .csv file, and allowed the data to be searched by various criteria.   Matching records could be written out to a file in JSON format:

* ***json_project_original:*** Written prior to the discussion of program specs in class.  Reads in the Capital Projects .csv file into a dictionary list.  Reads in empty selection criteria in a JSON file.  Allows a user to enter values for those selection criteria.  Displays matching records and writes them out to a file in JSON format. 
* ***json_project_inclass:*** An extension to work we did in class.  Reads search criteria from a file in JSON format.  Reads each row of the Capital Projects .csv file to determine if it matches the search criteria.  Prints matching records to the console.

### Webscraping
Includes the following script to demonstrate the use of the BeautifulSoup library to scrape data from a web site:

* ***clinicaltrials.py:*** Uses the BeautifulSoup library to extract data from the Federal Government's database of clinical trials and write it out to a .csv file. 

 


