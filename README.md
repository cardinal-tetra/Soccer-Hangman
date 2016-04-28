## Soccer Hangman

### Setting Up
1. Update the value of application in app.yaml with the App ID you registered in the App Engine admin console that you want to use to host this application.
2. Open up the GoogleAppEngineLauncher program and choose 'add existing application', specify the directory containing your application code, as well the ports you want for the application interface and the admin interface.
3. Select 'run' which allows you to test your application on the relevant port you specified for localhost, add '_ah/api/explorer' to the URL to test the endpoints.
4. You can also select 'deploy' which will allow you to test the endpoints at the URL: {App_ID}.appspot.com/_ah/api/explorer

### Game Description
Soccer Hangman allows users to play the classic guessing game 'hangman' in the realm of famous soccer players. By making calls to relevant endpoints, users register themselves, and use their username to create games. The user then makes calls to the `make_move` endpoint using the `urlsafe_game_key` to guess the answer either by guessing the whole word, or by specifying single letters. Upon winning the game or losing it by running out of guesses, a score will be saved for that game. Users can play other games without finishing the initial one, can retrieve information about their scores, active games, and rankings by making calls to the appropriate endpoints.

### Files Included
- api.py: contains endpoints and most of the logic running the hangman game.
- app.yaml: app configuration.
- models.py: entity (sometimes accompanied by helper functions) and message definitions.
- helpers.py: contains function for retrieving entities by `urlsafe_game_key` and functions with additional game logic.

### Endpoints Included
- **create_user**
 - Path: 'user'
 - Method: POST
 - Parameters: username, email(optional)
 - Returns: message confirming creation of user
 - Description: Create a unique user by specifying the username; a registered user must be specified in order to create and play games.

- **new_game**
 - Path: 'game'
 - Method: POST
 - Parameters: username
 - Returns: GameForm with initial game state
 - Description: Create a new game by specifying the username of a registered user.
 
- **get_game**
 - Path: 'game/{urlsafe_game_key}'
 - Method: GET
 - Parameters: urlsafe_game_key
 - Returns: GameForm with current game state
 - Description: Allows access to information for a game corresponding to the urlsafe_game_key.
 
- **make_move**
 - Path: 'game/{urlsafe_game_key}'
 - Method: PUT
 - Parameters: urlsafe_game_key, guess
 - Returns: GameForm with game state after guess has been processed
 - Description: Allows user to specify the game using the `urlsafe_game_key` and the guess they want to make for it. The guess can be a letter or an entire word, and endpoint will return errors if malformed guesses are made or relevant game does not exist or has ended.
 
- **get_user_scores**
 - Path: 'scores/{username}'
 - Method: GET
 - Parameters: username
 - Returns: ScoreForms containing information about games the user completed
 - Description: Every time a user completes a game, a score entity is saved for that game with information about number of guesses, and whether the user won. This function retrieves all the scores for the user specified.

- **get_user_games**
 - Path: 'games/{username}
 - Method: GET
 - Parameters: username
 - Returns: GameForms showing the current game states for active games registered under the username specified.
 - Description: Allows user to retrieve game information (key, guesses made) about their active games.
 
- **cancel_game**
 - Path: 'cancel/game'
 - Method: POST
 - Parameters: urlsafe_game_key
 - Returns: Message string telling user that the game has been successfully cancelled.
 - Description: By specifying the `urlsafe_game_key`, user can cancel an active game which will be deleted from Datastore.
 
- **get_high_scores**
 - Path: 'scores/highscores'
 - Method: POST
 - Parameters: number_of_results (optional)
 - Returns: message strings displaying high scores
 - Description: Allows user to retrieve a list of high scores, which is essentially a record of games won and ordered by number of guesses made (the fewer the better); user can also pass in optional `number_of_results` parameter to limit results returned. Note that we use the POST method because using the GET method would make it mandatory for the user to specify `number_of_results`.
 
- **get_user_rankings**
 - Path: 'user/rankings'
 - Method: POST
 - Parameters: number_of_results (optional)
 - Returns: message strings displaying username and performance stats.
 - Description: Allows user to retrieve a list of users who have completed games, ranked according to their performance statistics (like win ratio and average guesses per game). As before, user can also pass in optional `number_of_results` parameter to limit results returned. Note that we use the POST method because using the GET method would make it mandatory for the user to specify `number_of_results`.
 
- **get_game_history**
 - Path: 'game/history/{urlsafe_game_key}'
 - Method: GET
 - Parameters: urlsafe_game_key
 - Returns: message strings displaying a record of historical guesses and results for game specified under `urlsafe_game_key`
 - Description: user can see a record of all historical guesses, results, and progress relating to the game specified under the `urlsafe_game_key`
