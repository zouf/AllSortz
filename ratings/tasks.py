from celery.decorators import task

@task(name="tasks.add")
def add(x, y):
    return x + y