from flask import Blueprint, render_template, redirect, url_for, abort
from random import randrange
# Импорты моделей и форм тоже нужны здесь, так как функции теперь живут тут!
from .models import Opinion 
from .forms import OpinionForm
from . import db

bp = Blueprint('opinions', __name__)

@bp.route('/')
def index_view():
    quantity = Opinion.query.count()
    if not quantity:
        abort(500)
    offset_value = randrange(quantity)
    opinion = Opinion.query.offset(offset_value).first()
    return render_template('opinion.html', opinion=opinion) 

@bp.route('/add', methods=['GET', 'POST'])
def add_opinion_view():
    form = OpinionForm()
    if form.validate_on_submit():
        opinion = Opinion(
            title=form.title.data, text=form.text.data, source=form.source.data
        )
        db.session.add(opinion)
        db.session.commit()
        return redirect(url_for('opinions.opinion_view', id=opinion.id)) # Обрати внимание на имя!
    return render_template('add_opinion.html', form=form)

@bp.route('/opinions/<int:id>')
def opinion_view(id):
    opinion = Opinion.query.get_or_404(id)
    return render_template('opinion.html', opinion=opinion)