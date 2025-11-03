## Software New Member Challenge
This is my submission for the LSU Tiger Racing software team!

Contact: discord: ih11, email: isaacjhumphries@gmail.com, github: isaach1003

### Required Software
Below are the required software, as well as the versions of them used in the project.
Python (3.13), pandas (2.3.3), numpy (2.3.4)

### Purpose & Use
The purpose of this code is to take a csv file and turn it into a readable JSON output.
JSON output will consist of: each driver's best lap, best overall sector times and laps (can contain multiple names/lap numbers), number of laps analyzed, and number drivers


Before using the code, make sure your data has the following categories:
lap time, sector times, driver names, and lap numbers. 
For each of these, it is suggested you rename them to 'time', 'sectorn', 'driver', and 'lap_number' respectively, before calling the main function 'lap_time_analysis'.

Currently, the code reformats the floats for the JSON output, and makes them round to the 3rd place. If you wish to change rounding for all numbers, go to the ffmt function (responsible for formatting) and switch the default value for the parameter 'decimals'. Alternatively, you can change the rounding of just one value by passing your desired rounding to the function call.

To use the code as intended, make sure you have an 'in' and 'out' folder, and uncomment the bottom of the code, replacing 'in/data.csv' with your file, and 'out/out.json' with whatever you want your JSON file to be called.

The test cases are also available for download and use, but if you do not wish to use those it is necessary to comment out the code between the comments labeled "start of test files" and "end of test files".

