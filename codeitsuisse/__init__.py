from flask import Flask
app = Flask(__name__)
people = {}
from codeitsuisse.routes import *