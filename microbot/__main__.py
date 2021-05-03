"""
__main__.py
"""
from . import socketio, create_app


def main():
    from werkzeug.debug import DebuggedApplication

    application = create_app()
    application.debug = True
    application.wsgi_app = DebuggedApplication(application.wsgi_app, evalex=True)
    socketio.run(application)


if __name__ == "__main__":
    main()
