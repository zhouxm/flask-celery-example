import logging
import os
import json
from flask import Flask, request, render_template, session, flash, redirect, url_for, jsonify
from flask_mail import Mail

from search.worker import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret!'

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.qq.com'
# app.config['MAIL_PORT']             = 587
# app.config['MAIL_USE_TLS']          = True
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = '77095729@qq.com'

# Celery configuration
# app.config['CELERY_BROKER_URL']     = 'redis://1qaz#WSX3edc#zhouxm.@www.leoleo.com.cn:19637/1'
# app.config['CELERY_RESULT_BACKEND'] = 'redis://1qaz#WSX3edc#zhouxm.@www.leoleo.com.cn:19637/1'
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/1'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# # Initialize extensions
mail = Mail(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', email=session.get('email', ''))
    email = request.form['email']
    session['email'] = email

    # send the email
    email_data = {
        'subject': 'Hello from Flask',
        'to': email,
        'body': 'This is a test email sent from a background Celery task.'
    }
    if request.form['submit'] == 'Send':
        # send right away
        send_async_email.delay(email_data)
        flash(f'Sending email to {email}')
    else:
        # send in one minute
        send_async_email.apply_async(args=[email_data], countdown=60)
        flash(f'An email will be sent to {email} in one minute')

    return redirect(url_for('index'))


@app.route('/longtask', methods=['POST'])
def longtask():
    task = long_task.apply_async()
    return jsonify({}), 202, {'Location': url_for('taskstatus', task_id=task.id)}


@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = long_task.AsyncResult(task_id)

    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    logging.warning(f"service:task id [{task.id}] status [{json.dumps(response)}]")
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
