set -e
rm -rf media
python3 thread.py final.html andrew-thread.html
python3 split.py andrew-thread.html andrew-thread.html
python3 lock.py andrew-thread.html andrew-thread.html
