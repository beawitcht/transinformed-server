from flask import Flask, request, make_response, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from werkzeug.exceptions import HTTPException
from utilities import prepare_blogs
from pathlib import Path
import os

from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent / '.env')

is_dev = os.getenv('IS_DEV')


# uses IP as remote address points to load balancer
def get_client_ip():
    if is_dev == '0':
        return request.headers['X-Real-IP']
    else: 
        return get_remote_address

# configure app
app = Flask(__name__)

limiter = Limiter(
    app=app, 
    key_func=get_client_ip,
    storage_uri="memory://",
)
app.config['WTF_CSRF_ENABLED'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = os.getenv('RECAPTCHA_PUBLIC_KEY')
app.config['RECAPTCHA_PRIVATE_KEY'] = os.getenv('RECAPTCHA_PRIVATE_KEY')

# disable caching if in development mode
if is_dev == '0':
    cache = Cache(app, config={'CACHE_TYPE': 'FileSystemCache', 'CACHE_DIR': Path(__file__).resolve().parent / 'tmp' / 'cache', 'CACHE_SOURCE_CHECK': True })
else:
    cache = Cache(app, config={'CACHE_TYPE': 'NullCache'})

# Set headers 
@app.after_request
def add_headers(response):
    response.headers['Strict-Transport-Security'] = 'max-age=63072000; includeSubDomains; preload'
    response.headers['Content-Security-Policy'] = f'default-src \'none\'; script-src \'self\' https://www.google.com/recaptcha/ https://www.gstatic.com/recaptcha/ https://js.stripe.com/v3/; img-src \'self\' data: https://http.cat/ https://*.medium.com/;  style-src \'self\'; font-src \'self\'; connect-src \'self\'; frame-src https://www.google.com/recaptcha/ https://recaptcha.google.com/recaptcha/ https://js.stripe.com/v3/;'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response

# get blogs
entries = prepare_blogs("https://medium.com/feed/@transinformed")

from blueprints import core_bp, blog_bp

app.register_blueprint(core_bp)
app.register_blueprint(blog_bp)

@app.errorhandler(HTTPException)
def handle_error(error):
    # make description generic for rate limit
    if error.code == 429:
        error.description = 'Try again later.'
    return make_response(render_template("error.html", name=error.name ,code=error.code, description=error.description), error.code)

# add header rows on blog posts before each heading and style images

if __name__ == '__main__':
    app.run()
