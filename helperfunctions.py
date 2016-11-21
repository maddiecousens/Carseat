

def state_to_timezone(state):
     """
     Takes in a state abbreviation, passes back a timzeone string.

     If state is an empty string, passes back 'US/Pacific'


     """
     state2timezone = {  'AK': 'US/Alaska',
                         'AL': 'US/Central',
                         'AR': 'US/Central',
                         'AS': 'US/Samoa',
                         'AZ': 'US/Mountain',
                         'CA': 'US/Pacific',
                         'CO': 'US/Mountain',
                         'CT': 'US/Eastern',
                         'DC': 'US/Eastern',
                         'DE': 'US/Eastern',
                         'FL': 'US/Eastern',
                         'GA': 'US/Eastern',
                         'GU': 'Pacific/Guam',
                         'HI': 'US/Hawaii',
                         'IA': 'US/Central',
                         'ID': 'US/Mountain',
                         'IL': 'US/Central',
                         'IN': 'US/Eastern',
                         'KS': 'US/Central',
                         'KY': 'US/Eastern',
                         'LA': 'US/Central',
                         'MA': 'US/Eastern',
                         'MD': 'US/Eastern',
                         'ME': 'US/Eastern',
                         'MI': 'US/Eastern',
                         'MN': 'US/Central',
                         'MO': 'US/Central',
                         'MP': 'Pacific/Guam',
                         'MS': 'US/Central',
                         'MT': 'US/Mountain',
                         'NC': 'US/Eastern',
                         'ND': 'US/Central',
                         'NE': 'US/Central',
                         'NH': 'US/Eastern',
                         'NJ': 'US/Eastern',
                         'NM': 'US/Mountain',
                         'NV': 'US/Pacific',
                         'NY': 'US/Eastern',
                         'OH': 'US/Eastern',
                         'OK': 'US/Central',
                         'OR': 'US/Pacific',
                         'PA': 'US/Eastern',
                         'PR': 'America/Puerto_Rico',
                         'RI': 'US/Eastern',
                         'SC': 'US/Eastern',
                         'SD': 'US/Central',
                         'TN': 'US/Central',
                         'TX': 'US/Central',
                         'UT': 'US/Mountain',
                         'VA': 'US/Eastern',
                         'VI': 'America/Virgin',
                         'VT': 'US/Eastern',
                         'WA': 'US/Pacific',
                         'WI': 'US/Central',
                         'WV': 'US/Eastern',
                         'WY': 'US/Mountain',
                          '' : 'US/Pacific',
                          '--': 'US/Pacific'}

     timezone = state2timezone.get(state)
      
     return timezone

def miles_to_degrees(miles):
    MILE_TO_DEGREE = 69.0
    return miles / MILE_TO_DEGREE







# def to_utc(state, start_time):
#     """Convert unaware time to UTC"""
#      # Convert time to datetime object without tz
#      start_time_notz = datetime.strptime(start_time, '%I:%M %p')
#      # Get timezone of ride's starting state
#      tz = state_to_timezone(state)
#      # Localize to timezone of state the ride is leaving from
#      start_time_aware = pytz.timezone(tz).localize(start_time_notz)
#      # Normalize to UTC in order to search DB
#      start_time_utc = pytz.utc.normalize(start_time_aware)
#      # Use time() method to create a time only object
#      return start_time_utc.time()

# def to_local(state, timestamp):
#      """Convert UTC to local time"""
#      # Use state from database to determine timezone
#      tz = state_to_timezone(state)
#      # Convert timestamp from db to be aware that it is in utc
#      utc = timestamp.replace(tzinfo=pytz.utc)
#      # Convert start_timestamp attribute to timezone of state
#      local = pytz.timezone(tz).normalize(utc)

#      return local

# def to_time_string(timestamp):
#      # If ride is today, adjust attribute to indicate
#      if timestamp.date() == date.today():
#           datetime = "Today, {}".format(timestamp.strftime('%-I:%M %p'))

#      # If ride is tomorrow, adjust attribute to indicate
#      elif timestamp.date() == (date.today() + timedelta(days=1):
#           datetime = "Tomorrow, {}".format(timestamp.strftime('%-I:%M %p'))
#      # Otherwise change attribute to formatted timestamp string
#      else:
#           datetime = timestamp.strftime('%A, %b %d, %Y %-I:%M %p')

#      return datetime










































