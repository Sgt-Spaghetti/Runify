# Runify
A python and TKinter fantasy language conversion program

To launch and use in console mode:
* python3 Runify.py c

To launch and use in graphical mode:
* python3 Runify.py

Runify allows the conversion of an input text file, or a live custom input, to be converted into Eldar Futhark runes and or into the fantasy dwarven language of Khazalid from the Warhammer universe.

However, it can do even more than that. As of 20/1/21, Runify is also capable of creating and loading custom conversion dictionaries for both letters and words! This means that now it can be used to translate or transliterate into any language or symbol of your choosing.

To use at its most basic in graphical mode:
* Select a file to as the input file from which text will be translated from using the file browser.
* Select if you want to transliterate letters, words or both.
* Press the submit button.
* Select the desired output file and its name using the browser.
* Done! The results should be visible in the lower output window and the contents should be written into the output file.

To use with custom input:
* Check the custom input checkbox.
* You will no longer be able to select an input file nor will any output be saved in a file.
* Select if you want to transliterate letters, words or both.
* Type or copy/past the text to be translated into the newly appeared input window (the leftmost text entry window).
* Press the submit button and the output should be visible in the output window.

To create a custom conversion dictionary:
* First decide if you want to create a Word dictionary or a letter dictionary.

For the best results, a word dictionary should have single word entries with no spaces or symbols, with a corresponding output word. a letter dictionary should have single character inputs and corresponding outputs.

* In the top menu, select the "Options" drop-down.
* Select the "Custom Dictionary" option.
* A new window should appear to help with the creation process.
* Enter the first of the new inputs and its corresponding outputs in the leftmost and rightmost boxes appropriately.
* To add a new field press the "New Entry" button.
* Once you have finished the creation process, press the "Save" button to save the created dictionary with a name and in a location of your choosing. It should be a text file.
* Note, created dictionaries are not automatically loaded, see below to load the dictionary.

To load custom dictionaries:
* Decide whether to load a word dictionary or a letter dictionary as described above.
* Click on the "Options" drop-down, and press the "Load Custom Dictionary" option.
* Select the appropriate dictionary option, word or letter.
* Navigate to and select the correct input file that you would like to use, created from the "Create Custom Dictionary" option.
* Done, the new custom dictionary should be set. You can try it out with the custom input option.

To load .csv files created externally:
Please make sure the .csv file is created from only 2 columns, the leftmost being the input character/word and the rightmost being the output character/word.
The file should look something like this:

input1,output1
input2,output2
input3,output3

* Select the "Options" drop-down, and select "Load from custom dictionary" followed by "Load from csv" and the appropriate option for the .csv file.
* Navigate and select the correct .csv file desired from the file browser.
* Done, the .csv file should now be loaded as a custom dictionary.

To clear custom dictionaries:
* Select the "Clear Custom Dictionaries" option from the "Options" Dropdown.

To set a theme for the Runify app:
* Click on the "Themes" drop-down in the menu-bar.
* Select the desired theme.

To save the current theme:
* Click on the "Themes" drop-down in the menu-bar.
* Select the "Save theme" option.
A new file, "config.txt" will be created in the Runify directory with the theme information which should now apply as the default theme when you start the application.
