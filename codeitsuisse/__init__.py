from flask import Flask
app = Flask(__name__)
people = {'Karina Kuder': 2, 'Lamont Lasch': 1, 'Jared Jinkins': 1, 'Fabian Fogel': 1, 'Spring Sawin': 1, 'Yuette Yurick': 1, 'Leana Lynde': 1, 'Tracie Temblador': 1, 'Ernesto Eno': 1, 'Percy Parisi': 1, 'Jefferson Juhl': 1, 'Olympia Oliphant': 1, 'Sharyl Shepler': 1, 'Alfonso Allred': 1, 'Simon Sprayberry': 1, 'Lauretta Lippard': 1, 'Rudolf Ravelo': 1, 'Astrid Acheson': 1, 'Pamula Parrinello': 1}
import codeitsuisse.routes.fixedrace
import codeitsuisse.routes.optopt
import codeitsuisse.routes.square
import codeitsuisse.routes.crack