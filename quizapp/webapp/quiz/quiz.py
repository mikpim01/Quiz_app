from flask import render_template, request, flash

from quiz import app, db
from quiz.db_tables import Question
from quiz.forms import QuizForm


@app.route('/', methods=['GET', 'POST'])
def quiz():
    questions = Question.query.all()
    form = QuizForm(request.form)
    if request.method == 'POST':
        # we are checking if the number of answers in the form data is the same
        # as the number of questions in the quiz.
        if len(form.answers.entries) == len(questions):
            return _render_score_page_(questions)
        else:
            flash("You must answer all the questions.")

    return _render_quiz_page_(form, questions)


def _render_quiz_page_(form, questions):
    for i, question in enumerate(questions):
        form.answers.append_entry()
        choices = [('1', question.option_a),
                   ('2', question.option_b),
                   ('3', question.option_c),
                   ('4', question.option_d)]
        form.answers.entries[i].choices = choices

    return render_template("quiz.html", questions=questions, form=form)


def _render_score_page_(questions):
    answers = []
    user_score = 0
    for i, question in enumerate(questions):
        user_answer = int(request.form['answers-' + str(i)])
        user_answer_letter = _get_answer_letter_(user_answer)
        if user_answer == question.answer:
            user_score += 1
            answers.append('{0} is correct'.format(user_answer_letter))
        else:
            correct_answer_letter = _get_answer_letter_(question.answer)
            answers.append('{0} is incorrect. Correct answer is {1}'
                           .format(user_answer_letter, correct_answer_letter))

    return render_template('quiz_answers.html', questions=questions,
                           answers=answers, score=user_score)


def _get_answer_letter_(user_answer):
    return chr(ord('A') + user_answer - 1)