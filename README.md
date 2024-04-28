# :honeybee: Flask-Spellingbee :honeybee:
### *A wordbuilder web application game modeling the New York Times Spellingbee*
### Deployed at : https://flask-spellingbee.onrender.com
#### Springboard SEC Capstone #1 by Michael Ellis

## :honeybee: About :honeybee:
Welcome to Flask Spellingbee! Flask Spellingbee is a webgame application modeled after the New York Times word building game SpellingBee! 
**The goal of the game is to simply build as many words as possible from a pool/hive of 7 letters. The center letter in the hive must always be used. Letters can be used more than once. Words must be 4 letters at minimum in length. The more words you make the higher your score and rank! Signup with a username, password, and avatar and start playing!**

## :honeybee: Instructions/User Flow :honeybee:

Using the application is simple! Head over to https://flask-spellingbee.onrender.com to play the current deployment of the game! Make an account with a username, password, and image url/avatar and signin/signup. On the following page, choose the start a fresh board button and then begin playing! You'll be redirected to the game UI page. See a Sample image of the game ui below! The user can then start submitting their words via the guessform. 

*Some valid words for the hive/board below would be "cool" "roll" "yell" "yelled" for example*

(![SpellingbeeUISN](https://github.com/MichaelAEllis86/SpellingBee/assets/118708666/97fc454e-9d6e-4311-8610-cf0ae0d01318)


## :honeybee: Current Features :honeybee:

- **Random Game Generation:** Make and play new games/hives at will through random generation of letter pools/hives! Every game is unique!
- **Game Saves:** Save your game at anytime from the gameboard! Games are also saved automatically upon logout, starting a new game or replaying a previous game!
- **Replays:** Access and replay your previous games from the user hub to increase your score. You can replay a game at anytime!
- **Game/User Stats** From the user hub access a chart of statistics for each game you play such as the amount of words you found, words remaining, rank, score, pangrams and more! Also get user stats such as the number of puzzles a user has played in total, and the total number of words made in total.
- **Dynamic hints and spoilers:** Each game/hive has its own set hints and spoilers based upon its unique letter pool!
- **Rules and Glossary:** The hints page provides a more detailed set of game rules and a glossary of terms for more info about the game
- **Merriam Webster Dictionary Search:** Use the dictionary search bar on the game page to check spellings, definitions, and pronounciation of words without any need to tab elsewhere. Think of this as a secondary tool for your game wordbuilding!
- **User Accounts and authentication:** Make, edit, and delete basic user accounts. We only do this so the stats have a person they're associated with. No email, or any other personal info is collected.

### API/Dictionary Integration https://dictionaryapi.com/products/api-collegiate-dictionary

## :honeybee: Features Under Construction :honeybee:
- **Unique scoring implementation for pangrams and perfect pangrams:** Pangrams are special words that use every letter in the hive! Perfect panagrams use each letter EXACTLY ONCE. As these words are unique and deserving of special distinction they also deserve special scoring! Currently updating the scoring system to account for pangram and perfect pangram scoring to reflect the rarity of these words.
- **Click hive integration:** working on updating the game hive ui so that clicking a letter/honeycomb will also enter that letter into the guess in addition to normal typing.

## :honeybee: Construction & Requirments :honeybee:





