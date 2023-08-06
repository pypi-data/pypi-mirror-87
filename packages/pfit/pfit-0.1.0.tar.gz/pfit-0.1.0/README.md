# Introduction
The Permafrost File Interoperability Toolkit (PFIT) is designed to promote interoperability and the adoption of standards for permafrost data files. This package currently supports the NTGS ground temperature standard. It includes tools to check and manipulate ground temperature data.

# File Data Checker
The `FileDataChecker` checks column names and values for CSV, XLS, and XLSX files. It logs issues with the files being read in if they do not conform to the NTGS standard.

The File Data Checker can be run by passing arguments through the command line, but it can also be imported for use as a module. 

### The following functions are available from the class:

`@static pathExists(path: str)` 

Checks for the existence of a path and raises an exception if it does not exist.

`@static createPathIfExists(path: str)` 

Creates a path if it does not exist and returns the path initially passed in otherwise.

`checkPath(pathLob: str, isVerbose: bool, logPath: str)`

- pathLoc - A string of a file path leading to the file to be checked. This can also be a zip file, which will be unzipped.
- isVerbose - A boolean value that determines if true, verbose logging to the console will also occur.
- logPath - A string of a file path that can either lead to a directory or a specific file for the log file to be created at. 

    _This parameter can be left as *None* or an empty string (although something must still be passed into the function)._

Sets logging level, creates passed file paths if non-existent, unzips files if in ZIP format and calls `checkFile`.

`checkFile(fileName: str)`

Opens file with _pandas_ and applies the error checks described below.

The following errors may be reported:

- Invalid Time - Time does not follow a valid time in the format HH:MM:SS.
- Invalid Date - Date values should be formatted as YYYY-MM-DD.
- Unexpected Column - One of the first 6 column names is not from the expected list of column names (or is not in the correct order). If this warning occurs, the columns must be resolved in the correct name and order first, otherwise no other checking is done. 
    - Expects data files to contain the first 6 columns with the exact following names:
        project_name, site_id, latitude, longitude, date_YYYY-MM-DD, time_HH:MM:SS
- Unexpected Metre - All following metre columns after the first 6 column names should be formatted as "<decimal>_m" only.
- No Measurements - No measurement columns are detected in the file.
- File Type - The file read in is not supported.
- Coordinate - A latitude or longitude value contains something that is not valid.
- Latitude - A latitude value is found that is not valid (Less than -90 or greater than 90).
- Longitude - A longitude value is found that is not valid (Less than -180 or greater than 180).
- Temperature - A temperature value is found that is not a valid temperature.


_XLS and XLSX files are **not recommended** as they can be problematic when parsing date/time values. Please consider saving data in CSV format._

_If you do decide to use XLS(X) files, ensure that the data is located in the first sheet as this is is the only sheet that is checked_.
 
# CSV Column Melter
The `CSVColMelter` accepts existing ground temperature data files that are in the **wide** format and converts it to the **long** CSV format through  transposition of depth columns. Files must conform to the NTGS-style ground temperature file format. This can be verified with the `FileDataChecker`.

The CSV Column Melter can be run by passing arguments through the command line, but it can also be imported for use as a module. 

### The following functions are available from the class:

`@static timezone_check(tz: str)`

Converts the timezone value to a float and checks if it is within reasonable range. Function for the command line argument parsing.

`@static pathExists(path: str)` 

Checks for the existence of a path and raises an exception if it does not exist.

`getISOFormat(date: str or datetime.datetime, time: str or datetime.time)`

Used in pandas value interpretation. Parses a date string as YYYY-MM-DD or datetime.datetime object and a time string as HH:MM:SS or a datetime.time object, returns a datetime.datetime object in ISO format.

`meltFile(filename: str, outLoc: str)`

Opens file for melting, outputs to specified output location (outLoc) when dataframe has been melted.

`meltDataFrame(df: pandas.DataFrame)`

Dataframe of read in file is manipulated from wide to long format.

# Conversion to NetCDF 
`NTGS_to_NetCDF` converts NTGS-style CSV files into NetCDF (`.nc`). Currently a work in progress.


