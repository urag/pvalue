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
    app.run(host='127.0.0.1', port=8080, debug=True)

