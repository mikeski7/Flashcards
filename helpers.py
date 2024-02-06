import requests

from flask import redirect, render_template, session
from functools import wraps


def apology(message):
    """Render message as an apology to user."""
    return render_template("apology.html", text=message)


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def translate(word, source_language='en', target_language='es', api_key='b8fba6eeb495da3683253c64f47a8ebb3eb21074df920e17e6efeeec8b92c5f7'):
    url = f'https://api.pons.com/v1/dictionary?l={source_language}{target_language}&q={word}'
    headers = {'X-Secret': api_key}

    response = requests.get(url, headers=headers)

    results=[]

    if response.status_code == 200:
        data = response.json()
        """translations = data.get('hits', [])"""
        for dict in data[0]["hits"][0]["roms"][0]["arabs"][0]["translations"]:
            results.append(dict["target"].split(" ")[0])
        return results

    else:
        print(f"Error {response.status_code}: {response.text}")
        return []

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def cards():
    card_list = db.execute("SELECT source, target FROM database WHERE user_id = ?", user_id)
    return card_list