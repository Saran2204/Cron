def parse_day_of_week(day_of_week):
    """
    Converts a comma-separated list of day-of-week values from a cron expression
    into a list of day names.
    """
    days = {
        '0': 'Sunday',
        '1': 'Monday',
        '2': 'Tuesday',
        '3': 'Wednesday',
        '4': 'Thursday',
        '5': 'Friday',
        '6': 'Saturday',
        '7': 'Sunday'
    }
    
    return [days.get(day, day) for day in day_of_week.split(',')]


def is_valid_cron_part(value):
    """
    Checks if a cron part value is valid.
    """
    valid_parts = ['*', '*/', '*/', '-', ',']  # Include ranges and lists
    if value.isdigit():
        return True
    if any(val in value for val in valid_parts):
        # Simple validation for ranges and lists
        if any(char in value for char in ['-', ',']):
            parts = value.replace(',', ' ').replace('-', ' ').split()
            return all(part.isdigit() or part == '*' for part in parts)
        return True
    return False

def parse_cron_expression(expression):
    """
    Parses a cron expression into its components.
    """
    try:
        parts = expression.split()
        
        if len(parts) != 5:
            raise ValueError("Cron expression must have exactly 5 parts")

        minute, hour, day_of_month, month, day_of_week = parts

        # Validate individual parts
        if not all([
            is_valid_cron_part(minute),
            is_valid_cron_part(hour),
            is_valid_cron_part(day_of_month),
            is_valid_cron_part(month),
            is_valid_cron_part(day_of_week)
        ]):
            raise ValueError(f"Invalid cron expression parts: {parts}")

        return {
            'minute': minute,
            'hour': hour,
            'day_of_month': day_of_month,
            'month': month,
            'day_of_week': parse_day_of_week(day_of_week),
        }
    except ValueError as ve:
        raise ValueError(f"Invalid cron expression: {ve}")
    except Exception as e:
        raise ValueError(f"Error parsing cron expression: {e}")


def extract_recurrence_interval(part):
    if '*/' in part:
        return int(part.split('*/')[1])
    return None
    