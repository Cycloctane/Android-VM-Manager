from mitmproxy.addonmanager import Loader

from db import sync_engine
from model import Base

class DatabaseInitializer:

    def load(self, addon_loader: Loader):
        with sync_engine.connect() as conn:
            Base.metadata.create_all(bind=conn)
