import random
from asl_detector_module import ASLDetector

# dictionaries for hangman categories and guessable words
categories = {
    "Capital Cities": ["JAKARTA", "AMSTERDAM", "CARACAS", "CAPETOWN", "COLOMBO", "PARIS", "SEOUL", "TOKYO", "JERUSALEM", "DUBLIN"],
    "Animals": ["SHEEP", "DOG", "CAT", "HORSE", "LION", "TIGER", "SNAKE", "CAPYBARA", "WOLF", "AXOLOTL"],
    "Fruits": ["LEMON", "APPLE", "PINEAPPLE", "CHERRY", "KIWI", "BANANA", "STRAWBERRY", "MANGO", "GUAVA", "GRAPES"]
}

# randomly choose a category and word
chosen_category = random.choice(list(categories.keys()))
chosen_word = random.choice(categories[chosen_category]).upper()

# set variables
# this one prints blank spaces so the user knows the length of the hidden word
guessed_word = ['_'] * len(chosen_word)
# will update the blank spaces whenever the user guesses
word_display = ' '.join(guessed_word)
# maximum amount of incorrect guesses the user may have
max_guesses = 5
# counter that will increase every time the user has an incorrect guess
counter = 0
# empty list that will be updated whenever the user guesses a letter
guessed_letters = []
# calling the ASL detector module from the external file
asl_detector = ASLDetector(model="C:\\Users\\almir\\Desktop\\final project algopro\\1\\Model\\keras_model.h5",
                           labels="C:\\Users\\almir\\Desktop\\final project algopro\\1\\Model\\labels.txt")


# while loop to make sure that the game keeps running as long as there are blank spaces and the user has enough incorrect guesses to use
while '_' in guessed_word and counter < max_guesses:
    # printing all the information for the user
    print(f"The category is {chosen_category}")
    print(f"Maximum incorrect guesses: {max_guesses}")
    print(f"{word_display}")
    print(f"Guessed letters: {' '.join(guessed_letters)}")

    # get user input and confirm
    while True:
        detected_letter = asl_detector.get_letter()

        if detected_letter is None:
            print("No letter detected. Try again!")
            continue
        # makes sure the input is part of the alphabet and is a single letter
        if detected_letter.isalpha() and len(detected_letter) == 1:
            break
        else:
            print("Invalid input. Please enter a single letter.")

    # ask for confirmation every time a letter is detected
    confirm = input(f"Confirm your guess is: {detected_letter}. Enter 'Y' to confirm or any other key to cancel:")
    if confirm.upper() != 'Y':
        print("Input cancelled!")
        # restart the loop without updating guessed_letters list
        continue  
    # iterating to make sure that the user doesnt repeat and when they do i will not update the list
    if detected_letter.upper() in map(str.upper, guessed_letters):
        print("This letter has been guessed, please try again.")
        continue
    # update guessed letters list
    guessed_letters.append(detected_letter)

    # if the guessed letter is in the hidden word, then it will update
    if detected_letter in chosen_word:
        for i in range(len(chosen_word)):
            if chosen_word[i] == detected_letter:
                guessed_word[i] = detected_letter
        word_display = ' '.join(guessed_word)
    else:
        counter += 1
        print("Incorrect guess. Try again!")
        print(f"You have {max_guesses - counter} guesses left")

# losing or winning statement
if counter == max_guesses:
    print(f"Sorry! The word was {chosen_word}")
else:
    print(f"Congratulations! The word was {chosen_word}")

# release all memory from the external ASL detector module
asl_detector.release()
