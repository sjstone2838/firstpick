from celery import Celery

app = Celery('tasks', broker='django://')

@app.task
def add():
	print "hello"
