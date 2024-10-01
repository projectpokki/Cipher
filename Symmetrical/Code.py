from numpy import empty, uint8
from PIL import Image

idToCharLookup = {
  0: "A",
  1: "B",
  2: "C",
  3: "D",
  4: "E",
  5: "F",
  6: "G",
  7: "H",
  8: "I",
  9: "J",
  10: "K",
  11: "L",
  12: "M",
  13: "N",
  14: "O",
  15: "P",
  16: "Q",
  17: "R",
  18: "S",
  19: "T",
  20: "U",
  21: "V",
  22: "W",
  23: "X",
  24: "Y",
  25: "Z",
  26: "0",
  27: "1",
  28: "2",
  29: "3",
  30: "4",
  31: "5",
  32: "6",
  33: "7",
  34: "8",
  35: "9",
  36: " ",
  37: "\n",
  38: ".",
  39: ",",
  40: ":",
  41: ";",
  42: "?",
  43: "!",
  44: "-",
  45: "(",
  46: ")",
  47: "\'",
  48: "\"",
  49: "º"
}


charToIdLookup = {
  "A": 0,
  "B": 1,
  "C": 2,
  "D": 3,
  "E": 4,
  "F": 5,
  "G": 6,
  "H": 7,
  "I": 8,
  "J": 9,
  "K": 10,
  "L": 11,
  "M": 12,
  "N": 13,
  "O": 14,
  "P": 15,
  "Q": 16,
  "R": 17,
  "S": 18,
  "T": 19,
  "U": 20,
  "V": 21,
  "W": 22,
  "X": 23,
  "Y": 24,
  "Z": 25,
  "0": 26,
  "1": 27,
  "2": 28,
  "3": 29,
  "4": 30,
  "5": 31,
  "6": 32,
  "7": 33,
  "8": 34,
  "9": 35,
  " ": 36,
  "\n": 37,
  ".": 38,
  ",": 39,
  ":": 40,
  ";": 41,
  "?": 42,
  "!": 43,
  "-": 44,
  "(": 45,
  ")": 46,
  "\'": 47,
  "\"": 48,
  "º": 49
}


def prng(seed, iterations):
  numbers = []
  for _ in range(iterations + 8):
    seed = (seed ** 2) % 59521081
    if seed in numbers:
      print("WARNING PRNG LOOP REACHED", len(numbers))
      exit()
    numbers.append(seed)
  return numbers[8:]


def encode(fileName, seed):
  try:
    with open(fileName, "r") as text:
      if not text.readable():
        print("ERROR: file is unable to be read")
        exit()
      textStr = text.read()
      if len(textStr) > 2352:
        print("ERROR: file exceeds limit of 2352 characters")
        exit()
      formattedList = [36] * 2352
      for num, char in enumerate(textStr):
        if char in charToIdLookup:
          formattedList[num] = charToIdLookup[char]
        else:
          print("ERROR: file includes invalid character")
          exit()
      value = formattedList
  except Exception:
    print("ERROR: file does not exist or is not a text file")
    exit()

  for seedChange in range(0, 126, 2):
    randNums = prng(seed + seedChange, 588)
    outputValues = []
    for i in range(0, 2352, 4):
      k = randNums[int(i * 0.25)]
      outputValues.extend([
        (value[i] + int((k * 0.000001) % 50)) % 50,
        (value[i+1] + int((k * 0.0001) % 50)) % 50,
        (value[i+2] + int((k * 0.01) % 50)) % 50,
        (value[i+3] + int(k % 50)) % 50
      ])
    value = outputValues

    randNums = prng(seed + seedChange + 1, 1176)
    pairCandidates = []
    for i in range(0, 2352):
      pairCandidates.append(i)
    pairs = []
    for j, randNum in enumerate(randNums):
      k1 = int(randNum * 0.0001) % (2352 - (j * 2))
      k2 = int(randNum % (2351 - (j * 2)))
      pairs.append([pairCandidates[k1]])
      pairCandidates.pop(k1)
      pairs[-1].append(pairCandidates[k2])
      pairCandidates.pop(k2)
    for pair in pairs:
      value[pair[0]], value[pair[1]] = value[pair[1]], value[pair[0]]
    
    for i in range(0, 2352):
      value[i] = sum(value) % 50

  # valueSum = sum(value)
  # value.extend([
  #   ((seed // 125000) + valueSum) % 50,
  #   ((seed // 2500) + valueSum) % 50,
  #   ((seed // 50) + valueSum) % 50,
  #   (seed + valueSum) % 50
  # ])
  
  # for i in range(0, 2304):
  #   value[i] = sum(value) % 50
  
  formattedOutput = ""
  for i in value:
    formattedOutput += str(i).zfill(2) + "-"
  return formattedOutput[:-1]


def decode(fileName, seed):
  try:
    with open(fileName, "r") as text:
      if not text.readable():
        print("ERROR: file is unable to be read")
        exit()
      textStr = text.read()
      value = []
      # if len(textStr) != 6911:
      if len(textStr) != 7055:
        print("ERROR: file is not valid cipher")
        exit()
      textStr += "-"
      # for i in range(0, 6912, 3):
      for i in range(0, 7056, 3):
        if not (textStr[i:i+2].isdecimal() and textStr[i+2] == "-"):
          print("ERROR: file is not valid cipher")
          exit()
        value.append(int(textStr[i:i+2]))
  except Exception:
    print("ERROR: file does not exist or is not a text file")
    exit()
  
  # for i in range(2303, -1, -1):
  #   value[i] = (value[i] * 2 - sum(value)) % 50

  # listSum = sum(value[:-4])
  # seed = ((value[-4] - listSum) % 50) * 125000 + ((value[-3] - listSum) % 50) * 2500 + ((value[-2] - listSum) % 50) * 50 + ((value[-1] - listSum) % 50)
  # value = value[:-4]
  
  for seedChange in range(124, -2, -2):
    for i in range(2351, -1, -1):
      value[i] = (value[i] * 2 - sum(value)) % 50
    
    randNums = prng(seed + seedChange + 1, 1176)
    pairCandidates = []
    for i in range(0, 2352):
      pairCandidates.append(i)
    pairs = []
    for j, randNum in enumerate(randNums):
      k1 = int(randNum * 0.0001) % (2352 - (j * 2))
      k2 = int(randNum % (2351 - (j * 2)))
      pairs.append([pairCandidates[k1]])
      pairCandidates.pop(k1)
      pairs[-1].append(pairCandidates[k2])
      pairCandidates.pop(k2)
    for pair in pairs:
      value[pair[0]], value[pair[1]] = value[pair[1]], value[pair[0]]
    
    randNums = prng(seed + seedChange, 588)
    outputValues = []
    for i in range(0, 2352, 4):
      k = randNums[int(i*0.25)]
      outputValues.extend([
        (value[i] - int((k * 0.000001) % 50)) % 50,
        (value[i+1] - int((k * 0.0001) % 50)) % 50,
        (value[i+2] - int((k * 0.01) % 50)) % 50,
        (value[i+3] - int(k % 50)) % 50
      ])
    value = outputValues
    
  return "".join(idToCharLookup[i] for i in value).rstrip()


def cipherToImg(fileName, newFileName):
  try:
    with open(fileName, "r") as text:
      if not text.readable():
        print("ERROR: file is unable to be read")
        exit()
      textStr = text.read()
      cipher = []
      # if len(textStr) != 6911:
      if len(textStr) != 7055:
        print("ERROR: file is not valid cipher")
        exit()
      textStr += "-"
      # for i in range(0, 6912, 3):
      for i in range(0, 7056, 3):
        if not (textStr[i:i+2].isdecimal() and textStr[i+2] == "-"):
          print("ERROR: file is not valid cipher")
          exit()
        cipher.append(int(textStr[i:i+2]))
  except Exception:
    print("ERROR: file does not exist or is not a text file")
    exit()

  formattedCipher = empty((28, 28, 3), dtype=uint8)
  for i in range(0, len(cipher), 3):
    formattedCipher[int((i/3)//28), int((i/3)%28)] = [cipher[i] * 5, cipher[i+1] * 5, cipher[i+2] * 5]

  img = Image.fromarray(formattedCipher, "RGB")
  try:
    img.save(newFileName)
  except Exception:
    print("ERROR: file to put image is not in image format")
    exit()
  print("write success")
  

def imgToCipher(fileName):
  try:
    img = Image.open(fileName)
    formattedCipher = list(img.getdata())
    cipher = ""
    for i in formattedCipher:
      for j in i:
        cipher += str(int(j * 0.2)).zfill(2) + "-"
    if len(cipher) != 7056:
      print("ERROR: file is not valid cipher")
      exit()
    return cipher[:-1]
  except Exception:
    print("ERROR: file does not exist, is unable to be read, or is not an image")
    exit()

#CONTROL
mode = input("[CIPHER PROGRAM]\n\nprogram modes:\n  0: plaintext -> cipher\n  1: cipher -> plaintext\n  2: cipher -> image\n  3: image -> cipher\n\nselect program mode 0-3: ")
if mode == "0":
  file = input("enter name of file to encode: ")
  seed = input("enter seed to use: ")
  newFile = input("enter name of file to write cipher: ")
  if seed.isdecimal() and int(seed) >= 8344:
    cipher = encode(file, int(seed))
    with open(newFile, "w") as nf:
      nf.write(cipher)
      print("write success")
  else:
    print("ERROR: seed must be a number greater or equal to 8344")
    
elif mode == "1":
  file = input("enter name of file to decode: ")
  seed = input("enter seed to use: ")
  newFile = input("enter name of file to write plaintext: ")
  if seed.isdecimal() and int(seed) >= 8344:
    plaintext = decode(file, int(seed))
    with open(newFile, "w") as nf:
      nf.write(plaintext)
      print("write success")
  else:
    print("ERROR: seed must be a number greater or equal to 8344")
    
elif mode == "2":
  file = input("enter name of file to visualise cipher: ")
  newFile = input("enter name of file to put image: ")
  cipherToImg(file, newFile)
  
elif mode == "3":
  file = input("enter name of file to decode image: ")
  newFile = input("enter name of file to write cipher: ")
  cipher = imgToCipher(file)
  with open(newFile, "w") as nf:
    nf.write(cipher)
    print("write success")
    
else:
  print("ERROR: enter an appropriate input")
