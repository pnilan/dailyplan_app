from dailyplan import create_app, mail
from dotenv import load_dotenv

load_dotenv('.env')

app = create_app()

if __name__ == '__main__':
	app.run()
