# Full Stack Trivia API Project
This project is a game where users can test their knowledge answering trivia questions. The task for the project was to create an API and test suite for implementing the following functionality:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

## Getting Started

### Installing Dependencies
Developers using this project should already have Python3, pip, node, and npm installed.

#### Frontend Dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

#### Backend Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

## Running the Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```

## Running the Server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
Omit the dropdb command the first time you run tests.

## API Reference

### Getting Started

* Base URL: Currently this application is only hosted locally. The backend is hosted at `http://127.0.0.1:5000/`
* Authentication: This version does not require authentication or API keys.

### Error Handling

Errors are returned as JSON in the following format:<br>

    {
        "success": False,
        "error": 404,
        "message": "resource not found"
    }

The API will return three types of errors:

* 400 – bad request
* 404 – resource not found
* 422 – unprocessable

### Endpoints

#### GET `/categories`
- Retrieves a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- *Request Arguments: None
- *Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}


#### GET `/questions?page=1`
- Retrieves a dictionary of questions from all categories which are paginated on the number of questions per page
- *Request Arguments: *(page:int) which is not mandatory(optional)
- *Returns :* ```
{
    "categories": {
        "3": "Sports",
        "7": "History",
        "9": "art",
        "10": "entertainment",
        "11": "geography",
        "12": "science"
    },
    "currentCategory": null,
    "questions": [
        {
            "answer": "Albert Einstein",
            "category": "12",
            "difficulty": 3,
            "id": 9,
            "question": "Who wrote about theory of relativity"
        },
        {
            "answer": "1945",
            "category": "7",
            "difficulty": 4,
            "id": 20,
            "question": "In which year did the World War II  end"
        }
    ],
    "success": true,
    "totalQuestions": 2
}```

#### POST `/questions`
Adds a new question to the database
- *Request body:* {question:string, answer:string, difficulty:int, category:string}
- *Example response:* 
```
{
  "message":"Created question with the id 10 ",
  "success": true
}
```

#### DELETE `/questions/<question_id>`
Delete an existing question from the database
- *Request arguments:* question_id:int (mandatory)
- *Example response:* 
```
{
  "message": "Success deleted question with 10", 
  "success": true
}
```

#### GET `/categories/<int:category_id>/questions`
Retrieves a dictionary of questions of the specified category_id
- *Request argument:* category_id:int(mandatory)
- *Example response:*
```
{
    "currentCategory": "History",
    "questions": [
        {
            "answer": "1945",
            "category": "7",
            "difficulty": 4,
            "id": 20,
            "question": "In which year did the World War II  end"
        }
    ],
    "success": true,
    "totalQuestions": 1
}
}
```
#### POST `/questions/search`
Retrieves all questions where a substring matches the substring in the question(case insensitive)
- *Request body:* {searchTerm:string}
- *Example response:*
```
{
    "currentCatgeory": null,
    "questions": [
        {
            "answer": "Albert Einstein",
            "category": "12",
            "difficulty": 3,
            "id": 9,
            "question": "Who wrote about theory of relativity"
        }
    ],
    "success": true,
    "totalQuestions": 1
}
```
#### POST `/quizzes`
Retrives one random question from a specified category by excluding the previous questions. 
- *Request body:* {previous_questions: arr[], quiz_category: {id:int, type:string}}
- *Example response*: 
```
{
    "question": {
        "answer": "1945",
        "category": "7",
        "difficulty": 4,
        "id": 20,
        "question": "In which year did the World War II end"
    },
    "success": true
}
```