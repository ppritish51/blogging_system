1. python manage.py test authPortal or python manage.py test authPortal.auth_portal_tests

uwsgi logs: tail -f /var/log/uwsgi/myapp.log
nginx location: /etc/nginx/sites-available/
serviceD logs: 
1. journalctl -u CheetahMatrixDev --reverse
2. journalctl -u CheetahMatrixDev -f
3. journalctl -u CheetahMatrixASGIDev --reverse
4. journalctl -u CheetahMatrixASGIDev -f
5. django logs: tail -f /var/www/dev/debug.log
6. systemctl status CheetahMatrixDev
7. systemctl status CheetahMatrixASGIDev

Other helpful commands:
1. systemctl daemon-reload
2. systemctl stop CheetahMatrixDev

Need to run redis in dev env so that channel can communicate between asgi and wsgi 
1. sudo apt-get install redis-server
2. sudo systemctl start redis
3. sudo systemctl enable redis

Postgres
1. systemctl status postgresql

Postgres setup:
1. sudo apt-get update
2. sudo apt-get install postgresql postgresql-contrib
3. sudo -i -u postgres //postgres user
4. psql
5. CREATE DATABASE your_database_name;
6. CREATE USER your_user_name WITH ENCRYPTED PASSWORD 'your_password';
7. GRANT ALL PRIVILEGES ON DATABASE your_database_name TO your_user_name; //Grant privileges to the user for the database
8. \q  //Exit the PostgreSQL prompt
9. exit //Switch back to the original user account

systemctl show -p MemoryLimit postgresql
systemctl show -p MemoryLimit redis-server
systemctl show -p MemoryLimit CheetahMatrixDev
systemctl show -p MemoryLimit CheetahMatrixASGIDev

######
If you run celery -A CheetahMatrix worker --loglevel=info & directly in the terminal, it will start the process in the background of that terminal session.

Closing the terminal will not necessarily kill this background process.

To manage the background process:

To Bring the Process to Foreground:
If you have just one job running in the background, you can bring it to the foreground using:
bash
Copy code
fg
If you have multiple jobs, you can list them with jobs and then bring the desired one to the foreground using its job number:
bash
Copy code
fg %1
Where %1 is the job number.
To Stop the Process:
Once the process is in the foreground (using the fg command), you can stop it using CTRL + C.
To Kill the Process:
If you know the process is running and you want to kill it without bringing it to the foreground:
a. Find the process ID (PID) using:
bash
Copy code
ps aux | grep 'celery worker'
b. Identify the PID from the output and kill it:
bash
Copy code
kill -9 PID
Replace PID with the actual process ID.
However, in a production environment or more structured development setup, it's advisable to manage Celery (and other services) using a process control system like systemd, as you're already doing with uWSGI and Uvicorn. This provides a more robust way to start, stop, and monitor the processes.