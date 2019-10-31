# created by zhaoliyuan

# load data from wind database

import numpy as np
import pandas as pd
from sqlhelper import batch
from sqlhelper.tableToDataframe import toSQL, toDf
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *

Base = declarative_base()

class  (Base)

    __tablename__ = ''

    OBJECT_ID = Column(, primary_key = True)

def loadStock():

    sql = toSQL('wind_db')
    sql = sql.query()
    sql = sql.filter()
    sql = sql.statement
    df = toDf('wind_db', sql, parse_dates = '')

def loadBond():

    sql = toSQL('wind_db')
    sql = sql.query()
    sql = sql.filter()
    sql = sql.statement
    df = toDf('wind_db', sql, parse_dates = '')

def loadCPI():

    sql = toSQL('wind_db')
    sql = sql.query()
    sql = sql.filter()
    sql = sql.statement
    df = toDf('wind_db', sql, parse_dates = '')

def loadPPI():

    sql = toSQL('wind_db')
    sql = sql.query()
    sql = sql.filter()
    sql = sql.statement
    df = toDf('wind_db', sql, parse_dates = '')

def loadGoods():

    sql = toSQL('wind_db')
    sql = sql.query()
    sql = sql.filter()
    sql = sql.statement
    df = toDf('wind_db', sql, parse_dates = '')

