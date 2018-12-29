# quick_search
A script that takes a query either from the clipboard or the command line, searches the user query on some websites, scrapes the links available and open a specified number of results.

This script can be activated from the command line by creating a .bat file using a python interpreter with the modules available in the requirement.txt file. 

Assuming a .bat file named "search" (example: search.bat), a simple search can be activated by (without quotes):
"search amazon oneplus 6t", "search bing programming basics", "search google how to travel", "search how to travel" (will use google), "search" (will search whatever is in the clipboard).

A prompt will then be shown to select the number of results to be opened. The search query on the search engine selected will always be opened.
