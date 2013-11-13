from flask import Flask, Response, abort
from feeds import feeds

app = Flask(__name__)


@app.route('/feed/<feedname>')
def feed(feedname):
    augmenter = feeds.get(feedname, None)
    if not augmenter:
        abort(404)

    return Response(augmenter.augment().to_xml(), mimetype='text/xml')


if __name__ == '__main__':
    app.run(debug=True)