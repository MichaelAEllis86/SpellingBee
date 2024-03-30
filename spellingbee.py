import random
# from random import choice
import string

#----rules of Spellingbee---- Spellingbee is a word making game where the user makes words from a pool of letters.Think Scrabble but without the board.
# 1. Overview: generate 7 letters and put them on the board, and the user constructs/makes as many words as possible from the pool of 7 letters.
#------valid words-----#
# 2. Letters can be used more than once
# 3. One central (center of letter hive) or special letter is selected from the pool of 7. It must be played be the used in the making of each word played or the word is invalid.
# 4. Each word must have at minimum 4 letters. 
# 3. we are assuming each board should contain one vowel letter, 
#4no letter s due to abusing plural words
# 4. points are assigned based on the length of the word, 1 point per letter

class SpellingBee():
    def __init__(self):

        self.words = self.read_dict("words.txt")
        self.no_s_words=self.subtract_s_words(self.words)
        self.score=0
        self.guessed_words=[]
        self.vowels=self.pick_vowels()
        self.consonants=self.pick_consonants()
        self.letters=self.generate_letters()
        self.center_letter=self.select_center_letter()
        self.all_valid_words=self.get_all_valid_words()
        self.total_points=self.get_total_points()
        self.pangrams=self.find_all_pangrams()
        

    def read_dict(self, dict_path):
        """Read and return all words in dictionary."""

        dict_file = open(dict_path)
        words = [w.strip() for w in dict_file]
        # lowercase_words=[word for ]
        dict_file.close()
        return words
    
    def subtract_s_words(self,word_list):
        no_s_word_list=[word for word in word_list if "s" not in word]
        return no_s_word_list
    
    # need to change this! per the spellingbee rules a word with a length of 4 has a score of 1, and each additional letter adds 1 point. right now score is just length of the word
    def add_score (self,valid_word):
        """adds a point value to score on an instance of SpellingBee game.
        a word's point value is equal to it's length! increment the score by that amount"""
        point_value=len(valid_word)
        self.score+=point_value

    # need to adjust pick vowels, pick consonants and generate letters to disallow duplicate letters!DONE!!!!
    # seems like in the real spellingbee there is always at least two vowels we might decide to adjust this to pick always between 2 and 3 vowels rather than just 1. This improves the game's flow by making words easier to form
        
    def pick_vowels(self):
        """Picks a random amount of vowels for the game's letter pool.
            First picks a random number of vowels between 1 and 3
            then we chose that number of vowels to add to the game's letter pool and returns vowel string. 
            Duplicate vowels are disallowed via set conversion (as in the letter "e" cannot appear as one of the vowels twice)"""
        all_vowels="aeiou"
        number_of_vowels=random.randint(2, 3)
        chosen_vowels=[random.choice(all_vowels) for num in range(number_of_vowels)]
        deduped_chosen_vowels=set(chosen_vowels)
        string_chosen_vowels="".join(deduped_chosen_vowels)
        return string_chosen_vowels
    
    def pick_consonants(self):
        """Picks a set of randoms consonants to go with the vowels generated via function pick_vowels() also found on this class.
        Picks as many random cosonants as is needed to fill the letter pool to 7 Depending on the amount of vowels we generated. The letter "S" is not included as per game rules.
        Duplicate consonants are not allowed and are checked via conversions into sets before converting back into a final string of consonants.
        
        Furthermore, if a duplicate consonant is found and subtracted via set conversion, we provide conditional logic that will refill the letter pool to 7 if necessary.
        The refill pulls from a new pool of consonants "usused_consonants" that does not include the letters we've already selected.
        
        """
        all_consonants="bcdfghjklmnpqrtvwyxz"
        all_cosonants_set=set(all_consonants)
        number_of_consonants=7-len(self.vowels)
        chosen_consonants=[random.choice(all_consonants) for num in range(number_of_consonants)]
        deduped_chosen_consonants=set(chosen_consonants)
        unused_consonants=list(all_cosonants_set - deduped_chosen_consonants)
        if len(deduped_chosen_consonants) < number_of_consonants:
            remaining_letters_togo=number_of_consonants-len(deduped_chosen_consonants)
            replacement_consonants=([random.choice(unused_consonants) for num in range(remaining_letters_togo)])
            replacement_consonants_set=set(replacement_consonants)
            consonants_union=replacement_consonants_set | deduped_chosen_consonants
            string_replacement_consonants="".join(consonants_union)
            return string_replacement_consonants
        else:
            string_chosen_consonants="".join(chosen_consonants)
        return string_chosen_consonants

            # adding conditional here! by pulling dups out of our consonants we may no longer have enough letters
            # if that's the case we need to add more letters that have not been used already so that we have 7 letters total with vowels and consonants
        
    
    def generate_letters(self):
        """ Joins together the selected pools of vowels and consonants to generate a unified pool of 7 letters for the game"""
        game_letters=self.vowels + self.consonants
        randomized_game_letter_list=random.sample(game_letters,7)
        randomized_game_letters="".join(randomized_game_letter_list)
        return randomized_game_letters
    
    def select_center_letter(self):
        chosen_letter=random.choice(self.letters)
        return chosen_letter
    
    #need to add functionality to not allow duplicate words! Done
    def validate_word(self,wordguess):
        """ This Function validates a wordguess from the user, gives feedback, updates scoring"""
        
        length_check=len(wordguess) >= 4
        # print(f"the length check is {length_check}")

        central_letter_check=self.center_letter in wordguess
        # print(f"the center letter check is {central_letter_check}")

        word_exists_check=wordguess in self.all_valid_words
        # print(f"the word exists check is {word_exists_check}")
        
        letter_check_results=all([letter in self.letters for letter in wordguess])
        # print(f"letter_check_results are {letter_check_results}")

        already_guessed_check=wordguess in self.guessed_words
        # print(f"already_guessed_check results are {already_guessed_check}")

        if length_check== False:
            result="too short"
            return result
        elif already_guessed_check== True:
            result="already guessed"
            return result
        elif length_check==True and central_letter_check==False:
            result="missing center letter"
            return result
        elif length_check==True and central_letter_check==True and word_exists_check==False:
            result="not a word"
            return result
        elif length_check==True and central_letter_check==True and word_exists_check==True and letter_check_results==False:
            result="bad letters"
            return result
        else:
            result="valid"
            self.add_score(wordguess)
            self.guessed_words.append(wordguess)
            # self.rating=self.evaluate_rating() line was causing bug
            return result
    
    def validate_word_v2(self,wordguess,letters,center_letter,valid_word_list,guessed_words):
        """ This Function validates a wordguess from the user, gives feedback, updates scoring"""
        
        length_check=len(wordguess) >= 4
        # print(f"the length check is {length_check}")

        central_letter_check=center_letter in wordguess
        # print(f"the center letter check is {central_letter_check}")

        word_exists_check=wordguess in valid_word_list
        # print(f"the word exists check is {word_exists_check}")
        
        letter_check_results=all([letter in letters for letter in wordguess])
        # print(f"letter_check_results are {letter_check_results}")

        already_guessed_check=wordguess in guessed_words
        # print(f"already_guessed_check results are {already_guessed_check}")

        if length_check== False:
            result="too short"
            return result
        elif already_guessed_check== True:
            result="already guessed"
            return result
        elif length_check==True and central_letter_check==False:
            result="missing center letter"
            return result
        elif length_check==True and central_letter_check==True and word_exists_check==False:
            result="not a word"
            return result
        elif length_check==True and central_letter_check==True and word_exists_check==True and letter_check_results==False:
            result="bad letters"
            return result
        else:
            result="valid"
            self.add_score(wordguess)
            self.guessed_words.append(wordguess)
            # self.rating=self.evaluate_rating() line was causing bug
            return result
    
    def validate_words_initial(self,wordguess):
        """Special function only used to determine the total pool of valid words possible. Does not update the score, or guessed_words or other properties"""
        length_check=len(wordguess) >= 4
        # print(f"the length check is {length_check}")

        central_letter_check=self.center_letter in wordguess
        # print(f"the center letter check is {central_letter_check}")

        word_exists_check=wordguess in self.no_s_words
        # print(f"the word exists check is {word_exists_check}")
        
        letter_check_results=all([letter in self.letters for letter in wordguess])
        # print(f"letter_check_results are {letter_check_results}")

        if length_check== False:
            result="too short"
            return result
        elif length_check==True and central_letter_check==False:
            result="missing center letter"
            return result
        elif length_check==True and central_letter_check==True and word_exists_check==False:
            result="not a word"
            return result
        elif length_check==True and central_letter_check==True and word_exists_check==True and letter_check_results==False:
            result="bad letters"
            return result
        else:
            result="valid"
            return result
    
    def get_all_valid_words(self):
       all_valid_words=[ word for word in self.no_s_words if self.validate_words_initial(word)=="valid"]
       return all_valid_words
    
    def get_total_points(self):
        total=0
        for word in self.all_valid_words:
            total+=len(word)
        return total
    
    # def evaluate_rating(self):
    #     """Function relating the percentage of words a player has found to a a game rating or  """
    #     percentage_score=num_of_points/total_num_points
    #     if percentage_score >= 0.9:
    #         rating="Genius"
    #         return rating
    #     elif percentage_score < 0.9 and percentage_score >=0.8:
    #         rating="Amazing"
    #         return rating
    #     elif percentage_score <0.8 and percentage_score >=0.7:
    #         rating="Great"
    #         return rating
    #     elif percentage_score < 0.7 and percentage_score >=0.6:
    #         rating="Nice"
    #         return rating
    #     elif percentage_score < 0.6 and percentage_score >=0.5:
    #         rating="Solid"
    #         return rating
    #     elif percentage_score < 0.5 and percentage_score >=0.4:
    #         rating="Good"
    #         return rating
    #     elif percentage_score < 0.4 and percentage_score >=0.3:
    #         rating="moving up"
    #         return rating
    #     elif percentage_score < 0.3 and percentage_score >=0.2:
    #         rating="Good start"
    #         return rating
    #     else:
    #         rating="Beginner"
    #         return rating
               
    def check_guess_for_pangram(self, wordguess):
        """Checks for a pangram! A pangram a word that uses each letter on the board!
        Ex. given board='aglerin'  one pangram on this board could be pangram='learning'!
        Each letter can must be used at least once for the word to be a valid pangram, but a word be used more than once if needed!!!
        This version uses properties on the instance to check a pangram """
        
        valid_word_check=self.validate_words_initial(wordguess)=="valid"
        all_letters_used_check=len(set(wordguess))==7

        if valid_word_check and all_letters_used_check == True:
            return True
        else:
            return False
    
    def check_guess_for_pangram_v2(self,wordguess,letters,center_letter,valid_word_list,guessed_words):

        """Checks for a pangram! A pangram a word that uses each letter on the board!
        Ex. given board='aglerin'  one pangram on this board could be pangram='learning'!
        Each letter can must be used at least once for the word to be a valid pangram, but a word be used more than once if needed!!!
        This Version of the function uses external parameters outside of the context of the self/instance to check for a pangram """
           
        valid_word_check=self.validate_word_v2(wordguess,letters,center_letter,valid_word_list,guessed_words)=="valid"
        all_letters_used_check=len(set(wordguess))==7

        if valid_word_check and all_letters_used_check == True:
            return True
        else:
            return False
    
    def find_all_pangrams(self):
        pangrams=[word for word in self.all_valid_words if self.check_guess_for_pangram(word)]
        return pangrams
    
        
       
    # def generate_letters(self):
    #     all_letters="abcdefghijklmnopqrstuvwxyz"
    #     pick_vowel=choice
    