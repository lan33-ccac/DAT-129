# Data Editor

### Purpose:
Week 2 exercise on editing a dictionary entry with multiple levels (i.e., sub-dictionaries).  It allows the user to:

* View key/value pairs at different levels of the dictionary.
* Change the value of a selected key at the current level in the dictionary.
* Delete an existing key/value pair at the current level in the dictionary.
* Add a new key/value pair at the current level in the dictionary.

### Basic Design:

* Reads a dictionary schema from a text file (sample=publication_schema.txt) and ensures it is a valid dictionary.
* Prints some basic stats about the dictionary, including number of dictionaries it contains and the total number of keys.
* Displays the top-level dictionary key/value pairs and the user menu
* Accepts a command from the user
* Uses a recursive design to navigate up and down levels of the dictionary and perform editing actions at a given level
* Prevents users from deleting the last key/value pair in a dictionary/subdictionary (although the entire subdictionary can be deleted at a higher level).
* Allows the user to save changes to the schema in an output file.
* Anticipates user errors and provides feedback messages as necessary.

### Notes:

* It should be able to handle ANY number of dictionary levels due to it's recursive design.
* In addition to strings, ints, and floats, it will accept lists, tuples, and dictionaries as new or changed values.

### Limitations/Possible Future Enhancements:
* It does not handle lists of dictionaries in the input file.
* Statistics are limited. 
* Although lists and tuple values can be added/changed, the program does not unpack the values to allow individual elements to be changed.  A new list or tuple must be specified (in python code format, e.g., [0,1]).
* Error handling is minimal (although most user errors have been anticipated).
* The "Interact" recursive function could be written as a separate class.

### Credits:

* Spr 19 Student Judy's data editor code, for helping me clarify the program requirements
* Dan Nydick, "Programming God", for suggesting a recursive design and debugging help
* Joe S., for supplying an alternative schema for testing purposes 

