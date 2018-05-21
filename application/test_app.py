from flask import Flask, render_template, redirect, url_for, request, session
from flask_bootstrap import Bootstrap

from application.tools.exceptions import NoResults
from application.tools.database import get_asso_words, get_definitions, pick_words_4experiment, pick_words_4control, \
    get_quiz_info, increase_corrate, decrease_corrate, pick_words


test_app = Flask(__name__)
test_app.config['SECRET_KEY'] = 'XMDidks2hal89JHNhdk93049dKndOpP'
bootstrap = Bootstrap(test_app)


@test_app.route('/')
def index():
    return render_template('test_welcome.html')


@test_app.route('/thankyou')
def thankyou():
    return render_template('test_thankyou.html')


@test_app.route('/semanphone')
def api_semanphone():
    """
    url_format: http://semanphone.fun/semanphone?word=word_argument
    """

    word = request.args.get('word', None)
    if word is not None:
        definition_list = get_definitions(word)
        asso_word_list = get_asso_words(word)
        return render_template('semanphone.html', word=word, asso_word_list=asso_word_list, definition_list=definition_list)
    else:
        raise NoResults()


@test_app.route('/dictionary')
def api_dictionary():
    """
    url_format: http://semanphone.fun/dictionary?word=word_argument
    """

    word = request.args.get('word', None)
    if word is not None:
        definition_list = get_definitions(word)
        return render_template('dictionary.html', word=word, definition_list=definition_list)
    else:
        raise NoResults()


@test_app.route('/experiment')
def experiment():
    # random_words = pick_words_4experiment()
    # session["exp_random_words"] = random_words
    fixed_words = pick_words('experiment')
    session["fixed_words"] = fixed_words
    return render_template('experiment.html', random_words=fixed_words)


@test_app.route('/control')
def control():
    # random_words = pick_words_4control()
    # session["con_random_words"] = random_words
    fixed_words = pick_words("control")
    session["fixed_words"] = fixed_words
    return render_template('control.html', random_words=fixed_words)


@test_app.route('/quiz/<group>')
def quiz(group):
    # if group == 'experiment':
    #     random_words = session["exp_random_words"]
    # elif group == "control":
    #     random_words = session["con_random_words"]
    # else:
    #     random_words = []

    if session["fixed_words"]:
        fixed_words = session["fixed_words"]
    else:
        fixed_words = []

    quiz_info = get_quiz_info(fixed_words)
    return render_template('quiz.html', quiz_info=quiz_info)


@test_app.route('/increase/<word>/<ref_word>/<group>')
def increase(word, ref_word, group):
    """
    increase <group> correct time of the word
    """
    increase_corrate(word=word, ref_word=ref_word, group=group)
    return "success"


@test_app.route('/decrease/<word>/<ref_word>/<group>')
def decrease(word, ref_word, group):
    """
    decrease <group> correct time of the word
    """
    decrease_corrate(word=word, ref_word=ref_word, group=group)
    return "success"


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

