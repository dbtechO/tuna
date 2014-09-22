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
import logging

from google.appengine.ext import db
from google.appengine.api import users

from lyrics import *
import json

VS_NUM = 1

class Tune(db.Model):
    idd = db.StringProperty(required=True)
    version = db.IntegerProperty(required=True)
    title = db.StringProperty(required=True)
    artist = db.StringProperty(required=True)
    scale = db.FloatProperty(required=True)
    popularity = db.IntegerProperty(required=True)


class SongHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        idd = self.request.get('id')
        url = 'http://www.songlyrics.com/'+idd+'/'


        tunes = Tune.all()
        tunes.filter("idd =", idd)
        result = tunes.get()
        if result == None:
            #generate new database entry
            result = Tune(
                idd = idd,
                version = VS_NUM,
                title = lyrics.getTitle(url),
                artist = lyrics.getArtist(url),
                scale = float(lyrics.arbitraryScale(url)),
                popularity = 1)
            if result.artist == "Error" or result.title == "Error":
                return self.handle_exception("Invalid ID", False)
            result.put()
            
        else:
            if result.version != VS_NUM:
                result.scale = float(lyrics.arbitraryScale(url))
                result.version = VS_NUM
            result.popularity = result.popularity+1
            result.put()

        #Could be optimized by grabbing html first.
        yamlresponse = {
            'id': result.idd,
            'title': result.title,
            'artist': result.artist, 
            'scale': result.scale,
            'popularity': result.popularity
        }
        self.response.out.write(json.dumps(yamlresponse))
        

    #in the case that no artist is found we return the standard error.
    def handle_exception(self, exception, debug):
        yamlresponse = {
            'id': 'error',
            'exception': str(exception)
        }
        self.response.out.write(json.dumps(yamlresponse))





