import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for
    expected errors.
    """

    def test_get_categories(self):
        response = self.client().get('/categories')
        # print(response.data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data['categories']))
        self.assertEqual(data["success"], True)

    def test_get_questions(self):
        response = self.client().get('/questions?page=1')
        # print(response.data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["questions"])
        self.assertTrue(data["totalQuestions"])
        self.assertTrue(data["categories"])
        self.assertEqual(data["success"], True)

    def test_delete_question_success(self):
        response = self.client().delete('/questions/9999')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["message"])

    def test_delete_question_fail(self):
        response = self.client().delete('/questions/1')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_search_questions_success(self):
        response = self.client().post('/questions/search',
                                      json={'searchTerm': 'which'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["totalQuestions"])
        self.assertEqual(data["success"], True)

    def test_search_questions_fail(self):
        response = self.client().post('/questions/search')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable request")

    def test_play_trivia_game_success(self):
        response = self.client().post(
            '/quizzes',
            json={
                'previous_questions': [],
                'quiz_category': {
                    'type': 'click',
                    'id': '3'}})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])

    def test_play_trivia_game_fail(self):
        response = self.client().post(
            '/quizzes', json={'previous_questions': []})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable request")

    def test_create_new_question_success(self):
        new_question = {
            'question': 'In which year did the World War II start end?',
            'answer': '1945',
            'difficulty': 4,
            'category': '3'
        }
        response = self.client().post('/questions', json=new_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["message"])

    def test_create_new_question_failed(self):
        new_question = {
            'question': 'In which year did the World War II start end?',
        }
        response = self.client().post('/questions', json=new_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"])

    def test_get_questions_by_category_success(self):
        response = self.client().get("/categories/3/questions")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["questions"])
        self.assertTrue(data["totalQuestions"])
        self.assertEqual(data["success"], True)
        self.assertEqual(data["currentCategory"], Category.query.get(3).type)

    def test_get_questions_by_category_fail(self):
        response = self.client().get("/categories/9999999/questions")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
