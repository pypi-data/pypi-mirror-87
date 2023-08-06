"""
Google Spreadsheet を wget を使ってダウンロードする
"""

import datetime
import logging
import shutil
import subprocess
import sys
from pathlib import Path

# import logging

from . import config
from . import log

_logger = log.chandler(__name__, logging.INFO)


def make_url(key, gid, fmt):
    """
    Make spreadsheet URL for export

    Parameters
    ----------
    key : str
        spredsheet ID
    gid : int or None
        sheet ID
    fmt : str
        save format

    Returns
    -------
    str
        exported URL
    """
    _formats = ["xlsx", "ods", "pdf", "zip", "csv", "tsv"]
    if not fmt in _formats:
        _logger.error(f'"{fmt}" is a wrong format. Pick from {_formats}. ... Exit.')
        sys.exit()

    path = f"https://docs.google.com/spreadsheets/d/{key}/export"
    query = f"format={fmt}"
    if not str(gid) == "None":
        query += f"&gid={gid}"
    url = f"{path}?{query}"
    return url


def get_url(name):
    """
    Get spreadsheet URL for export with name

    Parameters
    ----------
    name : str
        name of spreadsheet

    Returns
    -------
    str
        spreadsheet URL for export
    """
    sheets = config.sheets()
    if not name in sheets:
        _logger.error(f'"{name}" is not in sheet list. Pick from {sheets}. ... Exit.')
        sys.exit()
    sheet = config.sheet(name)
    key = sheet.get("key")
    gid = sheet.get("gid")
    fmt = sheet.get("format")
    return make_url(key, gid, fmt)


def get_cmd(name, fname, by):
    """
    Get download command list

    Pass this list to subprocess

    Parameters
    ----------
    name : str
        name of spreadsheet
    fname : str
        download filename
    by : str
        wget or curl

    Returns
    -------
    list
        commands passed to subprocess
    """
    commands = ["wget", "curl"]
    if not by in commands:
        _logger.error(f'"{by}" is not in command list. Pick from {commands}. ... Exit.')
        sys.exit()

    url = get_url(name)
    options = config.options().get(by)
    if by == "wget":
        cmd = ["wget", options, "-O", fname, url]
    else:
        url = f'"{url}"'
        cmd = ["curl", options, "-o", fname, "-L", url]

    ## drop None value in cmd
    cmd = [str(c) for c in cmd if c]
    msg = (" ").join(cmd)
    _logger.debug(msg)
    return cmd


def download(name, stem="snapshot", snapd=".", by="wget"):
    """
    Download spreadsheet

    Parameters
    ----------
    name : str
        name of spreadsheet
    stem : str
        download filename
    by : str
        wget or curl

    Returns
    -------
    str
        downloaded filename
    """
    _logger.info(f"ダウンロードするよ : {name}")
    fmt = config.sheet(name).get("format")
    fname = Path(snapd) / f"{stem}.{fmt}"
    cmd = get_cmd(name, fname, by)
    subprocess.run(cmd)
    _logger.info(f"ダウンロードしたよ : {fname}")
    return fname


def backup(src, stem=None, snapd=".", datefmt="%Y%m%dT%H%M%S"):
    """
    Backup snapshot

    Parameters
    ----------
    src : str
        source file
    datefmt : str, optional
        dateformat, by default '%Y%m%dT%H%M%S'
    stem : str, optional
        backup filename, by default None
    snapd : str, optional
        backup directory, by default '.'

    Returns
    -------
    str
        backedup filename
    """
    src = Path(src)
    fmt = src.suffix
    ## stem を指定していない場合は、srcから取得
    if not stem:
        stem = src.stem
    dt = datetime.datetime.now().strftime(datefmt)
    fname = Path(snapd) / f"{dt}_{stem}{fmt}"
    _logger.info(f"移動するよ : {src.name}")
    # shutil.copy(src, dst)
    shutil.move(src, fname)
    _logger.info(f"移動したよ : {fname.name}")
    return fname


def snapshot(name, stem="snapshot", snapd=".", datefmt="%Y%m%dT%H%M%S", by="wget"):
    """
    Make snapshot (download & backup) of spreadsheet

    Parameters
    ----------
    name : str
        name of spreadsheet
    by : str
        wget or curl
    datefmt : str, optional
        dateformat, by default '%Y%m%dT%H%M%S'
    stem : str, optional
        download filename, by default 'snapshot'
    snapd : str, optional
        download directory, by default '.'

    Returns
    -------
    str
        download filename
    """
    fname = download(name, stem=stem, snapd=snapd, by=by)
    fname = backup(fname, stem=stem, snapd=snapd, datefmt=datefmt)
    return fname


def get(name, by):
    """
    Get snapshot

    返り値をスナップショットのファイル名にしてあるので、
    そのまま pandas などで読み込んで使うことができる。

    Parameters
    ----------
    name : str
        name of spreadsheet
    by : str
        wget or curl

    Returns
    -------
    str
        filename of snapshot
    """
    ## Config : volume
    v = config.volumes()
    snapd = v.get("snapd")
    ## Config : sheet
    s = config.sheet(name)
    stem = s.get("stem")
    datefmt = s.get("datefmt")
    fname = snapshot(name, stem=stem, snapd=snapd, datefmt=datefmt, by=by)
    return fname
