from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap

from application.tools.exceptions import NoResults
from application.algorithms.semanphone import semanphone
from application.tools.oxford_dictionary import crawl_word, extract_definitions


test_app = Flask(__name__)
bootstrap = Bootstrap(test_app)


@test_app.route('/', methods=['GET'])
def index():
    return render_template('test_welcome.html')


@test_app.route('/semanphone', methods=['GET'])
def api_semanphone():
    """
    url_format: http://semanphone.fun/semanphone?word=word_argument
    """

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


@test_app.route('/dictionary', methods=['GET'])
def api_dictionary():
    """
    url_format: http://semanphone.fun/dictionary?word=word_argument
    """

    word = request.args.get('word', None)
    if word is not None:
        r = crawl_word(word)
        if r is None:
            raise NoResults()
        definition_list = extract_definitions(r.json())
        return render_template('dictionary.html', word=word, definition_list=definition_list)
    else:
        raise NoResults()


@test_app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@test_app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@test_app.errorhandler(NoResults)
def handle_no_results(error):
    return render_template(error.render_page)


if __name__ == '__main__':
    test_app.run(debug=True)

