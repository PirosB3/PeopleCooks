import os
from fabric.api import *

REPOSITORY = 'https://github.com/PirosB3/PeopleCooks'

# Local
PATH = os.path.dirname(os.path.abspath(__file__))
command = lambda c: os.path.join(PATH, c)

def test():
    local('python %s' % command('tests.py'))
# End local

# Environments
def staging():
    env.hosts = ['piros@10.211.55.6:22']
    env.path = '/var/www/'
    env.user = 'www-data'
    env.virtualenv = 'com.peoplecooks.dev'
    env.branch = 'staging'

def production():
    env.hosts = ['piros@192.168.1.100']
    env.path = '/var/www/'
    env.user = 'www-data'
    env.virtualenv = 'com.peoplecooks.www'
    env.branch = 'production'

virtualenv_dir = lambda: os.path.join(env.path, env.virtualenv)
project_dir = lambda: os.path.join(virtualenv_dir(), 'peoplecooks')
source_virtualenv = lambda: 'source %s' % os.path.join(virtualenv_dir(), 'bin/activate')
# End Environments


def pull():
    with cd(project_dir()):
        run('git pull origin %s' % env.branch)
    with prefix(source_virtualenv()):
        run('pip install -r %s' % os.path.join(project_dir(), 'requirements.txt'))

def reload():
    run('service mongo restart')
    run('supervisorctl restart')

def bootstrap():
    sudo("aptitude -y install git-core python-dev python-setuptools build-essential mongodb supervisor")
    with cd(env.path):
        run('virtualenv %s' % env.virtualenv)
    with cd(virtualenv_dir()):
        run('git clone %s peoplecooks' % REPOSITORY)
    with cd(project_dir()):
        run('git checkout remotes/origin/%s' % env.branch)
    pull()

