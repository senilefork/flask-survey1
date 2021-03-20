from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "super-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

#responses = []
num = 0



@app.route('/')
def start():
    title = satisfaction_survey.title    
    return render_template("start.html", title=title)

@app.route('/session-info', methods=["POST"])
def session_info():
    session['responses'] = []
    return redirect(f'/questions/{num}')

@app.route('/questions/<int:num>')
def questions(num):
    question = satisfaction_survey.questions[num].question
    ques = question
    options = satisfaction_survey.questions[num].choices
    responses = session['responses']
    if(num != len(responses)):
         flash('Please choose an option in order to move on', 'error')
         return redirect(f'/questions/{len(responses)}')
    return render_template('questions.html', question=ques, choices=options, num=num)

@app.route('/answers', methods=["POST"])
def save_answers():
    global num

    responses = session['responses']
    if(num != len(responses)):
        return redirect(f'/questions/{len(responses)}')

    answer = request.form.get('answer')
    if(answer == None):
       flash('Please choose an option in order to move on', 'error')
       return redirect(f'/questions/{num}')

    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses
    num += 1

    if(num == len(satisfaction_survey.questions)):
        num = 0
        return redirect('/thankyou')
    return redirect(f'/questions/{num}')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')