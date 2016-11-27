from datetime import time

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

order_by_time = {time(0,0) : 65,
                    time(0,15) : 66,
                    time(0,30) : 67,
                    time(0,45) : 68,
                    time(1,0) : 69,
                    time(1,15) : 70,
                    time(1,30) : 71,
                    time(1,45) : 72,
                    time(2,0) : 73,
                    time(2,15) : 74,
                    time(2,30) : 75,
                    time(2,45) : 76,
                    time(3,0) : 77,
                    time(3,15) : 78,
                    time(3,30) : 79,
                    time(3,45) : 80,
                    time(4,0) : 81,
                    time(4,15) : 82,
                    time(4,30) : 83,
                    time(4,45) : 84,
                    time(5,0) : 85,
                    time(5,15) : 86,
                    time(5,30) : 87,
                    time(5,45) : 88,
                    time(6,0) : 89,
                    time(6,15) : 90,
                    time(6,30) : 91,
                    time(6,45) : 92,
                    time(7,0) : 93,
                    time(7,15) : 94,
                    time(7,30) : 95,
                    time(7,45) : 96,
                    time(8,0) : 1,
                    time(8,15) : 2,
                    time(8,30) : 3,
                    time(8,45) : 4,
                    time(9,0) : 5,
                    time(9,15) : 6,
                    time(9,30) : 7,
                    time(9,45) : 8,
                    time(10,0) : 9,
                    time(10,15) : 10,
                    time(10,30) : 11,
                    time(10,45) : 12,
                    time(11,0) : 13,
                    time(11,15) : 14,
                    time(11,30) : 15,
                    time(11,45) : 16,
                    time(12,0) : 17,
                    time(12,15) : 18,
                    time(12,30) : 19,
                    time(12,45) : 20,
                    time(13,0) : 21,
                    time(13,15) : 22,
                    time(13,30) : 23,
                    time(13,45) : 24,
                    time(14,0) : 25,
                    time(14,15) : 26,
                    time(14,30) : 27,
                    time(14,45) : 28,
                    time(15,0) : 29,
                    time(15,15) : 30,
                    time(15,30) : 31,
                    time(15,45) : 32,
                    time(16,0) : 33,
                    time(16,15) : 34,
                    time(16,30) : 35,
                    time(16,45) : 36,
                    time(17,0) : 37,
                    time(17,15) : 38,
                    time(17,30) : 39,
                    time(17,45) : 40,
                    time(18,0) : 41,
                    time(18,15) : 42,
                    time(18,30) : 43,
                    time(18,45) : 44,
                    time(19,0) : 45,
                    time(19,15) : 46,
                    time(19,30) : 47,
                    time(19,45) : 48,
                    time(20,0) : 49,
                    time(20,15) : 50,
                    time(20,30) : 51,
                    time(20,45) : 52,
                    time(21,0) : 53,
                    time(21,15) : 54,
                    time(21,30) : 55,
                    time(21,45) : 56,
                    time(22,0) : 57,
                    time(22,15) : 58,
                    time(22,30) : 59,
                    time(22,45) : 60,
                    time(23,0) : 61,
                    time(23,15) : 62,
                    time(23,30) : 63,
                    time(23,45) : 64}

def miles_to_degrees(miles):
    MILE_TO_DEGREE = 69.0
    return miles / MILE_TO_DEGREE









































