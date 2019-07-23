from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.errors import HttpError
import slack

EXAMPLE_COMMAND = "session"

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'exampleKey.json'
VIEW_ID = 'VIEW_KEY'

def initialize_analyticsreporting():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE_LOCATION, SCOPES)
    analytics = build(
        'analytics', 
        'v4', 
        discoveryServiceUrl='https://analyticsreporting.googleapis.com/$discovery/rest?version=v4', 
        credentials=credentials)
    return analytics

def session():
    analytics = initialize_analyticsreporting()
    response = analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
          'metrics': [{'expression': 'ga:sessions'}]
        }]
      }
    ).execute()
    answer = response['reports'][0]['data']['totals'][0]['values'][0]
    #print(response)
    return answer

# @slack.RTMClient.run_on(event='open')
# def get_team_data(**payload):
#     team_domain = payload['data']['team']['domain']
#     #print(payload)

@slack.RTMClient.run_on(event='message')
def handler(**payload):
    data = payload['data']
    #print(data)
    if data['text'].startswith(EXAMPLE_COMMAND):
        channel_id = data['channel']
        user = data['user']
        #metric = EXAMPLE_COMMAND
        #print(metric)

        webclient = payload['web_client']
        webclient.chat_postMessage(
            channel=channel_id,
            text="Hi {}! Sessions: {}".format(user, session())
        )

if __name__ == '__main__':
    slack_token = "SLACK_TOKEN"
    rtmclient = slack.RTMClient(token=slack_token)
    rtmclient.start()