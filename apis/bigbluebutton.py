import hashlib
import urllib.parse

# Global Variables
S_KEY = 'zo76ubWZJiQtl63GjAJ7SG2Sq6Tlf8xZfncKTTjF0'
url = 'https://bbb.ngwork.de/bigbluebutton/api/'

def get_meetings():
    api_url = get_meetings_req_string()
    print(api_url)

def get_meetings_req_string():
    query_string = 'getMeetings'
    query_string_append = query_string + S_KEY
    checksum = sha1_hash(query_string_append)
    api_request_string = url+query_string+'?checksum='+checksum
    return api_request_string

# Verwendung für andere API Request, welche _ Leerzeichen in den Params haben
# TODO
def url_encode(query):
    return urllib.parse.quote(query)

def sha1_hash(string):
    encode_to_bytes = string.encode('utf-8')
    hash_object = hashlib.sha1(encode_to_bytes)
    hashed_string = hash_object.hexdigest()
    return hashed_string

def main():
    get_meetings()

if __name__ == '__main__':
    main()






