# Note to self: I needed to be in Python 3.9 for pandas to work and not have a ModuleNotFoundError that might be a me problem for now though

import pandas as pd
import zipfile

infotable_data = None

# ZipFile can take a filepath in its construction, can be a relative filepath, and a mode (r for reed, w for write)
with zipfile.ZipFile("test_data/01jun2026-31aug2026_form13f.zip", mode="r") as archive:
    # archive is the archive variable itself I think

    # In the archive, open an INFOTABLE.tsv (might potentially have the 13FS information in the actual data scrapper?)
    with archive.open("INFOTABLE.tsv") as infotable_file:
        # infotable_file as the file to examine
        # \t for the separator because when I looked at INFOTABLE.tsv the data seemed to be separated by tabs
        # dtype=str so everything including IDs will be strings for the time being (we can change it for some colummns later maybe)
        infotable_data = pd.read_csv(infotable_file, sep="\t", dtype=str)

if infotable_data is not None:
    # Work with infotable_data
    pass

else:
    print("infotable_data is either not found or has no data")

