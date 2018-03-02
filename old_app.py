from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm

from wtforms import StringField
from wtforms.validators import Required
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
        session['word_id'] = form.word_id.data
        session['comparison'] = semanphone(session['word_id'])
        form.word_id.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, word_id=session.get('word_id'), comparison=session.get('comparison'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)

