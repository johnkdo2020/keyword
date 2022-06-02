#!/usr/bin/env python3


import argparse
import os
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('cmd', type=str, nargs=argparse.REMAINDER, default='')
args = parser.parse_args()

PROJECT_NAME = 'keyword'
SOURCE_PATH = os.path.join(os.getcwd(), f'{PROJECT_NAME}')

# AWS EC2 Information
USER = 'ubuntu'
HOST = '52.79.85.87'
TARGET = f'{USER}@{HOST}'
HOME = str(Path.home())
# 현재 폴더 경로
IDENTITY_FILE = os.path.join(HOME, '.ssh', 'keyword-it.pem')
SECRETS_FILE = os.path.join(os.getcwd(), 'secrets.json')

# Docker Information
DOCKER_NAME = f'{PROJECT_NAME}'
DOCKER_IMAGE = f'johnkdo2020/{DOCKER_NAME}'
DOCKER_IMAGE_TAG = f'{DOCKER_NAME}'

DOCKER_OPTIONS = [
    ('--rm', ''),
    ('-it', ''),
    ('-d', ''),
    ('-p', '80:80'),
    ('--name', f'{PROJECT_NAME}'),
]


def run(cmd, ignore_error=False):
    process = subprocess.run(cmd, shell=True)
    if not ignore_error:
        process.check_returncode()


def ssh_run(cmd, ignore_error=False):
    run(f"ssh -o StrictHostKeyChecking=no -i {IDENTITY_FILE} {TARGET} -C {cmd}", ignore_error=ignore_error)


def local_build_push():
    print('*********************build**********************')
    run(f'pip freeze > requirements.txt')
    run(f'sudo docker build -t {DOCKER_IMAGE} .')
    run(f'sudo docker push {DOCKER_IMAGE}')
    print('build finish*************************')


def server_init():
    print('*******************server init ************************')
    ssh_run(f'sudo apt update')
    ssh_run(f'sudo apt --fix-broken install -y')
    ssh_run(f'sudo DEBIAN_FRONTEND=noninteractive apt dist-upgrade -y')
    # ssh_run(f'sudo apt list --upgradable')
    ssh_run(f'sudo apt -y install docker.io')
    print('*******************server setting finish ************************')


def server_pull_run():
    print('*******************server docker hub pull ************************')
    ssh_run(f'sudo docker stop {DOCKER_NAME}', ignore_error=True)
    print('*******************server docker stop ************************')

    ssh_run(f'sudo docker pull {DOCKER_IMAGE}')
    print('*******************server docker hub pull ************************')

    ssh_run('sudo docker run {options} {tag} /bin/bash'.format(
        options=' '.join([
            f'{key} {value}' for key, value in DOCKER_OPTIONS
        ]),
        tag=DOCKER_IMAGE,
    ))
    print('*******************server docker pull completed ************************')


def copy_secrets():
    run(f'scp -i {IDENTITY_FILE} {SECRETS_FILE} {TARGET}:/tmp', ignore_error=True)
    print('**************************scp secrets*******************')
    ssh_run(f'sudo docker cp /tmp/secrets.json {DOCKER_NAME}:/srv/{PROJECT_NAME}')
    print('*******************copy secrets************************')


def server_cmd():
    ssh_run(f'sudo docker exec {DOCKER_NAME} /usr/sbin/nginx -s stop', ignore_error=True)
    print('sudo docker nginx stop')
    ssh_run(f'sudo docker exec {DOCKER_NAME} python manage.py collectstatic --noinput')
    # ssh_run(f'sudo docker exec {DOCKER_NAME} python manage.py crontab add')
    ssh_run(f'sudo docker exec -it -d {DOCKER_NAME} '
            f'supervisord -c /srv/{PROJECT_NAME}/.config/local_dev/supervisord.conf -n')
    print('여기까지 문제 없음')


if __name__ == '__main__':
    try:
        local_build_push()
        server_init()
        server_pull_run()
        copy_secrets()
        server_cmd()
    except subprocess.CalledProcessError as e:
        print('deploy Error')
        print(' cmd:', e.cmd)
        print(' returncode:', e.returncode)
        print(' output:', e.output)
        print(' stdout:', e.stdout)
        print(' stderr:', e.stderr)
