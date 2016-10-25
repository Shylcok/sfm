source /data/suyuan/sfm_env/bin/activate
#export PYTHONPATH=/data/htapp/hera/
export SFM_ENV=PROD
exec python sfm.py --log-rotate-mode=time --log-rotate-when=midnight $*
