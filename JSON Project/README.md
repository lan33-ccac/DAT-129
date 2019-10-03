# JSON Mini Project

There are two different programs included:

1. "json_project original"
2. "json_project inclass"

### JSON Project Original
This was my attempt at writing the JSON assignment before I knew what the actual requirements of the program were.  The program:

* Reads Capital Projects records from a CSV file into a list of dictionaries
* Reads empty search criteria fields from a JSON-formatted file
* Logs malformed dictionary records.
* Displays a menu that allows a user to enter a search criterion.  (The user may enter additional search criteria to further narrow the results).
* Checks for matching records.
* Computes total management costs for matching records based on the budget amount field and a made-up schema defined in a JSON file called, "mgmt_costs.json".
* Prints matching records to the console.
* Gives the user the option to write matching records to a JSON file.

**Note:** "search_criteria.json" goes with this project 

### JSON Project Inclass
This is an extension of the JSON program we started writing in class.  This program:

* Reads filled-out selection criteria from a JSON-formatted file.
* Reads and processes each record in a CSV file containing Capital Projects data:
<p>
	* Checks the record to see if it passes an integrity test, and logs malformed project records.
	* Checks whether the record matches all search criteria from the JSON file.
	* Prints eligible records to the console.

**Note:** "search_criteria 2.json" goes with this project