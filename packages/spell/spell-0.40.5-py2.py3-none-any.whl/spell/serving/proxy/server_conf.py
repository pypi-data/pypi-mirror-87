bind = "0.0.0.0:8000"
workers = 1
worker_class = "uvloop"

# These are the default configs. Unknown why they're ignored as soon as a config is
# passed into hypercorn
accesslog = "-"
access_log_format = "[proxy] %(h)s %(l)s %(l)s %(t)s %(r)s %(s)s %(b)s %(f)s %(a)s"
