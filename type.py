from datetime import datetime, date, timedelta
from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase
from enum import Enum
from typing import Union, Optional, Literal
from util import parse_str_date, parse_iso_date


class Chamber(Enum):
    HOUSE = "house"
    SENATE = "senate"


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Stats:
    count_issuers: int
    count_politicians: int
    count_trades: int
    date_first_traded: Union[str, datetime]
    date_last_traded: Union[str, datetime]
    volume: int


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Asset:
    asset_type: str
    asset_ticker: Optional[str]
    instrument: Optional[str]


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Issuer:
    _stateId: Optional[str]
    c2iq: str
    country: str
    issuer_name: Optional[str]
    issuer_ticker: Optional[str]
    sector: Optional[str]


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Politician:
    _stateId: str
    chamber: Union[str, Chamber]
    dob: date
    first_name: str
    last_name: str
    gender: str
    nickname: Optional[str]
    party: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class CommitteeMember:
    _politicianId: str
    member_role: str
    side: str
    chamber: str
    party: str
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    nickname: Optional[str] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Committee:
    _committeeId: str
    chamber: str
    committee_name: str
    committee_url: str
    members: list[CommitteeMember]
    stats: Stats
    meta: Optional[dict] = None

    def __post__init__(self):
        self.stats.date_first_traded = parse_str_date(self.stats.date_first_traded)
        self.stats.date_last_traded = parse_str_date(self.stats.date_last_traded)


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Trade:
    _txId: int
    _politicianId: str
    _assetId: int
    _issuerId: int
    pub_date: Union[str, datetime]
    filing_date: Union[str, datetime]
    tx_date: Union[str, datetime]
    tx_type: Literal["sell"]
    tx_type_extended: Optional[str]
    has_capital_gains: bool
    owner: str
    chamber: Union[str, Chamber]
    price: Optional[Union[str, float]]
    size: Optional[str]
    size_range_high: Optional[int]
    size_range_low: Optional[int]
    value: int
    filing_id: int
    filingURL: str
    reporting_gap: 27
    comment: Optional[str]
    committees: list[str]
    asset: Asset
    politician: Politician
    labels: list

    def __post_init__(self):
        c = self.chamber
        if c:
            self.chamber = Chamber(c)
            self.politician.chamber = Chamber(c)

        self.pub_date = parse_iso_date(self.pub_date)
        self.tx_date = parse_str_date(self.tx_date)
        self.filing_date = parse_str_date(self.filing_date)
        self.politician.dob = parse_str_date(self.politician.dob)

    @property
    def id(self):
        date = self.tx_date.strftime("%d%m%y")
        return f"{self._politicianId}-{date}-{self.asset.asset_ticker}-{self.tx_type.capitalize()}"

    def filing_trade_diff(self) -> timedelta:
        """Get the difference between trade- filing & order date in days"""
        return self.filing_date - self.tx_date

    def pub_trade_diff(self) -> timedelta:
        """Get the difference between trade- publication & order date in days"""
        return self.pub_date - self.tx_date
