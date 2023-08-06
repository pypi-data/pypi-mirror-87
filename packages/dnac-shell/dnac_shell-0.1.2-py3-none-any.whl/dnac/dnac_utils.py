import requests

# copyright (c) 2020 cisco Systems Inc., ALl righhts reseerved
# @author rks@cisco.com

def get_login_url():
	return  '/api/system/v1/identitymgmt/login'

#
def dnac_cookie_header(cookie):
	if cookie:
		return ({'X-auth-token': cookie})
	return None
#

def get_dnac_url(dnacip, url):
	return 'https://' + dnacip + url

#
def login_dnac(dnac_url, credentials):
	#with requests.Session() as session:
	print('login-dnac url = ' + dnac_url)
	print('cred = ' + str(credentials))
	return requests.get(dnac_url, auth=credentials, verify=False)

#
def call_dnac_with_session(dnac_url, session_cookie):
	#with requests.Session() as session:
	return requests.get(dnac_url, headers=dnac_cookie_header(session_cookie), verify=False)

#
def call_dnac(dnacip, url, credentials):
	sess_cookie = get_token(dnacip, credentials)
	return call_dnac_with_session( get_dnac_url(dnacip, url), session_cookie=sess_cookie)

#
def get_token(dnac_ip, credentials):
	login_url = get_dnac_url(dnac_ip, get_login_url())
	res = login_dnac( login_url, credentials)
	hdrs = res.headers
	xauth_cookie = None
	cookie_key = 'Set-Cookie'
	if cookie_key in hdrs.keys(): 
		cookies = hdrs[cookie_key]
		cookie=cookies.split(';')
		lst=cookie[0].split('=')
		xauth_cookie=lst[1]
	#
	return xauth_cookie

#
def get_floors(dnac_ip, credentials):
	return call_dnac(dnac_ip, '/api/v1/dna-maps-service/domains', credentials)
#

