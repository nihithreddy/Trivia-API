import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category


QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app)

    @app.after_request
    def cors_after_request(response):
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,POST,PUT,PATCH,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        return response

    '''
  @DONE:
  Create an endpoint to handle GET requests
  for all available categories.
  '''
    @app.route('/categories', methods=['GET'])
    def get_all_available_categories():
        all_categories = Category.query.all()
        # Using Dictionary Comprehension
        result_categories = {category.format()["id"]: category.format()[
            "type"] for category in all_categories}
        print(result_categories)  # For Debugging Purpose
        return jsonify({
            "success": True,
            "categories": result_categories
        })

    '''
  @DONE:
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen
  for three pages.Clicking on the page numbers should update the questions.
  '''
    @app.route('/questions', methods=['GET'])
    def get_questions():
        # Retrieveing questions in the insertion order
        available_questions = Question.query.order_by(Question.id).all()
        # If there are no questions then we throw a 404 error
        if len(available_questions) == 0:
            abort(404)
        # Retrieveing categories in the alphabetical order
        available_categories = Category.query.order_by(Category.type).all()
        result_categories = {category.format()["id"]: category.format()[
            "type"] for category in available_categories}
        # Now Lets apply Pagination technique
        # Get the page number from the request arguments
        page_number = request.args.get(
            'page', 1, type=int)  # Default Page Number is 1
        # Find the Start Number
        start_number = (page_number - 1) * QUESTIONS_PER_PAGE
        end_number = start_number + QUESTIONS_PER_PAGE  # Find the End Number
        # Get all the questions
        paginated_questions = available_questions[start_number:end_number]
        # Formatting the questions by using format method
        formatted_questions = [question.format()
                               for question in paginated_questions]
        return jsonify({
            "questions": formatted_questions,
            "totalQuestions": len(formatted_questions),
            "currentCategory": None,
            "categories": result_categories,
            "success": True
        })

    '''
  @DONE:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will
  be removed.This removal will persist in the database and when you refresh
  the page.
  '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question_to_delete = Question.query.get(question_id)
            # If there is no question with the question_id then we abort thr
            # request
            if not question_to_delete:
                abort(404)
            # If question indeed exists then we can go ahead and delete it
            else:
                question_to_delete.delete()
        except BaseException:
            abort(404)
        return jsonify({
            "success": True,
            # For Checking if the question has been deleted or not
            "message": "Success deleted question with id " + str(question_id)
        })

    '''
  @DONE:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''
    @app.route('/questions', methods=['POST'])
    def create_new_question():
        params = request.get_json()
        # If we don't receive all the required
        # parameters(question,answer,difficulty,category) then we dont handle
        # the request
        if("question" not in params):
            abort(422)
        if("answer" not in params):
            abort(422)
        if("difficulty" not in params):
            abort(422)
        if("category" not in params):
            abort(422)
        question = params["question"]  # Retrieving thr question
        question_answer = params["answer"]  # Retrieving the answer
        question_difficuly = params["difficulty"]  # Retrieving the difficulty
        # Retrieving the category of the question
        question_category = params["category"]
        # Finally inserting the question in the table
        new_question = Question(
            question=question,
            answer=question_answer,
            difficulty=question_difficuly,
            category=question_category)
        try:
            new_question.insert()
        except BaseException:
            abort(422)
        return jsonify({
            "success": True,
            # For Checking if question has been created or not
            "message": "Created question with the id " + str(new_question.id)
        })

    '''
  @DONE:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''
    @app.route("/questions/search", methods=["POST"])
    def search_question():
        params = request.get_json()
        # First we search for searchTerm if it doesn't exist then we abort thr
        # request
        if("searchTerm" not in params):
            abort(422)
        search_query_word = params["searchTerm"]
        print(search_query_word)
        # Using ilike method for case insensitivity
        # For Case sensitivity we can use like
        found_questions = Question.query.filter(
            Question.question.ilike('%' + search_query_word + '%')).all()
        # Formatting the questions by using format method
        formatted_questions = [question.format()
                               for question in found_questions]
        return jsonify({
            "questions": formatted_questions,
            "totalQuestions": len(formatted_questions),
            "currentCatgeory": None,
            "success": True
        })

    '''
  @DONE:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def get_questions_by_category(category_id):
        current_category = Category.query.get(category_id)
        # If there is no category with the given category id then we throw a
        # 404 error
        if current_category is None:
            abort(404)
        # Convert category_id from integer to string because it is stored as
        # VARCHAR in database table
        category_id = str(category_id)
        # Getting questions of required category
        required_questions = Question.query.filter(
            Question.category == category_id).all()
        # Using Dictionary Comprehension
        formatted_questions = []
        # Formatting the questions by using format method
        for question in required_questions:
            formatted_questions.append(question.format())
        return jsonify({
            "questions": formatted_questions,
            "totalQuestions": len(formatted_questions),
            "currentCategory": current_category.type,
            "success": True
        })

    '''
  @DONE:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''
    @app.route("/quizzes", methods=["POST"])
    def play_trivia_game():
        params = request.get_json()
        # If the required parameters doesn't exist in json object then we abort
        # the request
        if ("previous_questions" not in params):
            abort(422)
        if ("quiz_category" not in params):
            abort(422)
        # Now Retreive the parameters from the json object params
        previous_quiz_questions = params["previous_questions"]
        quiz_category = params["quiz_category"]
        print(previous_quiz_questions)
        print(quiz_category)
        quiz_category_id = quiz_category["id"]
        quiz_category_type = quiz_category["type"]
        # Now find all the questions which are of quiz_category type
        # If the User Chooses all the categories
        if quiz_category_id == 0:
            required_questions = Question.query.all()
        # Else if the user chooses a specific category
        else:
            required_questions = Question.query.filter(
                Question.category == quiz_category_id).all()
        # Now exclude the previous questions from the above list of questions
        final_questions = []
        for question in required_questions:
            if question.id not in previous_quiz_questions:
                final_questions.append(question)
        # If there are no questions then return None
        if (len(final_questions) == 0):
            return jsonify({
                "success": True,
                "question": None
            })
        # Now Select a Random Question
        start = 0
        end = len(final_questions)
        random_value = random.randint(start, end - 1)
        return jsonify({
            "question": final_questions[random_value].format(),
            "success": True
        })

    '''
  @DONE:
  Create error handlers for all expected errors
  including 404 and 422.
  '''
    # Error Handler for HTTP Satus Code 400 => Bad Request
    @app.errorhandler(400)
    def error_handler_bad_request(error):
        return jsonify({
            "error": 400,
            "success": False,
            "message": "bad request"
        }), 400

    # Error Handler for HTTP Status Code 404 => Resource Not Found
    @app.errorhandler(404)
    def error_handler_resource_not_found(error):
        return jsonify({
            "error": 404,
            "success": False,
            "message": "resource not found"
        }), 404

    # Error Handler for HTTP Status Code 422 => Unprocessable
    @app.errorhandler(422)
    def error_handler_unprocessable(error):
        return jsonify({
            "error": 422,
            "success": False,
            "message": "unprocessable request"
        }), 422

    # Error Handler for HTTP Status Code 500 => Server Error
    @app.errorhandler(500)
    def error_handler_server_error(error):
        return jsonify({
            "error": 500,
            "success": False,
            "message": "server error"
        }), 500

    return app
