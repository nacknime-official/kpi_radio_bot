import logging
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Union

import consts
from .broadcast import get_broadcast_path


def create_dirs(path: Union[str, Path]) -> None:
    dirname = os.path.dirname(path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)


def delete_file(path: Path) -> None:
    if not path.exists():
        return
    try:
        path.unlink()
    except Exception as ex:
        logging.warning(f"pls add exception {ex} in except")
        logging.error(f'delete file: {ex} {path}')


def move_to_archive(day=None) -> None:
    if not day:
        day = datetime.now().weekday()
    src = str(get_broadcast_path(day))  # заказы
    dst = str(consts.PATHS['archive'])  # архив

    if not os.path.exists(dst):
        os.makedirs(dst)

    for src_dir, _, files in os.walk(src):
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst, file_)
            try:
                shutil.move(src_file, dst_file)
            except Exception as ex:
                logging.error(f'move file: {ex} {src_file}')
                logging.warning(f"pls add exception {ex} in except")


async def download_audio(audio, path):
    create_dirs(path)
    await audio.download(path, timeout=60)
