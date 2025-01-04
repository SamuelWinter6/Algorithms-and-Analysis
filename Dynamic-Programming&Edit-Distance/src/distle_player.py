from edit_dist_utils import *
import random

class DistlePlayer:
    '''
    AI Distle Player! Contains all of the logic to automagically play
    the game of Distle with frightening accuracy (hopefully)
    '''
    
    def start_new_game(self, dictionary: set[str], max_guesses: int) -> None:
        '''
        Called at the start of every new game of Distle, and parameterized by
        the dictionary composing all possible words that can be used as guesses,
        only ONE of which is the correct Secret word that your agent must
        deduce through repeated guesses and feedback.
        
        [!] Should initialize any attributes that are needed to play the
        game, e.g., by saving a copy of the dictionary, etc.
        
        Parameters:
            dictionary (set[str]):
                The dictionary of words from which the correct answer AND any
                possible guesses must be drawn
            max_guesses (int):
                The maximum number of guesses that are available to the agent
                in this game of Distle
        '''
        # [!] TODO
        self.dictionary = dictionary  # Stores a copy of the dictionary
        self.max_guesses = max_guesses  # Sets the maximum number of guesses allowed
        self.guesses_made = 0  # Resets the guess counter for the new game
        self.potential_guesses = list(dictionary)  # Initializes potential guesses with the whole dictionary
        self.last_guess = ""  # Resets the last guess made
        self.all_guesses: list[str] = []  # Initializes the list to track all guesses made

        return
    
    def make_guess(self) -> str:
        '''
        Requests a new guess to be made by the agent in the current game of Distle.
        Uses only the DistlePlayer's attributes that had been originally initialized
        in the start_new_game method.
        
        [!] You will never call this method yourself, it will be called for you by
        the DistleGame that is running.
        
        Returns:
            str:
                The next guessed word from this DistlePlayer
        '''
        # [!] TODO

        if self.guesses_made < self.max_guesses:
            # Filter out any previously guessed words
            possible_guesses = [word for word in self.potential_guesses if word not in self.all_guesses]
            if possible_guesses:
                guess = random.choice(possible_guesses)
            else:
                guess = None

            if guess:
                self.last_guess = guess
                self.all_guesses.append(guess)
                self.guesses_made += 1
                return guess
    
        return ''
    
    def get_feedback(self, guess: str, edit_distance: int, transforms: list[str]) -> None:
        '''
        Called by the DistleGame after the DistlePlayer has made an incorrect guess.
        The feedback furnished is described in the parameters below. Your agent will
        use this feedback in an attempt to rule out as many remaining possible guess
        words as it can, through which it can then make better guesses in make_guess.
        
        [!] You will never call this method yourself, it will be called for you by
        the DistleGame that is running.
        
        Parameters:
            guess (str):
                The last, incorrect guess made by this DistlePlayer
            edit_distance (int):
                The numerical edit distance between the guess your agent made and the
                secret word
            transforms (list[str]):
                The list of top-down transforms needed to turn the guess word into the
                secret word, i.e., the transforms that would be returned by your
                get_transformation_list(guess, secret_word)
        '''
        # [!] TODO

        matching_transforms = []
        len_count = len(guess)
        
        # Adjust based on transformations
        for letter in transforms:
            if letter == 'I':
                # Each 'I' means the secret word has one more character
                len_count += 1
            elif letter == 'D':
                # If 'D' is interpreted as removing from the guess
                len_count -= 1

        true_secret_length = len_count

        # Filter 1 potential guesses by this adjusted length estimate
        self.potential_guesses = [word for word in self.potential_guesses if len(word) == true_secret_length]

        for word in self.potential_guesses:
            if get_transformation_list(guess, word) == transforms:
                matching_transforms.append(word)

        # Filter len of guess & prioritize Transforms within guesses
        self.potential_guesses = matching_transforms