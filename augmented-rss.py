from flask import Flask, Response, abort
from feeds import feeds

app = Flask(__name__)


@app.route('/feed/<feedname>')
def feed(feedname):
    if feedname not in feeds:
        abort(404)

    return Response(feeds.get(feedname).augment().to_xml(encoding='utf-8'), mimetype='text/xml')


if __name__ == '__main__':
    app.run(debug=True)