# Copyright 2018 Google LLC
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

# [START gae_python37_render_template]
import datetime

from flask import Flask, render_template, request, abort
from scipy import stats

app = Flask(__name__)


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def calc_p_value():
    try:
        control_number_of_visitors = float(request.form.get('control_number_of_visitors'))
        control_number_of_conversion = float(request.form.get('control_number_of_conversion'))
        variation_number_of_visitors = float(request.form.get('variation_number_of_visitors'))
        variation_number_of_conversions = float(request.form.get('variation_number_of_conversions'))

        con_conv = control_number_of_conversion / control_number_of_visitors
        test_conv = variation_number_of_conversions / variation_number_of_visitors

        p_value_result = get_p_value(con_conv, test_conv,
                                     control_number_of_visitors, variation_number_of_visitors)
        return render_template('index.html', p_value=round(p_value_result, 3))
    except ValueError:
        abort(400)


def get_p_value(con_conv, test_conv, con_size, test_size):
    lift = -abs(test_conv - con_conv)

    scale_one = con_conv * (1 - con_conv) * (1 / con_size)
    scale_two = test_conv * (1 - test_conv) * (1 / test_size)
    scale_val = (scale_one + scale_two) ** 0.5

    p_value = stats.norm.cdf(lift, loc=0, scale=scale_val)
    return p_value


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [START gae_python37_render_template]
