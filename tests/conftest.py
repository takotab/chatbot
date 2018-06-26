# Copyright 2015 Google Inc.
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

"""conftest.py is used to define common test fixtures for pytest."""

from .. import bot
from .. import config
import pytest


def app(request):
    """This fixtures provides a Flask app instance configured for testing.

    It also ensures the tests run within a request context, allowing
    any calls to flask.request, flask.current_app, etc. to work."""
    app = bot.create_app(
        config,
        testing=True,
        )

    with app.test_request_context():
        yield app



