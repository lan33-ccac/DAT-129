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
![Capture1](https://github.com/lan33-ccac/DAT-129/blob/master/FileTree/Capture1.JPG)
![Capture2](https://github.com/lan33-ccac/DAT-129/blob/master/FileTree/Capture2.JPG)
![Capture3](https://github.com/lan33-ccac/DAT-129/blob/master/FileTree/Capture3.JPG)
![Capture4](https://github.com/lan33-ccac/DAT-129/blob/master/FileTree/Capture4.JPG)
---

The following are Excel histograms and box plots based on the same data (exported from Pandas):

---
![Capture5](https://github.com/lan33-ccac/DAT-129/blob/master/FileTree/Capture5.JPG)
![Capture6](https://github.com/lan33-ccac/DAT-129/blob/master/FileTree/Capture6.JPG)
![Capture7](https://github.com/lan33-ccac/DAT-129/blob/master/FileTree/Capture7.JPG)
![Capture8](https://github.com/lan33-ccac/DAT-129/blob/master/FileTree/Capture8.JPG)
![Capture9](https://github.com/lan33-ccac/DAT-129/blob/master/FileTree/Capture9.JPG)
---
 