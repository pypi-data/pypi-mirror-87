import argparse
from pfit.CSVColMelter import CSVMelter
import datetime
import pandas as pd
import pathlib
from pfit.pfnet_standard import nc_ground_temperature
import textwrap

class NTGS_NetCDF_Converter():
    def __init__(self, timezoneOffset = -7):
        self.timezoneOffset = timezoneOffset

    @staticmethod
    def dirExists(path):
        if pathlib.Path(path).is_dir():
            return path
        else:
            raise argparse.ArgumentTypeError(f"The directory specified does not exist: {path}")

    def read_NTGS(self, ntgs_file):
        filename = pathlib.Path(ntgs_file)
        if filename.suffix == ".csv":
            df = pd.read_csv(ntgs_file, keep_default_na=False, float_precision="round_trip");
        elif filename.suffix in [".xls", ".xlsx"]:
            df = pd.read_excel(ntgs_file, keep_default_na=False);
        else:
            raise TypeError("Unsupported file extension.")
        
        melter = CSVMelter(self.timezoneOffset)
        return melter.meltDataframe(df)

    def NTGS_to_nc(self, ntgs_file, ncfile):
        melted_df = self.read_NTGS(ntgs_file)
        rootgroup = nc_ground_temperature(f"{ncfile}{pathlib.Path(ntgs_file).stem}.nc")
        
        rootgroup['']
        return melted_df, rootgroup

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''
        Converts CSV, XLS, or XLSX files in the NTGS-style "wide" format to NetCDF files.
        The file being transformed must be free of errors prior to running this.
        '''))
    parser.add_argument('location', metavar='path', type=CSVMelter.pathExists, help='Path to input dataset file')
    parser.add_argument('output-path', metavar='output-path', type=NTGS_NetCDF_Converter.dirExists, help='Directory where the NetCDF file will be written to')
    parser.add_argument('--timezone-offset', metavar='timezone-offset', type=CSVMelter.timezone_check, help='Optional value indicating timezone offset from UTC-0 (default: UTC-7). To represent half hour, use "-3.5" for Newfoundland time as an example.')
    arguments = vars(parser.parse_args())
    netcdf_converter = None
    if arguments['timezone_offset'] is not None:
        netcdf_converter = NTGS_NetCDF_Converter(arguments['timezone_offset'])
    else:
        netcdf_converter = NTGS_NetCDF_Converter()
    netcdf_converter.NTGS_to_nc(arguments['location'], arguments['output-path'])
