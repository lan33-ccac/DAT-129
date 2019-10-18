# pubmedAPI.py Program

### Purpose
Extracts publication data from the Pubmed database using the Entrez API eutilities.  Specifically, it searches for publications with "ketamine" in their titles, a "depression" keyword, and publication dates between 2017 and 2019.  The program writes matching records to a CSV file.  This program is useful for building a ketamine research database because Pubmed includes records of publications that do not necessarily exist in other research databases such as Google Scholar, Microsoft Academic, and SCOPUS.

### Pubmed
Pubmed is a large database of medical-related publications.  It allows the user to enter search criteria and view information about matching publications.  

The following screen shot shows how search criteria is entered manually into Pubmed:

---
![ScreenCapture1](ScreenCapture1.jpg)
---
The following shows sample search results:

![ScreenCapture2](ScreenCapture2.jpg)

### Entrez eUtilities
Access to the PubMed database, and many other scientific databases is provided by an API called "Entrez."  The Entrez API includes 6 eUtilities, 3 of which were used by the pubmedAPI program:

1.**eSearch utility** takes a query string and returns a list of matching PMIDs (unique publication identifiers) in XML format.
<p>
2. **eSummary utility** takes a string containing PMIDs and extracts document summary (meta data) information for each PMID and returns it in XML format.
<p>
3. **eFetch utility** takes a string containing PMIDs and extracts document details from full publication data and returns it in XML format.

**Note:** An API key is only required if your program will issue more than 3 requests per second.  An API key can be obtained by registering your program via an email request.

### pubmedAPI.py Program Design
1. The program accepts some initialization parameters from the console, which are used to build URLs and to determine where to write the program output.
<p>
2. The program builds a URL and issues a request to extract PMIDs from the Pubmed database using the eSearch eUtility.  The url is built out of the following information (Note that different eUtilities take different combinations of parameters.):
<p>
	- The base URL of the API endpoint
	- The database (i.e., pubmed)
	- The name of the eUtility
	- The retstart parm, which indicates which number record should be returned first.  (This is useful when the program is run multiple times to collect additional records.)
	- The retmax parm, which indicates the max number of records that should be returned in a single request.
	- The retmode and rettype parms, which determine how the requested information is returned and formatted.
	- The query.  The best way to build the query is to enter search terms manually and then copy Pubmed's translation of the search terms into the program.  The following shows an example of a translated query:
	

![ScreenCapture3](ScreenCapture3.jpg)
	  
<p>
3. The program writes the XML response containing PMIDs out to a file.  It then parses out the PMIDs from the XML in this file using the xml.etree.ElementTree library.
<p>
4. The program builds a string of PMIDs and also builds a new URL which extracts publication summary data using the eSummary utility.  It writes the returned data to an XML file and then parses it to pull out the following data:
<p>
	- Publication Title
	- Journal Name
	- Publication Type (e.g., Journal Article)
	- Volume
	- Issue
	- Pages
	- DOI (a unique document identifier)
<p>
5. The program builds a new URL which extracts full data about publications via the eFetch utility.  The program writes the XML response to a file and parses it to pull out the following information:
<p>
	- Full list of author names
	- Full list of keywords assigned to the publication
<p>
6. The program combines the PMIDs, summary info, with the list of author names and keywords, and then it writes records out to a CSV file. The following is sample output:
<p>
---
![ScreenCapture5](ScreenCapture5.jpg)

 
 