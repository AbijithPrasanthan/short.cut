from app.app import app
from app.app import init

if __name__ == '__main__':
	init()
	app.run(host = '0.0.0.0',port='5200',debug = True)

