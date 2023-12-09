
# CS50Web Final Project (Mood Sync AI)

The project video is https://youtu.be/keHEdq3F18A.

## Description

This project uses OpenAI's API to generate Spotify music based on the users' current feeling. The inspiration comes from my personal situation where I cannot think of the best music that aligns with my current feeling. Using Django backend and Javascript and React as frontend, this website allows user to create their own playlist by searching music align with their feeling.

## Distinctiveness and Complexity

Without a doubt, this website is not similar to any of the projects we have created in CS50web as this is neither a social app or e-commerce. Utilizing the amazing featues of APIs, this project's complexity lies in its uniqueness of combining already exisiting APIs to create something that is useful. The main features of the project includes:

- Register/ Log-in/ Log-out features
- Prompt the feeling, music genre, artist and current situation
- Search the spotify music name and artist using chatgpt 3.5 turbo version
- Generate the spotify track lists based on the result of GPT APIs
- Include embed track features that can be easily played in any browser
- Add any music to your playlist database


## How the project works and different files

### Backend
Django handles all the APIs request and updating the databases

### Fntend
For the front end, javascript and react handles most of the page listing especially dynamically updating the playlist databases without reloading the page.

## How to run the application
- You will need a spotify account during the log-in state
- Make and apply migrations by running python manage.py makemigrations and python manage.py migrate


