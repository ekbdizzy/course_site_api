import os
from fabric import task
from fabric.connection import Connection, Config

# run, sudo, env, cd
from fab_templates import fab_config as config

HOST = 'root@67.205.130.122'

c = Connection(host=HOST)

ROOT = config.ROOT
GIT_REPO = config.GIT_REPO
USER_NAME = config.USER_NAME
USER_EMAIL = config.USER_EMAIL

PROJECT_NAME = 'course_site_api'
PROJECT_PATH = os.path.join(ROOT, PROJECT_NAME)
VENV_PATH = os.path.join(PROJECT_PATH, 'venv')


@task
def hello(c):
    with Connection(host=HOST) as c:
        c.run("whoami")
        c.run('pwd')


@task
def install_packages(c):
    packages = [
        'python3-pip',
        'python3.7',
        'python3.7-dev',
        'nginx',
        'git-core',
        'npm',
    ]
    with Connection(host=HOST) as c:
        c.sudo('apt update -y')
        c.sudo('apt install software-properties-common -y')
        c.sudo('add-apt-repository ppa:deadsnakes/ppa -y')
        c.sudo(f'apt-get install -y {" ".join(packages)}')
        c.run('python3.7 -m pip install virtualenv')


@task
def install_project_code(c):
    with Connection(host=HOST) as c:
        if c.run(f'test -d {ROOT}', warn=True).failed:
            c.run(f'mkdir -p {ROOT}')

        if c.run(f'test -d {PROJECT_PATH}', warn=True).failed:
            with c.cd('/home/root'):
                c.run(f'git clone {GIT_REPO}')
        else:
            with c.cd(PROJECT_PATH):
                c.run('git pull')


#

@task
def create_venv(c):
    with Connection(host=HOST) as c:
        with c.cd(ROOT):
            if c.run(f'test -d {VENV_PATH}', warn=True).failed:
                c.run(f'python3.7 -m virtualenv {VENV_PATH}')


@task
def install_pip_requirements(c):
    with Connection(host=HOST) as c:
        with c.cd(PROJECT_PATH):
            c.run(f'{VENV_PATH}/bin/python3.7 -m pip install -r requirements.txt -U')


#
# def npm_install():
#     with cd(PROJECT_PATH):
#         sudo('npm install')
#
#
@task
def configure_uwsgi(c):
    with Connection(host=HOST) as c:
        c.sudo('python3 -m pip install uwsgi')
        c.sudo('mkdir -p /etc/uwsgi/sites')
        c.put('fab_templates/uwsgi.ini', '/etc/uwsgi/sites/course_site_api.ini')
        c.put('fab_templates/uwsgi.service', '/etc/systemd/system/uwsgi.service')


@task
def configure_nginx(c):
    with Connection(host=HOST) as c:
        if c.run(f'test -d /etc/nginx/sites-enabled/default', warn=True).failed:
            c.sudo('rm /etc/nginx/sites-enabled/default')
        c.put('fab_templates/nginx.conf', '/etc/nginx/sites-enabled/course_site_api.conf')


@task
def create_env_config(c):
    with Connection(host=HOST) as c:
        c.put('course_site/env.py', f'{PROJECT_PATH}/course_site/env.py')


@task
def migrate_database(c):
    with Connection(host=HOST) as c:
        with c.cd(PROJECT_PATH):
            c.run(f'{VENV_PATH}/bin/python manage.py makemigrations course lesson user')
            c.run(f'{VENV_PATH}/bin/python manage.py migrate')


@task
def collectstatic(c):
    with Connection(host=HOST) as c:
        with c.cd(PROJECT_PATH):
            c.run(f'{VENV_PATH}/bin/python manage.py collectstatic')


#
# def npm_run_build():
#     with cd(PROJECT_PATH):
#         run('npm run build')
#
#

@task
def createsuperuser(c):
    with Connection(host=HOST) as c:
        with c.cd(PROJECT_PATH):
            command = f'manage.py createsuperuser --username {USER_NAME} --email {USER_EMAIL}'
            c.run(f'{VENV_PATH}/bin/python {command}')


@task
def restart_all(c):
    with Connection(host=HOST) as c:
        c.sudo('systemctl daemon-reload')
        c.sudo('systemctl reload nginx')
        c.sudo('systemctl restart uwsgi')

#
# def bootstrap():
#     install_packages()
#     install_project_code()
#     create_venv()
#     install_pip_requirements()
#     # npm_install()
#     configure_uwsgi()
#     configure_nginx()
#     create_env_config()
#     migrate_database()
#     collectstatic()
#     # npm_run_build()
#     create_superuser()
#     restart_all()
