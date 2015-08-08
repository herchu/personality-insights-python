# Watson Personality Insights demo application for Bluemix

import os, cherrypy, requests, json
from mako.template import Template
from mako.lookup import TemplateLookup
lookup = TemplateLookup(directories=['templates'])


## Helper function to flatten a hierarchy of traits returned by the
## Personality Insights service, to be displayed in a raw table
def flattenPortrait(tree):
	arr = []
	def f(t, level):
		if t is None:
			return None;
		if level>0 and (("children" not in t) or level!=2):
			arr.append({
				"id"   : t["id"],
				"title": ("children" in t),
				"value": "%d%%" % int(t["percentage"]*100) if "percentage" in t else "",
			})
		if "children" in t and t["id"]!='sbh':
			for elem in t["children"]:
				f(elem, level+1);
	f(tree, 0)
	return arr


## This class implements a wrapper on the Personality Insights service 
class PersonalityInsightsService:	
	url = None
	API_PROFILE = "/v2/profile"
	API_VISUALIZATION = "/v2/visualize"
	
	## Construct an instance. Fetches service parameters from VCAP_SERVICES
	## runtime variable for Bluemix, or it defaults to local URLs.
	def __init__(self, vcapServices):
		if vcapServices is None:
			print("No VCAP_SERVICES was given. Using defaults. Make sure you have a valid username/password!")
			self.url = "https://gateway.watsonplatform.net/personality-insights/api";
			self.user = "<username>";
			self.password = "<password>";
		else:
			print("VCAP_SERVICES object found:", vcapServices)
			services = json.loads(vcapServices)
			for svc in services:
				print "* Found service from VCAP_SERVICES: %s" % svc
			svcName = 'personality_insights'			
			if svcName in services:
				print("Personality Insights service found!")
				svc = services[svcName][0]['credentials']
				self.url = svc['url']
				self.user = svc['username']
				self.password = svc['password']
			else:
				print("ERROR: No Personality Insights service was bound to this app!")

	## Builds the content object to send to Personality Insights API from a 
	## single piece of text
	def _formatPOSTData(self, text):
		return {
			'contentItems' : [{ 
				'userid' : 'dummy',
				'id' : 'dummyUuid',
				'sourceid' : 'freetext',
				'contenttype' : 'text/plain',
				'language' : 'en',
				'content': text
				}]
		};

	## Calls the Personality Insights API to analyze a piece of text and obtain
	## Personality, Values and Needs traits.
	def requestPortrait(self, text):
		if self.url is None:
			raise Exception("No Personality Insights service is bound to this app")
		data = self._formatPOSTData(text)
		r = requests.post(self.url+self.API_PROFILE, 
			auth=(self.user, self.password),
			headers = {'content-type': 'application/json'},
			data=json.dumps(data)
		)
		print("Profile Request sent. Status code: %d, content-type: %s" % (r.status_code, r.headers['content-type']))
		if r.status_code!=200:
			try:
				error = json.loads(r.text)
			except:
				raise Exception("API error, http status code %d" % r.status_code)
			raise Exception("API error %s: %s" % (error['error_code'], error['user_message']))
		return json.loads(r.text)

	## Builds a visualization of a portrait object, calling the visualize
	## API in Personality Insights
	def requestVisualization(self, data):	
		if self.url is None:
			raise Exception("No Personality Insights service is bound to this app")
		r = requests.post(self.url+self.API_VISUALIZATION, 
			auth=(self.user, self.password),
			headers = {'content-type': 'application/json'},
			data=json.dumps(data)
		)
		print("Viz Request sent. Status code: %d, content-type: %s" % (r.status_code, r.headers['content-type']))
		if r.status_code==200:
			return r.text
		else:
			return "Error building visualization"
			

## REST service/app. Since we just have 1 GET and 1 POST URLs, there is not
## even need to look at paths in the request. 
## This class implements the handler API for cherrypy library.
class DemoService(object):
	exposed = True
		
	def __init__(self, service):
		self.service = service

	## GET handler, just shows the default page with sample text content
	def GET(self):
		return lookup.get_template("index.html").render(content="")

	## Receives text content posted in the UI, posts it to Personality Insights
	## and builds a table with the results and the visualization
	def POST(self, content=None):
		traits, error, viz = (None, None, None)
		try:
			# Request analysis from Personality Insights API
			portrait = self.service.requestPortrait(content)
			# Flatten the returned JSON tree into an array to display a table
			traits = flattenPortrait(portrait["tree"])
			# Get a visualiation in HTML to be embedded in the page
#			viz = self.service.requestVisualization(portrait)
		except Exception as e:
			error = str(e)
		# Render response
		tmpl = lookup.get_template("index.html")
		return tmpl.render(
			content=content,
			traits=traits,
			error=error
#			viz=viz
		)
		
		
if __name__ == '__main__':
	# Wrapper for Personality Insights service
	pi = PersonalityInsightsService(os.getenv('VCAP_SERVICES'))

	# Get host/port from the Bluemix environment, or default to local
	HOST_NAME = os.getenv('VCAP_APP_HOST', '127.0.0.1')
	PORT_NUMBER = int(os.getenv('VCAP_APP_PORT', '9999'))
	cherrypy.config.update({
		'server.socket_host': HOST_NAME,
		'server.socket_port': PORT_NUMBER,
	}) 

	# Configure 2 paths: "static" for all JS/CSS content, and everything
	# else in "/" handled by the DemoService
	conf = {
		"/": {
			'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
			'tools.response_headers.on': True,
			'tools.staticdir.root': os.path.abspath(os.getcwd())
		},
		'/static': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': './public'
		}
    }

	# Start the server
	print("Listening on %s:%d" % (HOST_NAME, PORT_NUMBER))
	cherrypy.quickstart(DemoService(pi), "/", config=conf)
