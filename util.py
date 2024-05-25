from dateutil import tz, parser

timezone = tz.gettz("Europe/Amsteradm")


def parse_str_date(date):
    return parser.parse(date).replace(tzinfo=timezone)


def parse_iso_date(date):
    return parser.isoparse(date).replace(tzinfo=timezone)
