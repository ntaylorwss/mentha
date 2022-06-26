import multiprocessing

workers = multiprocessing.cpu_count()
worker_class = "uvicorn.workers.UvicornWorker"
logger_class = "mentha.api.logging.GunicornLogger"
timeout = 0
keepalive = 120
