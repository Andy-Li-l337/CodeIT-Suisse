from flask import Flask
app = Flask(__name__)
people = {}
import codeitsuisse.routes.fixedrace
import codeitsuisse.routes.optopt
import codeitsuisse.routes.square
import codeitsuisse.routes.crack