install:
	pip install -r requirements.txt

	ln -s /var/www/scouts-bevaix.ch/www.scouts-bevaix.ch/.system/www.scouts-bevaix.ch_nginx.conf /etc/nginx/sites-enabled
	ln -s /var/www/scouts-bevaix.ch/www.scouts-bevaix.ch/.system/www.scouts-bevaix.ch_gunicorn.service /etc/systemd/system

	systemctl daemon-reload
	systemctl restart nginx
	systemctl enable www.scouts-bevaix.ch_gunicorn
	systemctl restart www.scouts-bevaix.ch_gunicorn
