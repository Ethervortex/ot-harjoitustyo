from invoke import task
from subprocess import call
from sys import platform

@task
def start(ctx):
    print("Starting SciCalc")
    ctx.run("python3 src/index.py", pty=True)

@task
def test(ctx):
    ctx.run("pytest src", pty=True)

@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest src", pty=True)

@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html", pty=True)
    if platform != "win32":
        call(("xdg-open", "htmlcov/index.html"))

@task
def lint(ctx):
    ctx.run("pylint src", pty=True)

@task
def build(ctx):
    ctx.run("python3 src/build.py", pty=True)
