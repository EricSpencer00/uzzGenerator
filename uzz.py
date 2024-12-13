import re
from collections import defaultdict

# Utility functions
def load_custom_dictionary(file_path="uzzGenerator/word_replacements.txt"):
    """Load a custom dictionary of replacements from a file."""
    replacements = {}
    try:
        with open(file_path, "r") as file:
            for line in file:
                if line.strip():
                    word, replacement = line.strip().split(",")
                    replacements[word.lower()] = replacement
    except FileNotFoundError:
        print("Custom dictionary file not found. Continuing without it.")
    return replacements

def save_custom_dictionary(replacements, file_path="uzzGenerator/word_replacements.txt"):
    """Save a custom dictionary of replacements to a file."""
    with open(file_path, "w") as file:
        for word, replacement in replacements.items():
            file.write(f"{word},{replacement}\n")

def find_last_vowel(word):
    """Find the position of the last vowel in a word."""
    vowels = "aeiouAEIOU"
    for i in range(len(word) - 1, -1, -1):
        if word[i] in vowels:
            return i
    return -1

def transform_word(word):
    """Transform a word to follow the -uzz rule."""
    last_vowel_index = find_last_vowel(word)
    if last_vowel_index == -1:
        return word + "uzz"  # No vowels found, append -uzz
    return word[:last_vowel_index] + "uzz"

def is_noun(word, word_set):
    """Basic check if a word is likely a noun using a predefined word set."""
    return word.lower() in word_set

def process_text(file_path, output_path, custom_dict_path="uzzGenerator/word_replacements.txt", noun_list_path="uzzGenerator/nouns.txt"):
    """Process a text file, transforming nouns based on rules."""
    # Load the custom dictionary
    custom_dict = load_custom_dictionary(custom_dict_path)

    # Load the list of nouns
    with open(noun_list_path, "r") as file:
        noun_set = set(word.strip().lower() for word in file if word.strip())

    with open(file_path, "r") as file:
        lines = file.readlines()

    transformed_lines = []

    for line in lines:
        words = line.split()
        transformed_words = []

        for word in words:
            stripped_word = re.sub(r"\W+$", "", word)  # Remove trailing punctuation
            punctuation = word[len(stripped_word):]  # Store punctuation

            # Check if the word is in the custom dictionary
            if stripped_word.lower() in custom_dict:
                transformed_words.append(custom_dict[stripped_word.lower()] + punctuation)
            # Check if the word is a noun
            elif is_noun(stripped_word, noun_set):
                transformed_words.append(transform_word(stripped_word) + punctuation)
            else:
                transformed_words.append(word)

        transformed_lines.append(" ".join(transformed_words))

    # Write the transformed text to the output file
    with open(output_path, "w") as file:
        file.write("\n".join(transformed_lines))


if __name__ == "__main__":
    # Example usage
    input_file = "uzzGenerator/input.txt"
    output_file = "uzzGenerator/output.txt"

    # Save a sample custom dictionary
    sample_dict = {"bro": "bruzz", "girls": "huzz", "unemployed": "unempluzz"}
    save_custom_dictionary(sample_dict)

    # Create a sample noun list
    sample_nouns = ["bro", "girls", "unemployed", "logo", "barnacle", "pumpernickle"]
    with open("uzzGenerator/nouns.txt", "w") as file:
        file.write("\n".join(sample_nouns))

    process_text(input_file, output_file)
    print(f"Processed text saved to {output_file}")
