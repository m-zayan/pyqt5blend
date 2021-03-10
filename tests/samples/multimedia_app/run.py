from tests.samples.multimedia_app.app import MultimediaApp

config = {'full_screen': False, 'fixed_size': True}

gui = MultimediaApp(name='API Test (MultimediaApp)', screen_geometry=(0, 0, 1440, 810), config=config)
gui.run()
