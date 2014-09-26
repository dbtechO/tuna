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

class TopHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'

        result = []
        tunes = Tune.all()
        tunes.order('-popularity')
        rank = 0
        for tune in tunes.run(limit=10):
        	rank+= 1
        	result.append({
        		'id': tune.idd,
	            'title': tune.title,
	            'artist': tune.artist, 
	            'rank': rank,
	            'popularity': tune.popularity
        		})

        self.response.out.write(json.dumps(result))
        

    #in the case that no artist is found we return the standard error.
    def handle_exception(self, exception, debug):
        yamlresponse = {
            'id': 'error',
            'exception': str(exception)
        }
        self.response.out.write(json.dumps(yamlresponse))





