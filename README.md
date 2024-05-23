# Chess2Audio
Welcome to Chess2Audio! This is a self-maintained project. You can fork this, but I will most likely not accept any merges into the main branch. Feel free to use this wherever you see fit.

## Where to go?
There really is just one file, so just download it.
You will need pgn files to do this (duh), you can find this on lichess.org or on chess.com. Chess2Audio supports single file (manual input), a folder of files, or even a single huge pgn file with many games (supports auto-formatting).

## Usage
So how to use it?
Well at the moment (Commit 2), you can either run it as standalone code or import it.

### Standalone code:
Follow the instructions. Note that the file name **will** need a directory built in to it unless you want it within the same directory as the python file.
Be sure the file and folder exists! (If you run the exact same inputs again, the files will get overwritten!)

### As an import:
You have various methods, such as ```roundFrequency(freq)```, which just rounds frequency to the nearest piano note.

Here is a list of all the methods:
```
isThere(thing, move) # Similar to needle in haystack, but returns a boolean.

roundFrequency(freq) # Rounds frequency to nearest piano note

getFrequency(sC, lC, piece, capture, epx, epy, pro, check, mate) # Returns a value, relies on roundFrequency. The core of the code
'''
  sC: short castle
  lC: long castle
  piece: piece...
  capture: capture...
  epx: piece moved to file (x is the file as a number)
  epy: piece moved to rank (y is the rank as a number (it already is))
  pro: promotion
  check: check...
  mate: checkmate
'''
concatenate_frequencies_to_wav(frequencies, duration_s, output_file) # Concatenates frequencies generated into one .wav file. By default, duration_s = 1 and output_file = "output.wav".

concatenate_frequencies_to_csv(frequencies, duration_s, output_file, index) # Similar to the function for wav, but instead write out the frequencies to a csv file. The index is there for future use when concatenating many chess games into plotting for analysis.

Chess2Audio(origin, length, destination, useDefaultNamingScheme, idx, directory) # What actually turns a file into music and csv.
'''
  origin: File origin
  length: How long the gaps should be
  destination: Where the file should end up
  useDefaultNamingScheme: Default is False, when set to True it uses the information and outputs files as white's name and black's name with date.
  idx: only used for the csv file, if you don't need it, you don't have to put it.
  directory: needed if you are going to use default naming scheme, otherwise it presumes same directory. (edge case not tested yet)
'''
parseFolder(originalDirectory, destinationDirectory, delay) # originalDirectory is the folder to parse, destinationDirectory is where the audio should go, and delay is the delay between sounds. I recommend 0.1 for cool sounds.

parseHugeFile(file, destinationDirectory, pauseLength) # similar to parseFolder, but uses file instead of originalDirectory.
```

## Moving forward
Perhaps a visualization of the audio files for data analysis, clock moves corresponding to durations in length.
Consistency within functions.

### Other notes
Still learning ins and outs of github, so don't expect clean code or documentation much. Don't even expect this to be great. It's just good enough.
