## Soccer Hangman

Soccer Hangman allows users to play a variant of that classic guessing game in the realm of famous soccer players. By making calls to relevant endpoints, users register themselves, and will receive a `urlsafe_game_key` upon creating a game. The user then makes calls to the `make_move` endpoint using the `urlsafe_game_key` to guess the answer either by specifying the whole word, or a single letter. Each attempt consumes one of the six guesses that users have upon beginning the game. Upon winning the game or losing it by running out of guesses, a score (detailing the number of guesses made and final result) will be saved for that game. Users can create and play multiple games simultaneously, and can retrieve information about their scores, active games, and rankings by making calls to the appropriate endpoints.

Now a spoiler, the answer will be one of these players: Ronaldo, Messi, Bale, Rooney, Suarez, Fabregas, Cech, Sanchez, Aguero, Hazard, Benzema, and Neymar.

### Files
- `api.py` : defines endpoints and contains most of the game logic.
- `models.py` : contains entity and message class definitions.
- `helpers.py` : contains function for retrieving entities by `urlsafe_game_key` and functions with additional game logic.
- `app.yaml` : application configuration.
- `cron.yaml` : cron job configuration.

### Endpoints
- **create_user**
 - Path: 'user'
 - Method: POST
 - Parameters: username, email (optional)
 - Returns: Message confirming creation of user
 - Description: Create a unique user by specifying the username; a registered user is required to create and play games.

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
 - Description: Access information for a game corresponding to the urlsafe_game_key.
 
- **make_move**
 - Path: 'game/{urlsafe_game_key}'
 - Method: PUT
 - Parameters: urlsafe_game_key, guess
 - Returns: GameForm with game state after guess has been processed
 - Description: Allows user to specify the game using the `urlsafe_game_key` and the guess they want to make for it. The guess can be a letter or an entire word. Errors will be returned if malformed guesses are made or relevant game does not exist or has ended.
 
- **get_user_scores**
 - Path: 'scores/{username}'
 - Method: GET
 - Parameters: username
 - Returns: ScoreForms containing information about games the user completed
 - Description: Every time a user completes a game, a score entity is saved for that game with information about the number of guesses and outcome. This function retrieves all the scores for the user specified.

- **get_user_games**
 - Path: 'games/{username}
 - Method: GET
 - Parameters: username
 - Returns: GameForms displaying information for active games registered under the username specified.
 - Description: Allows user to retrieve a list of their active games with information such as urlsafe_game_key and game state.
 
- **cancel_game**
 - Path: 'cancel/game'
 - Method: POST
 - Parameters: urlsafe_game_key
 - Returns: Message string telling user that the game has been successfully cancelled.
 - Description: By specifying the `urlsafe_game_key`, user can cancel an active game which will be deleted from Datastore.
 
- **get_high_scores**
 - Path: 'scores/highscores'
 - Method: GET
 - Parameters: number_of_results
 - Returns: Message strings displaying high scores
 - Description: Retrieve a list of games won by users, ordered according to guesses made (the fewer the better).
 
- **get_user_rankings**
 - Path: 'user/rankings'
 - Method: GET
 - Parameters: number_of_results
 - Returns: Message strings displaying users ranked by performance stats.
 - Description: Retrieve a list of users who have completed games, ranked according to their performance statistics (like win ratio and average guesses per game). As before, user passes in `number_of_results` parameter to specify a limit on how many results they want returned.
 
- **get_game_history**
 - Path: 'game/history/{urlsafe_game_key}'
 - Method: GET
 - Parameters: urlsafe_game_key
 - Returns: Message strings displaying a record game states for the game corresponding to `urlsafe_game_key`
 - Description: Returns a record of all historical guesses, results, and progress relating to the game specified under the `urlsafe_game_key`
