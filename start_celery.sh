source /data/suyuan/sfm_env/bin/activate
export SFM_ENV=PROD
cd /data/suyuan/sfm
exec celery worker -A tasks --loglevel=info $*
