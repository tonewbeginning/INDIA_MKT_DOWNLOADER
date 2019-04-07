import os
import zipfile
import requests
from pathlib import Path
from datetime import datetime, timedelta

import click

download_path = os.path.join(str(Path(__file__).resolve().parent), "downloads")
supported_exchanges = ["bse", "nse","nse_fo"]

def yesterday():
    """
    formats date in british format
    """
    yesterday = datetime.now() - timedelta(days=1)
    return str(yesterday.date().strftime("%d/%m/%Y"))

def download(download_url, file_path):
    """
    download function is used to fetch the data
    """
    print("Downloading file at", file_path)

    # Don't download file if we've done that already
    if not os.path.exists(file_path):
        file_to_save = open(file_path, "wb")
        with requests.get(download_url, verify=False, stream=True) as response:
            for chunk in response.iter_content(chunk_size=1024):
                file_to_save.write(chunk)
        print("Completed downloading file")
    else:
        print("We already have this file cached locally")

def download_and_unzip(download_url, file_path):
    """
    download_and_unzip takes care of both downloading and uncompressing
    """
    download(download_url, file_path)
    with zipfile.ZipFile(file_path, "r") as compressed_file:
        compressed_file.extractall(Path(file_path).parent)
    print("Completed un-compressing")

def download_nse_bhavcopy(for_date):
    """
    this function is used to download bhavcopy from NSE
    """
    for_date_parsed = datetime.strptime(for_date, "%d/%m/%Y")
    month = for_date_parsed.strftime("%b").upper()
    year = for_date_parsed.year
    day = "%02d" % for_date_parsed.day
    url = f"https://www.nseindia.com/content/historical/EQUITIES/{year}/{month}/cm{day}{month}{year}bhav.csv.zip"
    file_path = os.path.join(download_path, "nse", f"cm{day}{month}{year}bhav.csv.zip")
    try:
        download_and_unzip(url, file_path)
    except zipfile.BadZipFile:
        print(f"Skipping downloading data for {for_date}")
        return
    os.remove(file_path)

def download_bse_bhavcopy(for_date):
    """
    this function is used to download bhavcopy from BSE
    """
    for_date_parsed = datetime.strptime(for_date, "%d/%m/%Y")
    month = "%02d" % for_date_parsed.month
    day = "%02d" % for_date_parsed.day
    year = for_date_parsed.strftime("%y")
    file_name = f"EQ{day}{month}{year}_CSV.ZIP"
    url = f"http://www.bseindia.com/download/BhavCopy/Equity/{file_name}"
    file_path = os.path.join(download_path, "bse", file_name)
    try:
        download_and_unzip(url, file_path)
    except zipfile.BadZipFile:
        print(f"Skipping downloading data for {for_date}")
    os.remove(file_path)

def download_nse_fo_bhavcopy(for_date):
    """
    This function downloads Equities FO from NSE
    """
    for_date_parsed = datetime.strptime(for_date, "%d/%m/%Y")
    month = "%02d" % for_date_parsed.month
    day = "%02d" % for_date_parsed.day
    year = for_date_parsed.strftime("%y")
    file_name = f"fo{day}{month}{year}.zip"
    url = f"https://www.nseindia.com/archives/fo/bhav/{file_name}"
    file_path = os.path.join(download_path, "nse_fo", file_name)
    try:
        download_and_unzip(url, file_path)
    except zipfile.BadZipFile:
        print(f"Skipping downloading data for {for_date}")
    os.remove(file_path)
    

@click.command()
@click.argument(
    "exchange",
    default="nse_fo")
@click.option(
    "--for_date",
    default=yesterday(),
    help="Date for which to download bhavcopy DD/MM/YYYY format")
@click.option(
    "--for_past_days",
    default=1,
    help="Number of calendar days for which we need to fetch data {E.g. past 15 days from today}")
def main(exchange, for_date, for_past_days):
    """
    download_bhavcopy is utility that will download daily bhav copies
    from NSE and BSE

    Examples:
    python download_bhavcopy.py bse --for_date 06/12/2017

    python download_bhavcopy.py bse --for_past_days 15
    """
    click.echo(f"downloading bhavcopy {exchange}")

    # We need to fetch data for past X days
    if for_past_days != 1:
        for i in range(for_past_days):
            ts = datetime.now() - timedelta(days=i+1)
            ts = ts.strftime("%d/%m/%Y")
            if exchange == "nse":
                download_nse_bhavcopy(ts)
            elif exchange == "bse":
                download_bse_bhavcopy(ts)
            elif exchange =="nse_fo":
                download_nse_fo_bhavcopy(ts)
    else:
        if exchange == "nse":
            download_nse_bhavcopy(for_date)
        elif exchange =="bse":
            download_bse_bhavcopy(for_date)
        elif exchange =="nse_fo":
            download_nse_fo_bhavcopy(for_date)

if __name__ == "__main__":
    # Make sure we have downloads directory
    Path(download_path).mkdir(parents=True, exist_ok=True)

    # Make sure we also have other directories
    for current_exchange in supported_exchanges:
        Path(os.path.join(download_path, current_exchange)).mkdir(parents=True, exist_ok=True)

    main()