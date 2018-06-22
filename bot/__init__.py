import numpy as np
import logging
from flask import Flask, current_app, render_template, request, send_file
import time
import os
import logging
import random
import string
# from google.cloud import error_reporting
from .attachement import attachement_check

from . import session_handler
N = 20


def create_app(config, debug=False, testing=False, config_overrides=None):

    app = Flask(__name__)
    app.config.from_object(config)

    app.debug = debug
    app.testing = testing
    if not testing:
        logging.basicConfig(level=logging.INFO)

    @app.route("/")
    def home():        
        # with app.app_context():
        print("project_id: {app.config.PROJECT_ID}")
        print(app.config["PROJECT_ID"])
        id_ = ''.join(random.choice(string.ascii_uppercase + string.digits)
                      for _ in range(N))
        return render_template("index.html", random_id=id_)

    @app.route("/get")
    def get_bot_response():        
        userText, id_ = request.args.get('msg').split("__id__")
        with app.app_context():
            session_return = session_handler.show_post(id_, userText)
        
        #attachement check
        session_return = attachement_check(session_return)

        # session_return = '<img src="/image/vergelijken.png" class="widthSet" alt="pic">'
        session_return = session_return.replace("$qr", "__$qr__")
        session_return = session_return.replace("$button", "__$qr__")
        
        return session_return

    @app.route('/image/<filename>')
    def root(filename):
        loc = os.path.join(os.getcwd(), 'image', "generated", filename)
        print("exist:",os.path.isfile(loc),"loc:",loc)
        if filename == 'a':
            filename = 'dyn_Melis_Schaap.png'
        print("got request", loc)
        # return filename
        return send_file(loc, mimetype='image/gif')

    # Add an error handler that reports exceptions to Stackdriver Error
    # Reporting. Note that this error handler is only used when debug
    # is False
    # @app.errorhandler(500)
    # def server_error(e):
    #     client = error_reporting.Client(app.config['PROJECT_ID'])
    #     client.report_exception(
    #         http_context=error_reporting.build_flask_context(request))
    #     return """
    #     An internal error occurred.
    #     """, 500
    

    return app
