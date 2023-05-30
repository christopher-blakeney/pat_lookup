#!/usr/bin/env python3

import pandas as pd
from tabulate import tabulate
import argparse
from pathlib import Path


def main():
    MRN_LOOKUP_LIST = []
    UNIQUE_PAT = []
    path_to_excel = ""
    sheet_name = ""
    lookup_txt = ""

    # CLI
    parser = argparse.ArgumentParser(
        prog="pat_lookup",
        description="lookup patient MRN's from a spreadsheet. Update lookup.txt file before running this program.",
    )
    parser.add_argument("path", help="path to lookup.txt file")
    args = parser.parse_args()
    lookup_txt = Path(args.path)

    with open(lookup_txt, "r") as file:
        for line in file:
            line = line.strip()
            if len(line) > 0:
                try:
                    line = int(line)
                    MRN_LOOKUP_LIST.append(int(line))
                except:
                    if line[0:5] == "path_":
                        path_to_excel = line[14:]
                    elif line[0:5] == "sheet":
                        sheet_name = line[11:]

    excel = pd.read_excel(path_to_excel, sheet_name)
    pat = excel.loc[excel["mrn"].isin(MRN_LOOKUP_LIST)]
    templist = []
    for i in pat["mrn"]:
        templist.append(i)
    for i in MRN_LOOKUP_LIST:
        if i not in templist:
            UNIQUE_PAT.append(i)

    # display
    counter = 0
    print(tabulate(pat, headers="keys"))
    print("Unknown Patients:")
    if len(UNIQUE_PAT) > 0:
        for i in UNIQUE_PAT:
            counter += 1
            print(f"{counter}. {i}")
    else:
        UNIQUE_PAT.append("- All patients known")
        print(UNIQUE_PAT[0])


if __name__ == "__main__":
    main()
