import redis
import json

'''
Listen to Redis Channel
Returns whether meeting has ended
'''
def connect_to_redis():
    CHANNEL_TO_VOICE = "to-voice-conf-redis-channel"
    CHANNEL_TO_APPS = "to-akka-apps-redis-channel"
    CHANNEL_FROM_APPS = "from-akka-apps-redis-channel"
    r = redis.Redis(host='127.0.0.1', port=6379)
    pb = r.pubsub()
    pb.subscribe([CHANNEL_TO_VOICE, CHANNEL_TO_APPS, CHANNEL_FROM_APPS])

    return pb.listen()

# Wait for "MeetingDestroyedEvtMsg (=> Meeting has ended) then True"
def meeting_has_ended(internal_meeting_id):
    pb_listener = connect_to_redis()
    for msg in pb_listener:
        channel = msg['channel'].decode('utf-8')
        data = str(msg['data'])
        try:
            # Output from redis: b'{"key": "value", ...}'
            # Get rid of the b'string'
            data_cleaned = data[1:].replace("'", "")
            data_json = json.loads(data_cleaned)
            message_name = data_json['envelope']['name']
            if (channel == "from-akka-apps-redis-channel" and message_name == "MeetingDestroyedEvtMsg"):
                # meetingID only shown after specific messages
                meeting_id = data_json['core']['body']['meetingId'] 
                if (meeting_id == internal_meeting_id):  
                    print('Meeting_id: ' + meeting_id)
                    print('Meeting has ended')
                    return True
        except ValueError: # ...
            print('Redis listener: JSON Decoding failed')

if __name__ == '__main__':
    internal_meeting_id = '3aef88dc4fce517bdf94627abee6a2a056cda0cd-1603390857218'
    meeting_has_ended(internal_meeting_id)