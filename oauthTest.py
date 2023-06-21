import dropbox
from dropbox.exceptions import AuthError
from dropbox.oauth import DropboxOAuth2FlowNoRedirect
from getpass import getpass
import time
import json
from dotenv import load_dotenv
import os

def get_dropbox_client():
    load_dotenv()

    APP_KEY = os.getenv("APP_KEY")
    APP_SECRET = os.getenv("APP_SECRET")

    # Check if we have previously stored the access token
    try:
        token = json.load(open('.dropbox_token', 'r'))
    except:
        token = None

    if not token or token['expires_at'] <= time.time():
        # Get the access token from the user and save it
        auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET, token_access_type='legacy')

        if not token:
            authorize_url = auth_flow.start()
            print('1. Go to: ' + authorize_url)
            print('2. Click "Allow" (you might have to log in first)')
            print('3. Copy the authorization code.')

            auth_code = getpass('Enter the authorization code here: ').strip()

            try:
                oauth_result = auth_flow.finish(auth_code)
            except AuthError as e:
                print('Error: %s' % (e,))
                return None
            
            # Save refresh token for later use
            token = {
                'refresh_token': oauth_result.refresh_token,
                'expires_at': oauth_result.expires_at.timestamp()
            }
            print(oauth_result)
        else:
            return 0


        # Save the token for later
        with open('.dropbox_token', 'w') as f:
            json.dump(token, f)

    dbx = dropbox.Dropbox(token['refresh_token'])
    return dbx

# Now you can use your Dropbox client
dbx = get_dropbox_client()