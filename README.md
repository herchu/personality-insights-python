# watson-usermodeling-python

[https://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/doc/systemuapi/index.html](IBM Watson User Modeling) sample Python application.

This is a sample application that uses the User Modeling service from [IBM Bluemix](http://bluemix.net).
It is just meant to describe how you can use Python to connect to the Watson services; not as a real world
application. Everyone is welcome to fork the repository or reuse this example code.

See this application running in http://um-pyton.mybluemix.net

## Notes

Note that Python is not officially supported in Bluemix at the time of writing this code.
However, virtually any language can be used if the right "buildpack" is provided to build the runtime;
and there are plenty of examples for different languages.  
Here is [http://thoughtsoncloud.com/2014/08/getting-started-python-ibm-bluemix/](a tutorial using Python buildpack), using the buildpack: https://github.com/cloudfoundry/cf-buildpack-python.git

## Deploying

To deploy this app (assuming you have a Bluemix account and the `cf` tool correctly set up, use the following command:
```
cf push um-python -m 128M -b https://github.com/cloudfoundry/cf-buildpack-python.git -c "python server.py"
```
If the app is deployed this way, one still needs to bind a User Modeling service -- this can be done in Bluemix UI.

For this app, I have used `cherrypy` as http server (static pages and basic REST api), and the `mako` framework for rendering via templates. I also used `requests` to communicate with the User Modeling API. These are listed in `requirements.txt` for the buildpack to install them when the app is pushed onto Bluemix.

## License

Copyright 2014 IBM Corporation

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


