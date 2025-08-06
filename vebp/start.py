from colorama import init

from vebp.app import App
from vebp.libs.launcher import launch


@launch
def run():
    init()
    app = App()
    app.run()