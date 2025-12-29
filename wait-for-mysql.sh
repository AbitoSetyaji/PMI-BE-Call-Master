#!/bin/sh
# wait-for-mysql.sh - Wait for MySQL to be ready before starting the application

set -e

host="$1"
shift
cmd="$@"

echo "⏳ Waiting for MySQL at $host to be ready..."
echo "   (MySQL first-time initialization can take up to 2 minutes)"

max_retries=60
retry_count=0
retry_interval=3

until mysql -h"$host" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" --skip-ssl -e "SELECT 1" > /dev/null 2>&1; do
  retry_count=$((retry_count + 1))
  
  if [ $retry_count -ge $max_retries ]; then
    echo "❌ MySQL did not become ready in time. Exiting..."
    exit 1
  fi
  
  if [ $((retry_count % 10)) -eq 0 ]; then
    echo "⏳ Still waiting for MySQL... ($((retry_count * retry_interval))s elapsed)"
  fi
  
  sleep $retry_interval
done

echo "✅ MySQL is ready! Connection verified."
exec $cmd
