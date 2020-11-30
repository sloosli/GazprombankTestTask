from flask import render_template, request, jsonify
from . import app, db
from .models import User, Dictionary


@app.route('/')
def quiz_get():
    towns = Dictionary.query.filter_by(
        type_id=Dictionary.Type.town).order_by('value').all()
    return render_template('quiz.html', towns=towns)


@app.route('/', methods=['POST'])
def quiz_post():
    data = request.form
    errors = User.validate(data)
    if errors:
        return jsonify({'errors': list(errors)}), 422
    user = User(data)
    db.session.add(user)
    db.session.commit()
    return render_template('thanks.html')
