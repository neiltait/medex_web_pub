#!/bin/bash
set -e

#Run Gunicorn
exec gunicorn medexCms.wsgi:application \
  --name medex-cms \
  --bind 0.0.0.0:80 \
  --workers 3 \
  --log-level=info \
  --log-file=- \
  --access-logfile=- \
  --error-logfile=- \
  --timeout 60


# EXECUTE DOCKER COMMAND NOW
exec "$@"
