daemon = False
chdir = '/srv/keyword/app'
bind = 'unix:/run/keyword.sock'
accesslog = '/var/log/gunicorn/keyword-accesslog.log'
errorlog = '/var/log/gunicorn/keyword-error.log'
capture_output = True