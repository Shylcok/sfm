#source /data/htapp/.virtualenvs/hera/bin/activate
#export PYTHONPATH=/data/htapp/hera/
#export HTAPP_ENV=PROD
exec python sfm.py --log-file-prefix=/data/htapp/log/hera.log --log-rotate-mode=time --log-rotate-when=midnight $*