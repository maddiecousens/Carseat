

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









































