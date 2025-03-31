# Educational Web Application

## Project Overview
An educational web application designed as a series of engaging games that help users gain new knowledge and compete with each other, fostering connections among people with shared interests. The platform offers real-time multiplayer gameplay, where users can register as Players, Administrators, or Moderators, or join as Guests without registration.
Players can challenge each other in five different game modes, testing their skills in math, trivia, word puzzles, and logical matching. With built-in profile management and real-time matchmaking, the app creates an interactive and competitive environment that makes learning both fun and dynamic.

## Architecture
The system follows a three-layer architecture:
- **Client Layer:** For guests, users, moderators, and administrators, built with HTML5, CSS, and JavaScript.
- **Server Layer:** Manages data and information exchange, developed using Django.
- **Data Storage Layer:** Uses MySQL for efficient and scalable storage.

## Technologies Used
- **Frontend:** HTML5, CSS, JavaScript
- **Backend:** Django
- **Database:** MySQL

## Features
- **User Roles:** Register and log in as a Player, Administrator, or Moderator, or play as a Guest
- **Profile Management:** View and manage user profiles
- **Matchmaking:** Start a match,find opponents and compete against real players in real time
- **Gameplay:** Compete in five different challenges:
  - Use basic math operations and given numbers to get as close as possible to the target number
  - Answer trivia questions as quickly as possible
  - Find the required five-letter word
  - Match terms from the left column with corresponding terms from the right column
  - Play the classic word-guessing game by guessing the letters of a hidden word before the hangman is completed
