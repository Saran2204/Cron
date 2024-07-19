
from utils.cron_parser import extract_recurrence_interval

def convert_cron_to_iso8601(parsed_cron):
    """
    Converts a parsed cron expression to an ISO 8601 duration format.
    """
    minute = parsed_cron.get('minute', '*')
    hour = parsed_cron.get('hour', '*')
    day_of_month = parsed_cron.get('day_of_month', '*')
    month = parsed_cron.get('month', '*')

    def starts_with_star_slash(value):
        return isinstance(value, str) and value.startswith('*/')

    # Handle every N minutes
    if starts_with_star_slash(minute):
        interval = extract_recurrence_interval(minute)
        return f'PT{interval}M'

    # Handle every N hours
    if starts_with_star_slash(hour):
        interval = extract_recurrence_interval(hour)
        return f'PT{interval}H'

    # Handle every N days
    if starts_with_star_slash(day_of_month):
        interval = extract_recurrence_interval(day_of_month)
        return f'P{interval}D'

    # Handle every N months
    if starts_with_star_slash(month):
        interval = extract_recurrence_interval(month)
        return f'P{interval}M'

    # Special cases for specific cron expressions
    if minute == '*' and hour != '*' and day_of_month == '*' and month == '*':
        return f'PT{hour}H'  # Runs every day at a specific hour

    if hour == '*' and minute != '*' and day_of_month == '*' and month == '*':
        return f'PT{minute}M'  # Runs every day at a specific minute

    # Handle daily and other simple cases
    if minute == '*' and hour == '*' and day_of_month == '*' and month == '*':
        return 'P1D'  # Runs daily

    # Handle specific times (e.g., '05 9 * * *')
    if minute != '*' and hour != '*' and day_of_month == '*' and month == '*':
        return f'P1D'  # Runs daily at a specific time

    # Handle specific days (e.g., '00 9 2 * *' - every month on the 2nd day at 9 AM)
    if minute != '*' and hour != '*' and day_of_month != '*' and month == '*':
        return f'P1M'  # Runs monthly at a specific time and day

    # If none of the above cases are met, raise an exception
    raise ValueError(f"Unsupported cron expression for ISO 8601 duration: {minute} {hour} {day_of_month} {month}")
