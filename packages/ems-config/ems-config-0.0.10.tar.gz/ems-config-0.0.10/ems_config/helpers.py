from datetime import datetime
import pytz


def parse_dt_or_none(cfg_section, key, timezone=pytz.UTC, fmt="%Y-%m-%dT%H:%M:%SZ"):
    s = cfg_section.get(key, fallback=None)
    if s is None:
        return None
    d = datetime.strptime(s, fmt)
    if timezone:
        d = d.replace(tzinfo=pytz.UTC)
    return d


def parse_list_or_none(cfg_section, key, data_type=str, delimiter=','):
    s = cfg_section.get(key, None)
    if s is None:
        return None
    return [data_type(x.strip()) for x in s.split(delimiter) if x]
