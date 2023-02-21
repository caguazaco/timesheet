from datetime import date, datetime, timedelta

def billing_period(CUTOFF_DAY):
    today = date.today()

    if today.day >= CUTOFF_DAY:
        lower_date = datetime(today.year, today.month, CUTOFF_DAY)
    else:
        aux_date = today - timedelta(days = today.day)
        lower_date = datetime(aux_date.year, aux_date.month, CUTOFF_DAY)
    
    return [today, lower_date.date()]

def format_dates(data):
    for row in data:
        if hasattr(row, 'date'): row.date = row.date.strftime('%Y-%m-%d')
        if hasattr(row, 'start_time'): row.start_time = row.start_time.strftime('%H:%M')
        if hasattr(row, 'end_time'): row.end_time = row.end_time.strftime('%H:%M')
    
    return data