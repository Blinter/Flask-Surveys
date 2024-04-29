from flask import Flask, render_template, session, request, redirect, flash
# from flask_debugtoolbar import DebugToolbarExtension

from surveys import *

app = Flask(__name__)

app.config['SECRET_KEY'] = "oh-so-secret4"

# debug = DebugToolbarExtension(app)


@app.route('/', methods=['GET'])
def main_menu():
    """Main page, all POST redirects to /answer, then back to
     this page after taking form data information."""
    if not session.get('selected_survey', False):
        session['selected_survey'] = []
        session.modified = True
    if not session.get('survey_items', False):
        session['survey_items'] = []
        session.modified = True
    if not session.get('selected_survey', False):
        """Survey has NOT been selected by the user, and currently has no 
        questions answered."""
        return render_template("survey.html",
                               possible_surveys=surveys,
                               survey_items=session.get('survey_items', False))
    else:
        current_survey = surveys[session.get('selected_survey')]
        count_progress = len(session.get('survey_items', ''))
        if not session.get('survey_items', False):
            """Survey has been selected by the user, and currently has no 
            questions answered."""
            flash("You started a survey! Thank you so much!", 'success')
            return render_template("survey.html",
                                   select=current_survey,
                                   survey_items=current_survey.questions[
                                       len(session.get('survey_items', 0))])

        """Check that all survey questions are taken and display the results 
        back to the user. Provide ALL other surveys which can be 
        administered."""
        completed_at_progress = len(current_survey.questions)
        if completed_at_progress == count_progress:
            flash("You're awesome! Thanks for completing the survey!",
                  'success')
            return render_template("completed.html",
                                   select=current_survey,
                                   results=session.get('survey_items', []),
                                   resultst=session.get('survey_text_items',
                                                        []),
                                   possible_surveys=surveys)

        """Flash % Completion, Then provide specific items required by 
        client
        when end_survey is true, NEXT submit button converts to FINISH"""
        if completed_at_progress != count_progress + 1:
            (flash("Survey Completion: " + str(
                ((count_progress / completed_at_progress) * 100) // 1) + "%",
                   'success'))
        else:
            flash("You're almost done! Last question!", 'success')
        return render_template("survey.html",
                               select=current_survey,
                               survey_items=current_survey.questions[
                                   len(session.get('survey_items', 0))],
                               end_survey=
                               completed_at_progress == count_progress + 1)


@app.route('/answer', methods=["POST"])
def answer():
    """Page that handles all survey responses
    This route is only used to append to the session variables,
    respective to the user.
    """

    """Overwrites current selected survey and starts a new one"""
    restart_survey = request.form.get('newSurveyName', False)
    if restart_survey:
        session['selected_survey'] = restart_survey
        session['survey_items'] = []
        session['survey_text_items'] = []
        session.modified = True
        return redirect('/', 302)

    """Initial Survey Request"""
    start_survey = request.form.get("surveyName", False)
    if start_survey:
        if not session.get('selected_survey', False):
            session['selected_survey'] = []
            session['survey_text_items'] = []
        session['selected_survey'] = start_survey
        session.modified = True
        return redirect('/', 302)

    """Brand new survey initialization from clean user start"""
    current_survey = request.form.get("selectedChoice", False)
    if not session.get('survey_items', False) or not session.get(
            'survey_text_items', False):
        session['survey_items'] = []
        session['survey_text_items'] = []
        session.modified = True

    """Append to session objects"""
    if current_survey:
        current_text = request.form.get('selectedChoice', False)
        provided_text = request.form.get("textInput", False)
        session['survey_text_items'].append(provided_text if
                                            provided_text else '')
        session['survey_items'].append(current_text if current_text else '')
        session.modified = True
        return redirect('/', 302)

    """Return back to homepage anyway"""
    return redirect('/', 302)
