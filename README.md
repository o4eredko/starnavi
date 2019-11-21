# Starnavi Test Task
It is a REST API, that could be used for the blog web site

### Installation
Prerequisites:
* python3
* pip3
* virtualenv

If you don't have it installed on your computer, here is the instruction to install these packages in **Ubuntu 18.04.03 LTS**.
```
sudo apt-get install python3
sudo apt-get install python3-pip
pip3 install virtualenv
```
Then you need to install project requirements.
```
cd <project directory>
python3 -m virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 manage.py makemigrations blog
python3 manage.py migrate
```
That's all. Now you need to run the server
```
python3 manage.py runserver <port>
You can leave <port> blank, if you want it to be default (8000)
```
### Testing
To ensure that everything is working well, you can run command
```
python3 manage.py test
```
### Api Endpoints
```
<domain>/api/users/
GET:
    show all users that already exist in database
    return: json with list of all users

<domain>/api/users/<id>/
GET:
    show the information about one specific user
    return:
        success: 200 status code and json with fields (url, id, username, posts)
        error: 404 status code

<domain>/api/account/register/
POST:
    create new user
    fields: username, email, password, password2
    return:
        success: 201 status code and json with fields (username, email)
        error: 400 status code and json in format field: error_message

<domain>/api/account/token/
POST:
    log in to get the authorization token and the refresh token
    fields: username, password
    return:
        success: 200 status code and json with fields (refresh, access)
        error: 400 status code and json with error message

<domain>/api/account/refresh/
POST:
    refresh the access token
    fields: refresh
    return:
        success: 200 status code and json with fields (access)
        error: 400 status code and json with error message

<domain>/api/posts/
GET:
    show list of all posts
    return:
        success: 200 status code and json with fields (count, next, previous, results)
            count is the number of all posts 
            results is an array with information about first ten posts inside it
            next, previous are the pagination url's to get next/previous 10 posts
POST:
    create new post.
    !you have to be authorized with token, received from url <domain>/api/account/token/.
    fields: title, content
    return:
        success: 201 status code and json with fields (url, id, title, content, created, author, author_username, total_likes, is_fan)
        error: 400 status code and json with error message

<domain>/api/posts/<id>/
GET:
    show the information about one specific user
    return:
        success: 200 status code and json with fields (url, id, title, content, created, author, author_username, total_likes, is_fan)
        error: 404 status code
PUT:
    update the post's information.
    !you have to be authorized with token, received from url <domain>/api/account/token/.
    fields: title, content
    return:
        success: 200 status code and json with fields (url, id, title, content, created, author, author_username, total_likes, is_fan)
        error: 400 status code and json with error message
DELETE:
    delete post.
    !you have to be authorized with token, received from url <domain>/api/account/token/.
    return:
        success: 204 status code
        error: 404 status code
```
