from pydub import AudioSegment
from pydub.generators import Sine
from math import log, log2
from librosa import note_to_hz, hz_to_note
from os import chdir, listdir, remove
from progress.bar import Bar

def isThere(thing, move):
    res = move.find(thing)
    match res:
        case -1: return False
        case _: return True

def roundFrequency(freq):
    return note_to_hz(hz_to_note(freq))

def getFrequency(sC, lC, piece, capture, epx, epy, pro, check, mate):
    pieceValues = {
        'K': 12,
        'Q': 9,
        'R': 5,
        'B': 3.25,
        'N': 3,
        'P': 1
    }
    
    def subFunction(x, y):
        return x**2 + 2 * log2(y+1)
    
    frequency = 440 * log((pieceValues[piece]*subFunction(epx, epy)) + 1,6) - 50*capture + 75*pro + 100 * (check + 2*mate)
    return roundFrequency(pow(frequency, 7/8))

def concatenate_frequencies_to_wav(frequencies, duration_s=1, output_file="output.wav"):
    duration_ms = duration_s * 1000
    
    concatenated_audio = AudioSegment.silent(duration=0)
    
    for freq in frequencies:
        tone = Sine(freq).to_audio_segment(duration=duration_s*1000)
        concatenated_audio += tone
    
    concatenated_audio.export(output_file, format="wav")

def concatenate_frequencies_to_csv(frequencies, duration_s=1, output_file="output.csv", index=0):
    csvFile = "index,time,frequency\n"
    time = 0
    for freq in frequencies:
        csvFile += f"{index},{time},{freq}\n"
        time += duration_s
    f = open(output_file, "w")
    f.write(csvFile)
    f.close()

### MAIN ###
def Chess2Audio(origin, length, destination, useDefaultNamingScheme=False, idx=0, directory=""):
    # Declarations
    pieces = {'K', 'Q', 'R', 'B', 'N'}

    column = {
        "a": 1,
        "b": 2,
        "c": 3,
        "d": 4,
        "e": 5,
        "f": 6,
        "g": 7,
        "h": 8
    }

    # Get file    
    f = open(origin, 'r')
    information = []
    game = ""

    # Filter
    for thing in f.readlines():
        match thing[0]:
            case '[': information.append(thing[:-1])
            case '\n': continue
            case _: game += thing[:-1] + ' '

    game = game.split(' ')
    game.pop(len(game)-1)

    result = game.pop(len(game)-1)

    # Fill in the missing stuff:
    match result:
        case "1-": result += '0'
        case "1/2-1/": result += '2'
        case "0-": result += '1'

    moves = []

    # Filter stuff
    for move in game:
        if not move:
            continue
        if move[-1] not in ['.', '}','k']:
            moves.append(move)

    frequencies = []

    # Generate Audio
    for move in moves:
        shortCastle = isThere('O-O', move)
        longCastle = isThere('O-O-O', move)
        capture = isThere('x', move)
        promotion = isThere('=', move)
        check = isThere('+', move)
        mate = isThere('#', move)
        piece = 'P'
        xPos = 9
        yPos = 9
        
        for thing in pieces:
            if thing == move[0]:
                piece = thing
                break

        shift = 0
            
        if check or mate:
            shift -= 1

        if promotion:
            shift -= 2
        
        if not (shortCastle or longCastle):
            xPos = int(column[move[-2+shift]])
            yPos = int(move[-1+shift])

        frequencies.append(getFrequency(shortCastle, longCastle, piece, capture, xPos, yPos, promotion, check, mate))

    if useDefaultNamingScheme:
        name = ""
        date = ""
        for info in information:
            if info[0:8] in ("[White \"", "[Black \""):
                name += "_".join(info[8:-2].split(", ")) + "_"
            elif info[0:7] == "[Date \"":
                date = info[7:-2]
        if name != "" or date != "":
            destination = directory + "\\" + name + "_" + date + ".wav"

    concatenate_frequencies_to_wav(frequencies, duration_s=length, output_file=destination)
    concatenate_frequencies_to_csv(frequencies, length, destination[:-4] + ".csv", idx)
    f.close()

def parseFolder(originalDirectory, destinationDirectory, delay):
    items = listdir(originalDirectory)
    length = len(items)

    bar = Bar("Converting Files...", max=length)
    for i in range(0, length):
        file = items[i]
        if file.endswith(".pgn"):
            originalFile = originalDirectory + "\\" + file
            destinationFile = destinationDirectory
            Chess2Audio(originalFile, delay, destinationFile, False, i)
        bar.next()
    bar.finish()
    print("Done.")

def parseHugeFile(file, destinationDirectory, pauseLength):
    fi = open(file, 'r')
    f = fi.readlines()
    f.append("\n")
    f.append("\n")
    p1 = ""
    p2 = "?"
    lastGood = 0
    game = 1

    bar = Bar("Processing", max=len(f))
    for i in range(0, len(f)):
        p1 = f[i]
        if p1 == p2 and lastGood != i-1:
            if game > 1:
                lastGood += 1

            directory = destinationDirectory + "\\Game_" + str(game) + ".pgn"
            res = open(directory, "w")
            res.writelines(f[lastGood:i])
            res.close()
            lastGood = i
            game += 1
            
            Chess2Audio(directory, pauseLength, directory[:-3] + ".wav", True, int(game), destinationDirectory)
            remove(directory)
        elif p1 == p2:
            lastGood += 1
        p2 = p1
        bar.next()
    bar.finish()
    fi.close()
        
if __name__ == "__main__":
    print("Welcome to Chess2Audio!")
    useFolder = input("Do you want to parse through a folder of chess games? (Yes/Single File/No) ")

    match useFolder.lower():
        case "yes":
            depart = input("Starting Directory? ")
            arrival = input("Ending Directory? ")
            pauseLength = float(input("Delay? "))
            parseFolder(depart, arrival, pauseLength)
        case "single file":
            print("By default, this uses autonaming scheme.")
            depart = input("Starting File? ")
            arrival = input("Destination Directory? ")
            pauseLength = float(input("Delay? "))
            parseHugeFile(depart, arrival, pauseLength)
        case _:
            while True:
                start = input("Where to read file? ")
                duration = float(input("File Duration? "))
                end = input("Name the file: ")
                Chess2Audio(start, duration, end, False)
                after = input("Continue? (Yes/No) ")
                match after.lower():
                    case "no": break
                    case _: continue
