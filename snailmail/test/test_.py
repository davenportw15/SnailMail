
from flask import Flask, jsonify, session, request, redirect, url_for, render_template, flash
import sqlite3
import os
from datetime import datetime

from snailmail.models.user import User
from snailmail.models.mail import Mail
from snailmail.database import db_session
from snailmail.database import init_db

init_db()
print("It's working")


assert 0

