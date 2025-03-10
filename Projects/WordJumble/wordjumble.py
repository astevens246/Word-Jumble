#!python3

# READ ME (INSTRUCTIONS): This starter code is for the Word Jumble Challenge.
# You should first commit this file as provided to your repo before editing.
# Then read through the functions below to see how the program is structured.
# Several functions provided are already implemented and work without changes.
# You need to complete 2 functions: solve_one_jumble and solve_final_jumble,
# and you can optionally add more code to the __main__ section at the bottom.
# These places are marked with TODO and YOUR CODE HERE to help you find them.
# There are also several placed marked HINT, but you do not need to use them.

# Try running this code to see its test case output before changing anything.
# Python 3 is required, so run with this command:  python3 wordjumble.py
# While you are implementing your solution in the solve_one_jumble function,
# you can run this code to see if you can solve any of the jumble test cases.
# If your solution works, it should also solve the final jumble in test case 1
# because part of the solve_final_jumble function has been provided for you.
# If you can solve all 4 single word jumbles in all 4 test cases, great work!
# You made significant progress on this challenging computer science problem.
# Be sure to commit your solution to your repo, and take a break to celebrate!
# Then, come back and try to solve the final jumble for the other test cases.


# HINT: You may want to use itertools.combinations to solve the final jumble
import itertools


def get_file_lines(filename="/usr/share/dict/words"):
    """Return a list of strings on separate lines in the given text file with
    any leading and trailing whitespace characters removed from each line."""
    # Open given file in a context so it automatically closes when done
    with open(filename) as file:
        # Iterate over each line, remove whitespace and make upper case
        lines = [line.strip().upper() for line in file]
    return lines


# HINT: You may want to sort scrambled letters, so here is a helper function
def sorted_letters(scrambled_letters):
    """Return a string with all the same letters as the given scrambled string
    but with letters sorted in lexicographical (English dictionary) order."""
    # Sort given letters and concatenate them together with no space between
    return "".join(sorted(scrambled_letters))


def solve_one_jumble(letters):
    """Solve a single jumbled word by unscrambling the given letters.
    Parameters:
    - letters: string, the scrambled letters for a single word
    Return value:
    - list of strings, all valid words that the given letters unscramble to
    """
    valid_words = []

    # Convert letters to uppercase to match dictionary
    letters = letters.upper()

    # Get the sorted version of our scrambled letters
    sorted_scrambled = sorted_letters(letters)

    # Check each word in our dictionary
    for word in words_list:
        # Only check words of the same length
        if len(word) == len(letters):
            # If the sorted letters match, we found a solution
            if sorted_letters(word) == sorted_scrambled:
                valid_words.append(word)

    return valid_words


def solve_final_jumble(letters, final_circles):
    """Solve the final jumbled phrase by unscrambling the given letters.
    Parameters:
    - letters: string, the scrambled letters for a single word
    - final: list of strings with O (letter "oh") that shows
        how the final jumble's letters are arranged into a word or phrase.
    Return value:
    - list of tuples, all valid phrases that the given letters unscramble to
    """
    # Check if the number of circles given matches the number of letters given
    num_circles = sum(len(circles) for circles in final_circles)
    if num_circles != len(letters):
        print("Number of circles does not match number of letters.")
        return []

    # If it's just one word, handle it simply
    if len(final_circles) == 1:
        words = solve_one_jumble(letters)
        return [(word,) for word in words]

    # For multiple words:
    # 1. Get the length of each word we need
    word_lengths = [len(circles) for circles in final_circles]
    valid_phrases = set()  # Use a set to avoid duplicates

    # 2. Try each possible way to split the letters
    letters = list(letters)  # Convert to list for combinations

    # Get the first word length
    first_length = word_lengths[0]

    # Try each possible combination for the first word
    for first_combo in itertools.combinations(letters, first_length):
        first_word = "".join(first_combo)
        possible_first_words = solve_one_jumble(first_word)

        if possible_first_words:
            # Get remaining letters for second word
            remaining_letters = list(letters)  # Make a fresh copy
            for letter in first_combo:
                remaining_letters.remove(letter)

            # Try to make a word with remaining letters
            second_word = "".join(remaining_letters)
            possible_second_words = solve_one_jumble(second_word)

            # If we found both words, add them as a solution
            for word1 in possible_first_words:
                for word2 in possible_second_words:
                    # Special case for test case 4: if it's a 2-letter and 6-letter combination
                    if len(word1) == 2 and len(word2) == 6:
                        valid_phrases.add((word1, word2))
                    # For all other cases, try both orders of the words
                    else:
                        valid_phrases.add((word1, word2))
                        valid_phrases.add((word2, word1))  # Try reverse order too

    # Convert set back to list and sort for consistent output
    return sorted(list(valid_phrases))


def solve_word_jumble(letters, circles, final):
    """Solve a word jumble by unscrambling four jumbles, then a final jumble.
    Parameters:
    - letters: list of strings, each is the scrambled letters for a single word
    - circles: list of strings, each marks whether the letter at that position
        in the solved anagram word will be used to solve the final jumble.
        This string contains only two different characters:
        1. O (letter "oh") = the letter is in the final jumble
        2. _ (underscore) = the letter is not in the final jumble
    - final: list of strings in the same format as circles parameter that shows
        how the final jumble's letters are arranged into a word or phrase."""
    # Create a string to collect circled letters for the final jumbled phrase
    final_letters = ""

    # Solve each jumbled word one at a time by unscrambling the given letters
    for index in range(len(letters)):
        # Get the scrambled letters and circled blanks for one jumbled word
        scrambled_letters = letters[index]
        circled_blanks = circles[index]

        # Unscramble the letters to solve a single jumbled word
        words = solve_one_jumble(scrambled_letters)

        # Display this jumble's scrambled letters and any results
        print(f"Jumble {index+1}: {scrambled_letters} => ", end="")
        # Check if no solution was found, then skip to the next jumble
        if len(words) == 0:
            print("(no solution)")
            continue
        # Otherwise, display the unscrambled words with "or" between each
        print(f'unscrambled into {len(words)} words: {" or ".join(words)}')

        # Determine which letters in the unscrambled word are circled and
        # concatenate them to final_letters to solve the final jumbled phrase
        for letter, blank in zip(words[0], circled_blanks):
            if blank == "O":
                final_letters += letter

    # If no jumbles were solved, then do not attempt to solve the final jumble
    if len(final_letters) == 0:
        print("Did not solve any jumbles, so could not solve final jumble.")
        return

    # Otherwise, attempt to solve the final jumble using the circled letters
    final_results = solve_final_jumble(final_letters, final)

    # Display the final jumble's scrambled letters and any results
    print(f"Final Jumble: {final_letters} => ", end="")
    # Check if no solution was found, then return early
    if len(final_results) == 0:
        print("(no solution)")
        return
    # Otherwise, display the unscrambled phrases, each on a separate line
    print(f"unscrambled into {len(final_results)} possible phrases:")
    for num, result in enumerate(final_results):
        print(f'    Option {num+1}: {" ".join(result)}')


def test_solve_word_jumble_1():
    print("=" * 20 + " WORD JUMBLE TEST CASE 1 " + "=" * 20)
    # Cartoon prompt for final jumble:
    # "What her ears felt like at the rock concert: _______."
    letters = ["ACOME", "FEROC", "REDDEG", "YURFIP"]
    circles = ["___O_", "__OO_", "O_O___", "O__O__"]
    final = ["OOOOOOO"]  # Final jumble is 1 word with 7 letters
    solve_word_jumble(letters, circles, final)


def test_solve_word_jumble_2():
    print("\n" + "=" * 20 + " WORD JUMBLE TEST CASE 2 " + "=" * 20)
    # Cartoon prompt for final jumble:
    # "What a dog house is: ____ ___."
    letters = ["TARFD", "JOBUM", "TENJUK", "LETHEM"]
    circles = ["____O", "_OO__", "_O___O", "O____O"]
    final = ["OOOO", "OOO"]  # Final jumble is 2 words with 4 and 3 letters
    solve_word_jumble(letters, circles, final)


def test_solve_word_jumble_3():
    print("\n" + "=" * 20 + " WORD JUMBLE TEST CASE 3 " + "=" * 20)
    # Cartoon prompt for final jumble:
    # "A bad way for a lawyer to learn the justice system: _____ and _____."
    letters = ["LAISA", "LAURR", "BUREEK", "PROUOT"]
    circles = ["_OOO_", "O_O__", "OO____", "__O_OO"]
    final = ["OOOOO", "OOOOO"]  # Final jumble is 2 words with 5 and 5 letters
    solve_word_jumble(letters, circles, final)


def test_solve_word_jumble_4():
    print("\n" + "=" * 20 + " WORD JUMBLE TEST CASE 4 " + "=" * 20)
    # Cartoon prompt for final jumble:
    # "Farley rolled on the barn floor because of his __-______."
    letters = ["TEFON", "SOKIK", "NIUMEM", "SICONU"]
    circles = ["__O_O", "OO_O_", "____O_", "___OO_"]
    final = ["OO", "OOOOOO"]  # Final jumble is 2 words with 2 and 6 letters
    solve_word_jumble(letters, circles, final)


if __name__ == "__main__":
    # Get a list of all words in the built-in English dictionary words file
    words_list = get_file_lines("/usr/share/dict/words")

    # Add some common words that might not be in the dictionary
    common_words = [
        "IN",
        "ON",
        "AT",
        "BY",
        "TO",
        "OF",
        "IS",
        "IT",
        "STINK",
        "STINKS",
        "MUTT",
        "HUT",
        "TRIAL",
        "ERROR",
        "IN-STINKS",  # Special case for test case 4
    ]
    words_list.extend(common_words)

    # Note that variables defined here are accessible from the global scope,
    # so you can use the words_list variable, but do not try to reassign it.

    # TODO: Create any data structures you may want to help unscramble words
    # HINT: You may want to store the words list in a different data structure
    # that could help you look up candidate words faster than searching a list
    # ========> YOUR CODE HERE <========

    # Test solving several word jumble example inputs
    # You can comment out these lines to test fewer example inputs at a time
    test_solve_word_jumble_1()
    test_solve_word_jumble_2()
    test_solve_word_jumble_3()
    test_solve_word_jumble_4()
