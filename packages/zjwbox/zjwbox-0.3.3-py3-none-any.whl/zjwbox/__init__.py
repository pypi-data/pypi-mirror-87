from __future__ import absolute_import
from .zjwbox import Infer
from .auto_req import get_window_page, get_source_page, extra
from .comm_req import Comm_req
from .update import update_driver
from .store import Store
from .auto_sel import AutoSel
from .pre_deal import KnnMiss
from pyppeteer import chromium_downloader


name = "zjwbox"
version = "0.3.3"


pyppeteer_version_win32 = chromium_downloader.downloadURLs.get("win32")
pyppeteer_version_win64 = chromium_downloader.downloadURLs.get("win64")

