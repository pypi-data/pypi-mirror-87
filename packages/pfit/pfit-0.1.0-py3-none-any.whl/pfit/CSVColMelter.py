import argparse
import datetime
import numpy as np
import pandas as pd
import pathlib
import re
import textwrap

class CSVMelter():
    def __init__(self, areaTimezone = -7):
        self.areaTimezone = datetime.timezone(datetime.timedelta(hours=areaTimezone))

    @staticmethod
    def timezone_check(tz):
        tz = float(tz)
        if (tz < -15) or (tz > 14):
            raise argparse.ArgumentTypeError(f"Timezone value {tz} out of bounds!")
        return tz
        
    @staticmethod
    def pathExists(path):
        if pathlib.Path(path).exists():
            return path
        else:
            raise argparse.ArgumentTypeError(f"The path specified does not exist: {path}")

    def getISOFormat(self, date, time):
        if isinstance(date, str):
            # Case from CSV files where the date is string
            try:
                year, month, day = [int(dateVal) for dateVal in date.split("-")]
            except ValueError:
                raise ValueError(f"The date {date} was unable to be parsed. The format required is YYYY-MM-DD.")
        elif isinstance(date, datetime.datetime):
            # Case XLSX files - are "timestamp" objects
            year, month, day = date.year, date.month, date.day
        else:
            raise ValueError(f"The date {date} was unable to be parsed.")
            
        if isinstance(time, str):
            try:
                h, m, s = [int(timeVal) for timeVal in time.split(":")]
            except ValueError:
                raise ValueError(f"The time {time} was unable to be parsed. The format required is (H)H:MM:SS.")
        elif isinstance(time, datetime.time):
            h, m, s = int(time.hour), time.minute, time.second
        else:
            raise ValueError(f"The time {time} was unable to be parsed.")
        return datetime.datetime(year,month,day,hour=h,minute=m,second=s,tzinfo=self.areaTimezone).isoformat()
    
    def meltDataframe(self, df):
        originalCols = []
        meltCols = []
                    
        # Regex detect columns 
        for colName in df.columns:
            # if colName ends with '_m', it's depth
            if "_m" in colName:
                obj = re.search("^(?:(?!.*)|[+-]?((\d+\.?\d*)|(\.\d+)))(_m)$", colName)
                if obj is not None:
                    meltCols.append(colName)
                else:
                    raise ValueError(f"The column {colName} cannot be converted to a valid metre value. Ensure that all columns are free of errors.")

        tmp = set(meltCols)
        originalCols = [x for x in df.columns if x not in tmp]

        if len(meltCols) <= 0:
            raise ValueError("No depth columns found.")

        newColName = "depth"
        newValueName = "temperature"

        # Transpose of the columns occurs here
        melted_df = pd.melt(df, id_vars=originalCols, value_vars=meltCols, var_name=newColName, value_name=newValueName)
       
        # Convert depth values to floats and truncate the "_m"
        melted_df['depth'] = melted_df['depth'].apply(lambda val: float(val[:-2]))

        # Reorder the columns
        melted_df = melted_df[['project_name', 'site_id','latitude','longitude','time','depth','temperature']]
        
        return melted_df
    
    def parseTimeFormat(self, time):
        try:
            timeObj = datetime.datetime.strptime(str(time), "%Y-%m-%d %H:%M:%S")
        except ValueError as e:
            raise ValueError(f"The time {time} was unable to be interpreted in the YYYY-MM-DD HH:MM:SS format.")
        return timeObj.strftime("%Y-%m-%d"), timeObj.strftime("%H:%M:%S")
    
    def stringifyDepths(self, columns):
        depthVals = [name for name in columns if type(name) in (float, int)]
        depthDict = {}
        depths = []
        for name in depthVals:
            if not type(name) == str:
                # Check if you can change depth into int without losing info, otherwise keep as float, then append _m
                depthDict[name] = f"{str(int(name))}_m" if int(name) == name and isinstance(name, float) else f"{str(name)}_m"
                depths.append(f"{str(int(name))}_m" if int(name) == name and isinstance(name, float) else f"{str(name)}_m")
        return depthDict, depths
    
    def longToWide(self, df):
        depths = df.groupby(["time", "depth"])["temperature"].aggregate('mean').unstack()
        depths = depths.reset_index()
        wide = df[["project_name", "site_id", "latitude", "longitude"]].copy()
        wide = wide.join(depths, how="right")
        for col in ["project_name", "site_id", "latitude", "longitude"]:
            wide[col] = wide[col].mode()[0]
        wide["date_YYYY-MM-DD"], wide["time_HH:MM:SS"] = zip(*wide["time"].apply(self.parseTimeFormat))
        colOrder = ['project_name', 'site_id', 'latitude', 'longitude', 'date_YYYY-MM-DD', 'time_HH:MM:SS'] 
        depthDict, strDepths = self.stringifyDepths(wide.columns.tolist())
        wide.rename(columns=depthDict, inplace=True)
        colOrder.extend(strDepths)
        wide = wide[colOrder]
        return wide
    
    def meltFile(self, filename, outLoc = '.'):
        if pathlib.Path(filename).suffix == ".csv":
            try:
                df = pd.read_csv(filename, keep_default_na=False, float_precision="round_trip", parse_dates={"time": [4,5]}, date_parser=self.getISOFormat)
            except IndexError:
                raise IndexError("There are insufficient columns, the file format is invalid.")
        elif pathlib.Path(filename).suffix in [".xls", ".xlsx"]:
            try:
                df = pd.read_excel(filename, keep_default_na=False, parse_dates={"time": [4,5]}, date_parser=self.getISOFormat)
            except IndexError:
                raise IndexError("There are insufficient columns, the file format is invalid.") 
        else:
            raise TypeError("Unsupported file extension.")
            
        melted_df = self.meltDataframe(df)
        
        fs = f"melted_{pathlib.Path(filename).stem}.csv"
        if outLoc != '.' and outLoc is not None: 
            fs = pathlib.Path(outLoc, f"melted_{pathlib.Path(filename).stem}.csv")
        else:
            pass
        melted_df.to_csv(fs, encoding="utf-8", index=False)
        return 1
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''
        Converts CSV, XLS, or XLSX files in the NTGS-style "wide" format to CSV files in "long" format by creating a new column for depth.
        The file being transformed must be free of errors prior to running this.
        '''))
    parser.add_argument('location', metavar='path', type=CSVMelter.pathExists, help='Path to file')
    parser.add_argument('--output-path', metavar='output-path', type=CSVMelter.pathExists, help='Optional directory of the melted CSV file to write to')
    parser.add_argument('--timezone-offset', metavar='timezone-offset', type=CSVMelter.timezone_check, help='Optional value indicating timezone offset from UTC-0. If no value is given, timezone defaults to UTC-7. To represent half hour, use "-3.5" for Newfoundland time as an example.')
    arguments = vars(parser.parse_args())
    cm = None
    if arguments['timezone_offset'] is not None:
        cm = CSVMelter(arguments['timezone_offset'])
    else:
        cm = CSVMelter()
    cm.meltFile(arguments['location'], arguments['output_path'])
