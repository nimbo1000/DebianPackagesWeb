from flask import Flask, render_template
import logging
from logging import Formatter, FileHandler
import os
from parser import Parser

app = Flask(__name__)
app.config.from_object('config')


@app.route('/')
def home():
    my_parser = Parser("/var/lib/dpkg/status")
    packages = sorted(my_parser.get_package_names())
    return render_template('pages/home.html', packages=packages)


@app.route("/<name>")
def package(name):
    my_parser = Parser("/var/lib/dpkg/status")
    package_info = my_parser.get_package_info(name)
    if package_info is not None:
        return render_template("pages/package.html", package_name=name, package_details=package_info)
    else:
        return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    # app.logger.info('errors')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
