import os
import csv
from copy import deepcopy

from .commons import run_requests, structure_sheets, structure_sheet
from ..services.services import Services


def convert_to_csv(
    input_path: str,
    services: Services,
    workers: int = 1,
    output_path: str = None,
    probability=False,
):
    # Get requests result
    result = run_requests(workers, input_path, services)
    processed_dir_name = os.path.normpath(output_path).split(os.path.sep)[-1]

    # Structure result
    sheets = structure_sheets(result)

    for sheet in sheets:
        write_csv(f"{processed_dir_name}_{sheet}.csv", structure_sheet(sheets[sheet]))


def write_csv(file_name, records):
    set_value(records)
    with open(file_name, mode="w") as f:
        writer = csv.DictWriter(
            f, fieldnames=records[0].keys(), extrasaction="ignore", delimiter=";",
        )
        writer.writeheader()
        for row in records:
            writer.writerow(row)


def set_value(records):
    for idx, row_items in enumerate(deepcopy(records)):
        for field, value in row_items.items():
            records[idx][field] = value[0]
