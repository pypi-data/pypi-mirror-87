# -*- coding: utf-8 -*-

import os
import shutil

from PIL import Image
from pdf2image import convert_from_path
from pixelmatch.contrib.PIL import pixelmatch


def compare_images(reference_path: str, candidate_path: str, diff_path: str) -> int:
    img_a = Image.open(reference_path)
    img_b = Image.open(candidate_path)
    img_diff = Image.new('RGB', img_a.size)

    diffs = pixelmatch(img_a, img_b, img_diff, includeAA=True)
    img_diff.save(diff_path)

    return diffs


def list_files(dir: str) -> list:
    return sorted([file for file in os.listdir(dir) if os.path.isfile(os.path.join(dir, file))])


def compare_exported_images(reference_path: str, candidate_path: str, diffs_path) -> dict:
    # List dirs contents
    references = list_files(reference_path)
    candidates = list_files(candidate_path)

    if os.path.exists(diffs_path):
        shutil.rmtree(diffs_path)
    os.makedirs(diffs_path)

    result = {
        'missing': sorted(list(set(references) - set(candidates))),
        'extra': sorted(list(set(candidates) - set(references))),
        'common': {key: None for key in sorted(list(set(candidates) & set(references)))}
    }

    # for each common page, make diffs
    for basename in result['common'].keys():
        result['common'][basename] = compare_images(
            reference_path + '/' + basename,
            candidate_path + '/' + basename,
            diffs_path + '/' + basename
        )

    return result


def export_pdf_to_images(pdf_path: str, output_folder: str) -> None:
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)

    tmp_paths = convert_from_path(
        pdf_path,
        dpi=100,
        fmt='jpeg',
        output_folder=output_folder,
        paths_only=True,
        use_pdftocairo=True
    )

    format = '/{:05d}.jpg'
    for idx, src_path in enumerate(tmp_paths, start=1):
        dst_path = output_folder + format.format(idx)
        shutil.move(src_path, dst_path)
