#!/usr/bin/env python3

from datetime import datetime, timedelta

def get_dates_range(start_year, start_month, start_day, end_year, end_month, end_day):
    """Get an inclusive range of dates."""
    end_date = datetime(end_year, end_month, end_day)
    start_date = datetime(start_year, start_month, start_day)

    date_range = [start_date + timedelta(days=n) for n in range((end_date - start_date).days + 1)]

    return date_range
