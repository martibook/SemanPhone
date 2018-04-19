from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Required

from database import db_query_word, db_init_comparison, db_approve_word, db_disapprove_word
from exceptions import NoResults
from semanphone import semanphone

app = Flask(__name__)
app.config['SECRET_KEY'] = 'XMDidks2hal89JHNhdk93049dKndOpP'
bootstrap = Bootstrap(app)


class WordForm(FlaskForm):
    word_id = StringField('', validators=[Required()])


@app.route('/', methods=['GET', 'POST'])
def index():
    form = WordForm()
    if form.validate_on_submit():
        word_id = form.word_id.data
        db_query_word(word_id)
        form.word_id.data = ''

        comparison = semanphone(word_id)
        if len(comparison) < 5:
            raise NoResults()
        else:
            session['word_id'] = word_id
            session['comparison'] = comparison
            db_init_comparison(word_id, comparison)
            return redirect(url_for('word'))
    return render_template('index.html', form=form)


@app.route('/word', methods=['GET', 'POST'])
def word():
    form = WordForm()
    if form.validate_on_submit():
        word_id = form.word_id.data
        db_query_word(word_id)
        form.word_id.data = ''

        comparison = semanphone(word_id)
        if len(comparison) < 5:
            raise NoResults()
        else:
            session['word_id'] = word_id
            session['comparison'] = comparison
            db_init_comparison(word_id, comparison)
            return redirect(url_for('word'))
    return render_template('word.html', form=form, word_id=session.get('word_id'), comparison=session.get('comparison'))


@app.route('/approve/<q_word>/<r_word>')
def approve(q_word, r_word):
    db_approve_word(q_word, r_word)
    return "success"


@app.route('/disapprove/<q_word>/<r_word>')
def disapprove(q_word, r_word):
    db_disapprove_word(q_word, r_word)
    return "success"


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.errorhandler(NoResults)
def handle_no_results(error):
    return render_template(error.render_page)


if __name__ == '__main__':
    app.run(debug=True)
