utube:
	chmod +x utube_scraper.py utube.py
	mkdir -p ${HOME}/.local/utube/
	cp utube_scraper.py ${HOME}/.local/bin/utube_scraper.py
	cp utube.py ${HOME}/.local/bin/utube
	crontab ./scripts/scrape.cron
	cp ./scripts/utlh ${HOME}/.local/bin/
	cp ./scripts/utwatch ${HOME}/.local/bin/
	cp ./scripts/utdownload ${HOME}/.local/bin/

clean:
	rm ${HOME}/.local/bin/utube
	rm ${HOME}/.local/bin/utube_scraper.py

demo:
	rm ${HOME}/.local/bin/utlh
	rm ${HOME}/.local/bin/utwatch
	rm ${HOME}/.local/bin/utdownload
