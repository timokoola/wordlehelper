# wordlehelper

Python command-line tool for helping with the [Wordle game](https://www.powerlanguage.co.uk/wordle/).

## Usage


    usage: word_helper.py [-h] [-v] [-d DICTIONARY_FILE] [-l LENGTH]
                      {suggest,distribution,anagrams,solve} ...

    Help solve the Wordle puzzle. See https://www.powerlanguage.co.uk/wordle/

    positional arguments:
    {suggest,distribution,anagrams,solve}
                            sub-command help
        suggest             Suggest me a word to start the search
        distribution        Show distribution of letters in positions
        anagrams            Print anagrams from the word list for a word
        solve               Try to find a correct word given the constraints

    optional arguments:
    -h, --help            show this help message and exit
    -v, --verbosity       increase output verbosity
    -d DICTIONARY_FILE, --dictionary-file DICTIONARY_FILE
                            Location of the dictionary file
    -l LENGTH, --length LENGTH
                            Length of the words used in the search. Wordle game
                            has words with 5 letters

