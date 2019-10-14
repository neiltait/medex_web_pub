# source this, don't run it! (subshell innit)
export API_URL='http://localhost:9000' #- this is the address for the Data API. (Defaults to 'http://localhost:9000')
export CMS_URL='http://localhost:12000' #- this is the domain the CMS is running on. (Defaults to 'http://localhost:12000')
export OP_DOMAIN='https://***REMOVED***.oktapreview.com' #- the domain name for the OKTA auth service used in this environment
export OP_ISSUER='/oauth2/default' #- the method and the auth service being used to authenticate (Defaults to '/oauth/default')
export OP_ID='***REMOVED***' #- the client ID provide by OKTA
export OP_SECRET='***REMOVED***' #- the client secret provided by OKTA
export REFRESH_PERIOD=600 #- the amount of time between retrieving a refresh token from OKTA (in seconds)
export LOGOUT_IF_IDLE_PERIOD=3600 #- the amount of time before a forced logout
export REQUIRE_HTTPS='False' #- set to False for local development
export LOCAL='True'

export SECRET_KEY='bananarama'
