from app import app, api
from app.utils import configure_resources_routing


configure_resources_routing()

if __name__ == '__main__':
    app.run()