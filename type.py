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


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class CompanyOfficer:
    max_age: Optional[int] = None
    name: Optional[str] = None
    age: Optional[int] = None
    title: Optional[str] = None
    year_born: Optional[int] = None
    fiscal_year: Optional[int] = None
    total_pay: Optional[float] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Stock:
    """Represents the entire stock's info object from Yahoo Finance API"""

    address1: str
    city: str
    state: str
    zip: str
    country: str
    phone: str
    website: str
    industry: str
    industryKey: str
    company_officers: list[CompanyOfficer]
    industryDisp: str
    sector: str
    sectorKey: str
    sectorDisp: str
    longBusinessSummary: str
    fullTimeEmployees: int
    audit_risk: int
    board_risk: int
    compensation_risk: int
    share_holder_rights_risk: int
    overall_risk: int
    governance_epoch_date: int
    compensation_as_of_epoch_date: int
    ir_website: str
    max_age: int
    price_hint: int
    previous_close: float
    open: float
    day_low: float
    day_high: float
    regular_market_previous_close: float
    regular_market_open: float
    regular_market_day_low: float
    regular_market_day_high: float
    dividend_rate: float
    dividend_yield: float
    ex_dividend_date: int
    payout_ratio: float
    five_year_avg_dividend_yield: float
    beta: float
    trailingPE: float
    forwardPE: float
    volume: int
    regular_market_volume: int
    average_volume: int
    bid: float
    ask: float
    bid_size: int
    ask_size: int
    market_cap: int
    fifty_two_week_low: float
    fifty_two_week_high: float
    price_to_sales_trailing_12_months: float
    fifty_day_average: float
    trailing_annual_dividend_rate: float
    trailing_annual_dividend_yield: float
    currency: str
    enterprise_value: int
    profit_margins: float
    float_shares: int
    shares_outstanding: int
    shares_short: int
    shares_short_prior_month: int
    shares_short_previous_month_date: int
    date_short_interest: int
    shares_percent_shares_out: float
    held_percent_insiders: float
    held_percent_institutions: float
    short_ratio: float
    implied_shares_outstanding: int
    book_value: float
    price_to_book: float
    last_fiscal_year_end: int
    next_fiscal_year_end: int
    most_recent_quarter: int
    earnings_quarterly_growth: float
    net_income_to_common: int
    trailing_eps: float
    forward_eps: float
    peg_ratio: float
    last_split_factor: str
    last_split_date: int
    enterprise_to_revenue: float
    enterprise_to_ebitda: float
    last_dividend_value: float
    last_dividend_date: int
    exchange: str
    quote_type: str
    symbol: str
    underlying_symbol: str
    short_name: str
    long_name: str
    first_trade_date_epoch_utc: int
    time_zone_full_name: str
    time_zone_short_name: str
    current_price: float
    target_high_price: float
    target_low_price: float
    target_mean_price: float
    target_median_price: float
    recommendation_mean: float
    recommendation_key: str
    number_of_analyst_opinions: int
    total_cash: int
    total_cash_per_share: float
    ebitda: int
    total_debt: int
    quick_ratio: float
    current_ratio: float
    total_revenue: int
    debt_to_equity: float
    revenue_per_share: float
    return_on_assets: float
    return_on_equity: float
    operating_cashflow: int
    earnings_growth: float
    revenue_growth: float
    gross_margins: float
    ebitda_margins: float
    operating_margins: float
    financial_currency: str
    trailing_peg_ratio: float
