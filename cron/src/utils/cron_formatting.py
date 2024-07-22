from utils.cron_expression_parser import extract_recurrence_interval

def convert_cron_to_iso8601(parsed_cron):
    """
    Converts a parsed cron expression to an ISO 8601 duration format.

    Args:
        parsed_cron (dict): A dictionary containing the parsed cron expression components.

    Returns:
        str: The ISO 8601 duration string.

    Raises:
        ValueError: If the cron expression is unsupported or invalid.
        TypeError: If the input is not a dictionary or contains unexpected values.
    """
    def starts_with_star_slash(value):
        return isinstance(value, str) and value.startswith('*/')

    # Validate input type
    if not isinstance(parsed_cron, dict):
        raise TypeError('The input parsed_cron must be a dictionary.')

    # Extract cron components with default values
    minute = parsed_cron.get('minute', '*')
    hour = parsed_cron.get('hour', '*')
    day_of_month = parsed_cron.get('day_of_month', '*')
    month = parsed_cron.get('month', '*')

    # Lambda function to handle interval conversion
    interval_format = lambda value, unit: (
        f'PT{extract_recurrence_interval(value)}{unit}' 
        if starts_with_star_slash(value) 
        else None
    )

    # List of interval handlers
    interval_handlers = [
        (minute, 'M'),
        (hour, 'H'),
        (day_of_month, 'D'),
        (month, 'M')
    ]

    # Check intervals
    for value, unit in interval_handlers:
        try:
            result = interval_format(value, unit)
            if result:
                return result
        except ValueError as e:
            raise ValueError(f'Error processing cron interval for unit {unit}: {e}')

    # Lambda functions for cron patterns
    cron_patterns = [
        (lambda m, h, d, mo: 'PT1M' 
            if m == '*' and h == '*' and d == '*' and mo == '*' 
            else None,
         minute, hour, day_of_month, month),
        (lambda m, h, d, mo: f'PT{m}M' 
            if m != '*' and h == '*' and d == '*' and mo == '*' 
            else None,
         minute, hour, day_of_month, month),
        (lambda m, h, d, mo: f'PT{h}H' 
            if m == '*' and h != '*' and d == '*' and mo == '*' 
            else None,
         minute, hour, day_of_month, month),
        (lambda m, h, d, mo: 'P1D' 
            if m != '*' and h != '*' and d == '*' and mo == '*' 
            else None,
         minute, hour, day_of_month, month),
        (lambda m, h, d, mo: f'P{mo}M' 
            if m != '*' and h != '*' and d != '*' and mo != '*' 
            else None,
         minute, hour, day_of_month, month)
    ]

    # Check patterns
    for func, *args in cron_patterns:
        try:
            result = func(*args)
            if result:
                return result
        except Exception as e:
            raise ValueError(f'Error processing cron pattern: {e}')

    # If none of the above cases are met, raise an exception
    raise ValueError(
        f"Unsupported cron expression for ISO 8601 duration: "
        f"{minute} {hour} {day_of_month} {month}"
    )
