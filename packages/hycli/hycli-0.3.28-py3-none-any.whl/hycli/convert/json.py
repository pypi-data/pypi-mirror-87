import os
import json

from concurrent.futures import ThreadPoolExecutor, as_completed

import click

from ..services.requests import extract_invoice
from .commons import read_pdf, get_filenames


def convert_to_json(
    input_path, services, workers, output_path: str = None, skip: bool = False
):
    files = get_filenames(input_path, output_path, skip)
    skipped_files = []

    with ThreadPoolExecutor(max_workers=workers) as exe:
        jobs = {
            exe.submit(
                extract_invoice,
                read_pdf(file_path),
                services.extractor_endpoint,
                file_extension,
                services.get_token,
                services.headers,
            ): file_path
            for file_path, file_extension in files.items()
        }
        label = f"Converting {len(jobs)} invoices"
        with click.progressbar(jobs, label=label) as bar:
            for idx, future in enumerate(as_completed(jobs)):
                file_name = jobs[future].split("/")[-1]
                try:
                    response = future.result(timeout=300)

                except Exception as e:
                    skipped_files.append((file_name, e))
                    continue

                file_path = f"{file_name.split('.')[0]}.json"

                if output_path:
                    file_path = os.path.join(output_path, file_path)
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)

                with open(file_path, "w") as f:
                    json.dump(response, f)

                bar.update(1)

    return skipped_files
