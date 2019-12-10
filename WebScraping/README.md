# clinicaltrials.py Program

### Purpose:
This program used the BeautifulSoup library to webscrape the federal government's database of clinical trials (https://clinicaltrials.gov) and writes information out to a csv file.

### Program Design/Flow:

1. Initialization values can be set at runtime to control the search criteria that gets passed to the host.
<p>
2. A CSV output file is initialized with a header record.
<p>
3. A URL is built from initialization values.
<p>
4. A request is issued to the web host and the response page is stored.
<p>
5. The BeautifulSoup object is initialized with the stored page.
<p>
6. The BeautifulSoup object is traversed, looking for the following information:

	- Study Status
	- Study Number
	- Study Name
	- Condition(s) Studied
	- Intervention(s)
	- Study type
	- Current Study Phase
	- Location(s) of Study
<p>
7. Each study's record is written out to the CSV file.

### Sample Data from ClinicalTrials.gov Site

![Capture1](https://github.com/lan33-ccac/DAT-129/blob/master/WebScraping/ScreenCapture1.JPG)

### Sample CSV Output

![Capture2](https://github.com/lan33-ccac/DAT-129/blob/master/WebsScraping/ScreenCapture2.JPG)


 