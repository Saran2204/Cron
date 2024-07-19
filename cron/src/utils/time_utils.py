import pytz
from datetime import datetime
from dateutil import tz
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
   
def get_timezone(t_zone):
    timezone = tz.gettz(t_zone)
    time_now = datetime.now(timezone)
    year = time_now.year
    month = time_now.month
    day = time_now.day
    hour = time_now.hour
    minutes = time_now.minute
    
    date_time = datetime(year, month ,day, hour, minutes)
    
    return date_time

def convert_to_utc(time_str):
    local_time = datetime.fromisoformat(time_str)
    utc_time = local_time.astimezone(pytz.utc)
    return utc_time.isoformat()  
