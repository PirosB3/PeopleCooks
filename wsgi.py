import os
from settings import ADDRESS

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN = 'main:app'
WORKERS = '4'

def main():
    # Change to working directory
    os.chdir(PROJECT_DIR)

    # Run Gunicorn
    os.execvp('gunicorn',(
        'gunicorn',
        MAIN,
        '-b %s' % ADDRESS,
        '-w %s' % WORKERS
    ))

if __name__ == '__main__':
    main()
