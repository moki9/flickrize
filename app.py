import requests
import feedparser

from flask import Flask, url_for, request, render_template, flash
from flask_bootstrap import Bootstrap

from forms import SearchForm
from settings import FLICKR_FEED

app = Flask(__name__)
app.secret_key='3248yhjkdhsuydgf4w834q3434t'
Bootstrap(app)

@app.route("/", methods=['GET', 'POST'])
def index():
	form = SearchForm()
	terms = None
	if request.method == 'POST':
		terms = form.search.data

	msg, photos = query_flickr(terms)
	if 'error' in msg:
		flash("Something went wrong and I don't know why.")

	return render_template('index.html', form=form, photos=photos,terms=terms)

def query_flickr(terms=None):
	payload = {'format':'atom', 'lang': 'en-us'}
	if terms:
		payload['tags'] = terms
	
	print "payload: %s" % payload

	feeds = requests.get(FLICKR_FEED, params=payload)

	if feeds.status_code == 200 and feeds.content is not None:
		ds = feedparser.parse(feeds.content)
		photoset = []
		for entry in ds['entries']:
			if 'staticflickr.com' in entry['links'][1]['href']:
				photo = { 'title' : entry['title'], 'url': entry['links'][1]['href'] }
				photoset.append(photo)
				
		return 'success', photoset
	else:
		'error', None

		
if __name__ == '__main__':
    app.run(debug=True, port=8001, host='192.168.5.100')
