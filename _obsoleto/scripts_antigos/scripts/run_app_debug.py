from main import App
import traceback
try:
    app = App()
    print('App created OK')
except Exception as e:
    print('Exception during App init:')
    traceback.print_exc()
