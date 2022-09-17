from flask import Flask

app = Flask(__name__)
import codeitsuisse.routes.tickerStream
import codeitsuisse.routes.manualEndpoint
import codeitsuisse.routes.collatz
import codeitsuisse.routes.magiccauldrons