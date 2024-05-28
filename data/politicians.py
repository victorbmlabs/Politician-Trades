from typing import Optional
from fake_useragent import UserAgent
from typing import Optional, Union
from datetime import datetime
import requests
import logging
from type import Trade
from dotenv import load_dotenv
import functools
import os

load_dotenv()

# Ideas

# Data
# Record personal portfolio, what politician bought & what the share of purchase is of their total portfolio
# Update records

PROXY_PORTS = [8001, 8002, 8003]  # Oxylabs ports
OXYLABS_USERNAME = os.getenv("OXYLABS_USERNAME")
OXYLABS_PASSWORD = os.getenv("OXYLABS_PASSWORD")


class CapitolTrades:
    """A class for interacting with the API which supports https://capitoltrades.com."""

    def __init__(self):
        """init varz"""
        self.__url = "https://bff.capitoltrades.com"
        self.__ua = UserAgent()
        self.__session = requests.Session()
        self.__session.request = functools.partial(self.__session.request, timeout=5)
        self.__session.get("https://bff.capitoltrades.com/trades")
        self.__update_proxy()
        try:
            data = self.__get_data()
        except Exception as e:
            raise Exception("Error initializing: " + str(e))
        self.__politicians = self.__parse_data(data)

    def __update_proxy(self):
        port = PROXY_PORTS.pop()
        proxy = {
            "http": f"http://{OXYLABS_USERNAME}:{OXYLABS_PASSWORD}@ddc.oxylabs.io:{port}",
            "https": f"https://{OXYLABS_USERNAME}:{OXYLABS_PASSWORD}@ddc.oxylabs.io:{port}",
        }

        self.__session.proxies.update(proxy)

    @property
    def politicians(self) -> dict[str, str]:
        """Returns the map of politician ID to politician name of all known
        politicians on https://capitoltrades.com. Useful for debugging."""
        return self.__politicians

    def __get_headers(self) -> dict[str, any]:
        """Generates headers for the Capitol Trades API."""
        return {
            "User-Agent": self.__ua.random,
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "application/json",
            "Origin": "https://bff.capitoltrades.com",
            "DNT": "1",
            "Connection": "keep-alive",
            "Referer": "https://bff.capitoltrades.com/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Sec-GPC": "1",
            "Cache-Control": "max-age=0",
            "TE": "trailers",
        }

    def __get_data(self) -> Optional[dict]:
        """Gather data on all known politicians from https://capitoltrades.com"""
        logging.debug("Getting seed data")

        seed_data = []
        page = 1
        paginating = True
        while paginating:
            params = (
                ("page", page),
                # 100 is the max return size of the API.
                ("pageSize", 100),
            )
            r = self.__session.get(
                self.__url + "/politicians",
                headers=self.__get_headers(),
                params=params,
            )
            r.raise_for_status()

            response_json = r.json()
            data = response_json["data"]
            seed_data.extend(data)

            if (
                len(seed_data) >= response_json["meta"]["paging"]["totalItems"]
                or not data
            ):
                paginating = False
            else:
                page += 1

        return seed_data

    def __parse_data(self, data: dict) -> dict[str, str]:
        """Reformat the API data into a hash map we can use to search for politicians by name."""
        logging.debug("Parsing list of politicians")
        return {p["_politicianId"]: p["fullName"] for p in data}

    def get_politician_id(self, name: str) -> Optional[str]:
        """Search for the politician ID of the provided name."""
        for pid in self.__politicians.keys():
            if name.lower() == self.__politicians[pid].lower():
                return pid
            if name.lower() == self.__politicians[pid].split(",")[0].lower():
                return pid
        return None

    def get_all_politician_trades(
        self, id: Union[Trade, str], age_days: int = 365
    ) -> list[Trade]:
        """Get all trades of a politician either by a Trade or politcian id string"""
        params = {}
        all_trades = []

        params["politician"] = id._politicianId if isinstance(id, Trade) else id

        r = self.__session.get(
            self.__url + "/trades", params=params, headers=self.__get_headers()
        )
        r.raise_for_status()

        data = r.json()
        print(data)
        all_trades.extend(Trade.from_dict(tr) for tr in data["data"])

        return all_trades

    def trades(self, politician_id: str) -> list[dict]:
        """Returns all of the trades for the provided politician ids."""
        assert politician_id in self.__politicians.keys()

        all_trades = []
        page = 1
        paginating = True
        while paginating:
            params = (
                ("page", page),
                # 100 is the max return size of the API.
                ("pageSize", 100),
                ("txDate", "all"),
                ("politician", politician_id),
            )
            r = self.__session.get(
                self.__url + "/trades",
                headers=self.__get_headers(),
                params=params,
            )
            r.raise_for_status()

            response_json = r.json()
            data = response_json["data"]
            all_trades.extend(data)

            if (
                len(all_trades) >= response_json["meta"]["paging"]["totalItems"]
                or not data
            ):
                paginating = False
            else:
                page += 1

        return all_trades

    def latest_trades(
        self, before: datetime = None, after: datetime = None
    ) -> list[Trade]:
        """Get all latest trades by any poltician"""
        # ?page=X

        all_trades = []
        page = 1
        paginating = True

        while paginating:
            params = {"page": page}
            r = self.__session.get(
                self.__url + "/trades",
                headers=self.__get_headers(),
                params=params,
                timeout=5,
            )
            r.raise_for_status()
            data = r.json()

            all_trades.extend(Trade.from_dict(tr) for tr in data["data"])
            page += 1

            if page > 5:
                paginating = False
                break

        return all_trades
