#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from lyrics import *
import json
class SearchHandler(webapp2.RequestHandler):
    def get(self):
    	self.response.headers['Content-Type'] = 'application/json'
    	query = self.request.get('query')
    	serResults = Lyrics.search(query)
        jsonresponse = {}
        clink = ""
    	for key in serResults:
            link = serResults[key]
            
            link = link.replace('http://www.songlyrics.com/', '')
            clink = link
            scale = 0#Lyrics.arbitraryScale(link)
            jsonresponse[key] = []
        self.response.out.write(clink)
        self.response.out.write(json.dumps(jsonresponse))     
    	'''obj = {
    		'query': query,
    		'scale': Lyrics.arbitraryScale(output), 
    		'payload':'some var', 
    	}
    	self.response.out.write(json.dumps(obj))
    	
    	self.response.write('Serves HTML [depricated]')
    	output = Lyrics.getLyrics('http://www.songlyrics.com/kanye-west/can-t-tell-me-nothing-lyrics/')
    	'''#self.response.write(str(Lyrics.arbitraryScale(output)))
