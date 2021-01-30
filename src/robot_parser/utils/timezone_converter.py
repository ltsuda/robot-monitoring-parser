from datetime import datetime
import pytz


def datetime_to_utc(date, timezone="America/Sao_Paulo"):
    return datetime.timestamp(
        pytz.timezone(timezone)
        .localize(datetime.strptime(date, "%Y%m%d %H:%M:%S.%f"))
        .astimezone(pytz.utc)
    )
