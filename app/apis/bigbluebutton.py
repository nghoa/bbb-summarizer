import hashlib
import urllib.parse
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup as Soup

# Global Variables
S_KEY = 'zo76ubWZJiQtl63GjAJ7SG2Sq6Tlf8xZfncKTTjF0'
# DOMAIN = 'https://bbb.ngwork.de/bigbluebutton/api/'
DOMAIN = 'http://34.107.7.184/bigbluebutton/api/'

def get_meetings():
    api_url = get_meetings_req_string()
    response = requests.get(api_url)
    xml_obj = Soup(response.content, 'xml')
    # Check for active meetings
    if (xml_obj.messageKey):
        print('No active Meetings')
    else:
        meetings = xml_obj.find_all({"meeting"})     # meetings[<xml>, <xml>, <xml>, ...]
        meetings_end = []
        for meeting in meetings:
            meeting = {
                "meeting_name": meeting.meetingName.get_text(),
                "meeting_id": meeting.meetingID.get_text(),
                "internal_meeting_id": meeting.internalMeetingID.get_text(),
                "voice_bridge": meeting.voiceBridge.get_text(),
                "moderator_pw": meeting.moderatorPW.get_text()
            }
            print('get_meetings from bbb.py', meeting)
            meetings_end.append(meeting)
        return meetings_end
        
'''
    TODO
        > add attendees to dictionary
        ------------- Structure -------------------
        attendee = {
            "user_id": userID,
            "full_name": fullName,
            "role": role,                   ## If role === MODERATOR -> isPresenter also true
        }
'''

def end_meeting(meeting_id, password):
    query = 'end'
    params = 'meetingID=' + url_encode(meeting_id) + '&password=' + url_encode(password)
    # to calc the "checksum" we need to concatenate => query + params + S_KEY
    checksum_string = query + params + S_KEY
    checksum = sha1_hash(checksum_string)
    api_request_string = DOMAIN + query + '?' + params + '&' +'checksum=' + checksum
    print('full request: ' + api_request_string)
    # Make API Call
    response = requests.get(api_request_string)
    xml_obj = Soup(response.content, 'xml')
    return_code = xml_obj.returncode.get_text()

    cases = {
        "SUCCESS": "Das Meeting konnte erfolgreich beendet werden!",
        "FAILED": "Das Meeting konnte nicht beendet werden"
    }

    # Check for correct return code
    print (cases.get(return_code))


'''
    for creating request_string():
        checksum = sha1_hash(query_string + append it with S_KEY)
        api_req_string = DOMAIN + query_string + ?checksum= + checksum
'''
def get_meetings_req_string():
    query_string = 'getMeetings'
    query_string_append = query_string + S_KEY
    checksum = sha1_hash(query_string_append)
    api_request_string = DOMAIN + query_string + '?' + 'checksum=' + checksum
    return api_request_string

# Verwendung für andere API Request, welche _ Leerzeichen in den Params haben
# TODO
def url_encode(query):
    return urllib.parse.quote_plus(query)

def sha1_hash(string):
    encode_to_bytes = string.encode('utf-8')
    hash_object = hashlib.sha1(encode_to_bytes)
    hashed_string = hash_object.hexdigest()
    return hashed_string

def main():
    pass
    # get_meetings()
    # end_meeting('random 192592!', 'mp')

if __name__ == '__main__':
    main()






