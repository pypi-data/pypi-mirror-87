import typing
from dataclasses import dataclass
from datetime import date, datetime, timedelta

from monitor_common.mongodb.status_entry import StatusEntry
from monitor_common.status import Status


@dataclass(frozen=True)
class HourSummary:
    date: date
    hour: int
    status: Status


@dataclass(frozen=True)
class DaySummary:
    date: date
    hourly_statuses: typing.Dict[int, Status]
    overall_status: Status


def _get_date(date_or_datetime: typing.Union[date, datetime]) -> date:
    if isinstance(date_or_datetime, datetime):
        return date_or_datetime.date()
    else:
        return date_or_datetime


def _start_of_day(day: typing.Union[date, datetime]) -> datetime:
    return datetime.combine(_get_date(day), datetime.min.time())


def hour_summary(day: typing.Union[date, datetime], hour: int) -> HourSummary:
    if not 0 <= hour < 24:
        raise ValueError("Hours must be between 0 and 23 inclusive.")

    start_of_hour = _start_of_day(day) + timedelta(hours=hour)
    end_of_hour = _start_of_day(day) + timedelta(hours=hour + 1)

    measurements = list(
        StatusEntry.objects(time__gte=start_of_hour, time__lt=end_of_hour)
    )

    if measurements:
        return HourSummary(
            date=_get_date(day),
            hour=hour,
            status=max(measurement.status for measurement in measurements),
        )
    else:
        return HourSummary(
            date=_get_date(day), hour=hour, status=Status(Status.UNKNOWN)
        )


def day_summary(day: typing.Union[date, datetime]) -> DaySummary:
    hourly_summaries: typing.List[HourSummary] = []

    for hour in range(0, 23):
        hourly_summaries.append(hour_summary(day, hour))

    hourly_statuses = dict(
        (summary.hour, summary.status) for summary in hourly_summaries
    )
    day_status = max(summary.status for summary in hourly_summaries)

    return DaySummary(
        date=_get_date(day), hourly_statuses=hourly_statuses, overall_status=day_status
    )
