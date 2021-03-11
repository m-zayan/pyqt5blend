from pyqt5blend.tests.samples.cacao_app.app import CacaoApp

config = {'full_screen': False, 'fixed_size': True}

gui = CacaoApp(name='Cacao', screen_geometry=(0, 0, 1440, 810), config=config)
gui.run()
