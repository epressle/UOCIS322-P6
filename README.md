# UOCIS322 - Project 6 - Ethan Pressley (epressle@uoregon.edu) #
Brevet time calculator with AJAX, MongoDB, and a RESTful API!

## Purpose ##
This project is intended to add an API to the brevet calculator that has been worked on since Project 4.  
By filling out the form in the consumer program, you can get a JSON formatted file and a CSV formatted file returned with the information you choose.
Otherwise, the project is the same as previous and functions identically.
## NOTES ##
An invalid value for the top K values (negative, alphabetical) will return empty. A value that is too high for the top K values will return all of the entries.  
If the type of output (JSON, CSV) is (somehow) incorrectly set, the API will default to JSON.  
If none of the radio buttons are selected for types of output (listAll, listOpen, listClose), the API will default to listing all.
