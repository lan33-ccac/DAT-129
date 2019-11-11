# filetree.py

### Purpose:
Uses the os.walk function to traverse multiple tree structures while collecting the following statistics for each tree:

* The index number of the tree
* The name of the root node of the tree
* The maximum depth (number of levels) of the tree
* The maximum breadth of the tree, defined as the most number of nodes (directories and/or files) at any level of the tree
* The total number of files contained in the tree
* The total number of directories contained in the tree
* The total size (in Bytes) of all files in the tree

The program loads statistics for each tree into a Pandas dataframe, displays the dataframe and summary statistics about the data, and plots a bar chart and a box plot for each numerical column of data. 

### Sample Output:
The following is output from Pandas:

---
![SampleOutput1](Capture1.jpg)
![SampleOutput2](Capture2.jpg)
![SampleOutput3](Capture3.jpg)
![SampleOutput4](Capture4.jpg)

---

The following are Excel histograms and box plots based on the same data (exported from Pandas):

---
![SampleOutput5](Capture5.jpg)
![SampleOutput6](Capture6.jpg)
![SampleOutput7](Capture7.jpg)
![SampleOutput8](Capture8.jpg)
![SampleOutput9](Capture9.jpg)

---
 