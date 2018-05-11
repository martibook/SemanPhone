from flask import Flask, render_template, session, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm

from wtforms import StringField
from wtforms.validators import Required
from semanphone import semanphone
from tools.exceptions import NoResults
from tools.oxford_dictionary import crawl_word, extract_definitions, extract_examples

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
        form.word_id.data = ''
        comparison = semanphone(word_id)
        if len(comparison) < 5:
            raise NoResults()
        else:
            session['word_id'] = word_id
            session['comparison'] = comparison
            return redirect(url_for('word'))
    return render_template('index.html', form=form)


@app.route('/word', methods=['GET', 'POST'])
def word():
    form = WordForm()
    if form.validate_on_submit():
        word_id = form.word_id.data
        form.word_id.data = ''
        comparison = semanphone(word_id)
        if len(comparison) < 5:
            raise NoResults()
        else:
            session['word_id'] = word_id
            session['comparison'] = comparison
            return redirect(url_for('word'))
    else:
        param = request.args.get('word', None)
        if param is not None:
            word_id = param
            form.word_id.data = ''
            comparison = semanphone(word_id)
            if len(comparison) < 5:
                raise NoResults()
            else:
                session['word_id'] = word_id
                session['comparison'] = comparison
        return render_template('word.html', form=form, word_id=session.get('word_id'), comparison=session.get('comparison'))


@app.route('/api/semanphone', methods=['GET'])
def api_semanphone():
    word = request.args.get('word', None)
    if word is not None:
        asso_word_list = semanphone(word)
        if len(asso_word_list) < 5:
            raise NoResults()
        r = crawl_word(word)
        if r is None:
            raise NoResults()
        definition_list = extract_definitions(r.json())
        return render_template('semanphone.html', word=word, asso_word_list=asso_word_list, definition_list=definition_list)
    else:
        raise NoResults()


@app.route('/api/dictionary', methods=['GET'])
def api_dictionary():
    word = request.args.get('word', None)
    if word is not None:
        r = crawl_word(word)
        if r is None:
            raise NoResults()
        definition_list = extract_definitions(r.json())
        return render_template('dictionary.html', word=word, definition_list=definition_list)
    else:
        raise NoResults()


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

