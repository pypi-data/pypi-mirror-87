import multiprocessing

bind = "0.0.0.0:8000"
workers = (multiprocessing.cpu_count() * 2) + 1
worker_class = "uvloop"

# These are the default configs. Unknown why they're ignored as soon as a config is
# passed into hypercorn
accesslog = "-"
access_log_format = "[server%(p)s] %(h)s %(l)s %(l)s %(t)s %(r)s %(s)s %(b)s %(f)s %(a)s"
