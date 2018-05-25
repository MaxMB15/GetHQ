import urllib
import json

artist = "The Beatles"
songs = ["Love Me Do", "P. S. I Love You", "Please Please Me"]
query = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=%s"

google_hits = list()
for song in songs:
    results = urllib.urlopen(query % (artist + " " + song))
    json_res = json.loads(results.read())
    google_hits.append(int(json_res['responseData']['cursor']['estimatedResultCount']))

print google_hits