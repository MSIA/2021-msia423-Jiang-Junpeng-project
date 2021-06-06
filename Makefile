image:
	docker build -t steam .

data/sample/steam.csv:
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY steam run.py download --s3path='s3://2021-msia423-jiang-junpeng/raw/steam.csv' --local_path='./data/sample/steam.csv'

download: data/sample/steam.csv

createdb:
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ steam run.py create_db

ingest:
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ steam run.py ingest

appimage:
	docker build --platform linux/x86_64 -f app/Dockerfile -t steam .

runapp:
	docker run -it -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e MYSQL_HOST -e MYSQL_PORT -e MYSQL_USER -e MYSQL_PASSWORD -e DATABASE_NAME -p 5000:5000 --name teststeam steam

