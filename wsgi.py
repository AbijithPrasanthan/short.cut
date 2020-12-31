from app.app import app
from app.app import init

if __name__ == '__main__':
	init()
	app.run(debug = True)

