# watson-personality-insights-python

IBM Watson Personality Insights sample Python application.

Read more about Personality Insights here: https://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/doc/personality-insights/

See this application running in http://watson-personality-insights-python.mybluemix.net/

This is a sample application that uses the Personality Insights service from [IBM Bluemix](http://bluemix.net).
It is just meant to describe how you can use Python to connect to the Watson services; not as a real world
application. Everyone is welcome to fork the repository or reuse this example code.

*NOTE This is not an officially supported application from the Watson Services -- it just provided "as is" for developers to find example Python code working with Personality Insights and Bluemix.*

## Notes

Note that Python is not officially supported in Bluemix at the time of writing this code.
However, virtually any language can be used if the right "buildpack" is provided to build the runtime;
and there are plenty of examples for different languages.  
Here is [http://thoughtsoncloud.com/2014/08/getting-started-python-ibm-bluemix/](a tutorial using Python buildpack), using the buildpack: https://github.com/cloudfoundry/cf-buildpack-python.git


## Deploying to Bluemix

To deploy this app (assuming you have a Bluemix account and the `cf` tool correctly set up, use the following command:
```
cf push <application-name> -m 128M -b https://github.com/cloudfoundry/python-buildpack -s cflinuxfs2
```
If the app is deployed this way, one still needs to bind a Personality Insights service -- this can be done in Bluemix UI.

For this app, I have used `cherrypy` as http server (static pages and basic REST api), and the `mako` framework for rendering via templates. I also used `requests` to communicate with the Personality Insights API. These are listed in `requirements.txt` for the buildpack to install them when the app is pushed onto Bluemix.

## Running locally

To run this app locally, make sure you have a python environment and install required packages:
```
sudo pip install cherrypy mako
```
Also, replace the username/password in `server.py` (around lines 40/41) with an existing Personality Insights service credentials. Then run the server with `python server.py`.

## Gotchas / Troubleshooting

Note that Python is not officially supported in Bluemix. So this app, its runtime or buildpack combinatin may be become non functional at any time. Feel free to leave comments or create an issue or pull request in the repository if you find a problem or its solution. 
 
Some considerations:
 * Bluemix defaults as of today (July 2015) to a `lucid64` stack. This stack is no longer supported by the [CloudFoundry Python buildpack](https://developer.ibm.com/bluemix/2015/07/29/cloud-foundry-php-buildpack-doesnt-support-lucid64/). So you need to specify `-s cflinuxfs2` (for an Ubuntu 14.04 stack) in the `cf` deploy command. [Read more here](https://github.com/cloudfoundry/php-buildpack/issues/87).
* For more hints on the Python buildpack, see [this example](https://github.com/IBM-Bluemix/bluemix-python-flask-sample) (which uses Flask, but it serves as example if it continues to be maintained).
 * See `runtime.txt`. Currently python 2.7.9 seems to be the only functional version.

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


