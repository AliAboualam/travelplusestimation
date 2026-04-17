import os
import sys

import pandas as pd


def xlsx_to_csv(xlsx_path: str, output_dir: str | None = None) -> None:
    """
    Read every sheet in an Excel file and write one CSV per sheet.
    CSV files are saved next to the Excel file (or in output_dir if provided),
    named <sheet_name>.csv.
    """
    if not os.path.isfile(xlsx_path):
        print(f"Error: file not found: {xlsx_path}")
        sys.exit(1)

    if output_dir is None:
        output_dir = os.path.dirname(os.path.dirname(os.path.abspath(xlsx_path)))
        print("the ouput dir is ", output_dir)

    os.makedirs(output_dir, exist_ok=True)

    xl = pd.ExcelFile(xlsx_path)
    for sheet_name in xl.sheet_names:
        df = xl.parse(sheet_name)
        safe_name = sheet_name.replace("/", "-").replace("\\", "-")
        csv_path = os.path.join(output_dir, f"{safe_name}.csv")
        df.to_csv(csv_path, index=False, encoding="utf-8")
        print(f"Saved sheet '{sheet_name}' -> {csv_path}")


if __name__ == "__main__":
    # Always use the Tarifs prestataires.xlsx in the same folder as this script
    excel_file = os.path.join(os.path.dirname(__file__), "Tarifs prestataires.xlsx")
    output_dir = os.path.dirname(os.path.dirname(excel_file))
    xlsx_to_csv(excel_file, output_dir)
