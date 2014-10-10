import os, cherrypy
#from genshi.template import TemplateLoader

#loader = TemplateLoader(
#	os.path.join(os.path.dirname(__file__), 'templates'),
#	auto_reload=True
#)

class DemoService(object):
	
	exposed = True
	def POST(self, content=None):
#		tmpl = loader.load('index2.html')
#		return tmpl.generate(
#			output="Here is the output",
#			error=None
#		).render('html', doctype='html')
		return "ok post"
		
	def GET(self):
#		tmpl = loader.load('index2.html')
#		return tmpl.generate(
#			output=None,
#			error=None
#		).render('html', doctype='html')
		return "ok get"
		
if __name__ == '__main__':
	HOST_NAME = os.getenv('VCAP_APP_HOST', '127.0.0.1')
	PORT_NUMBER = int(os.getenv('VCAP_APP_PORT', '9999'))
	
	cherrypy.config.update({
		'server.socket_host': HOST_NAME,
		'server.socket_port': PORT_NUMBER,
	}) 
	conf = {
#		'/': {
#			'tools.sessions.on': True,
#			'tools.staticdir.root': os.path.abspath(os.getcwd())
#		},
		"/": {
			'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
			'tools.response_headers.on': True,
#			'tools.response_headers.headers': [('Content-Type', 'text/plain')],
			'tools.staticdir.root': os.path.abspath(os.getcwd())
		},
		'/static': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': './public'
		}
    }

	print("Listening on %s:%d" % (HOST_NAME, PORT_NUMBER))
	cherrypy.quickstart(DemoService(), "/", config=conf)
