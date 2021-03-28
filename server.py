import asyncio

try:
    import ujson as json
except ImportError:
    import json

import threading
import traceback

from flask import Flask, request, g, jsonify

from utils.db import get_redis
from utils.exceptions import BadRequest, InvalidImage

from sentry_sdk import capture_exception

import time

# Initial require, the above line contains our endpoints.

config = json.load(open('config.json'))
endpoints = None

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5000

if 'sentry_dsn' in config:
    import sentry_sdk
    from sentry_sdk.integrations.flask import FlaskIntegration

    sentry_sdk.init(config['sentry_dsn'],
                    integrations=[FlaskIntegration()])


@app.before_first_request
def init_app():
    def run_gc_forever(loop):
        asyncio.set_event_loop(loop)
        try:
            loop.run_forever()
        except (SystemExit, KeyboardInterrupt):
            loop.close()

    gc_loop = asyncio.new_event_loop()
    gc_thread = threading.Thread(target=run_gc_forever, args=(gc_loop,))
    gc_thread.start()
    g.gc_loop = gc_loop

    from utils.endpoint import endpoints as endpnts
    global endpoints
    endpoints = endpnts
    # idk why this is here, but whatever
    import endpoints as _


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'pg'):
        g.pg.close()


@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"ok": True, "time": time.time() })


@app.route('/stats', methods=['GET'])
def stats():
    data = {}

    for endpoint in endpoints:
        data[endpoint] = {'hits': int(get_redis().get(endpoint + ':hits') or 0),
                          'avg_gen_time': endpoints[endpoint].get_avg_gen_time()}

    return jsonify(data)


@app.route('/gen/<endpoint>', methods=['GET', 'POST'])
def api(endpoint):
    if request.headers.get('Authorization', None) != config.get('token', None):
        return jsonify({'status': 403, 'code': 0, 'error': 'Invalid token!'}), 403
    if endpoint not in endpoints:
        return jsonify({'status': 404, 'code': 0, 'error': 'Endpoint {} not found!'.format(endpoint)}), 404
    if request.method == 'POST' and not request.is_json:
        return jsonify({'status': 400, 'code': 0, 'error': 'Payload must be in JSON format!'}), 400

    # Get kwargs
    if request.method == 'POST':
        kwargs = request.json
    else:
        kwargs = {}
        for arg in request.args:
            kwargs[arg] = request.args.get(arg)

    # Run endpoint
    try:
        result = endpoints[endpoint].run(**kwargs)
    except BadRequest as br:
        traceback.print_exc()
        if 'sentry_dsn' in config:
            capture_exception(br)
        return jsonify({'status': 400, 'code': 0, 'error': str(br)}), 400
    except InvalidImage as e:
        return jsonify({'status': 400, 'code': 2, 'error': str(e) }), 400
    except KeyError as e:
        return jsonify({'status': 400, 'code': 1, 'error': 'Missing parameter: ' + str(e).split('\'')[1], 'param': str(e).split('\'')[1] }), 400
    except Exception as e:
        traceback.print_exc()
        if 'sentry_dsn' in config:
            capture_exception(e)
        return jsonify({'status': 500, 'code': -1, 'error': str(e)}), 500

    return result, 200


if __name__ == '__main__':
    app.run(debug=False, use_reloader=False)
