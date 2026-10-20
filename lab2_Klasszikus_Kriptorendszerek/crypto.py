from pathlib import Path
from collections import Counter

#------------------------------------------------------
# ceasar cipher enkriptalo
def encrypt_caesar(plaintext):
    ciphertext = ""

    for char in plaintext:
        if 'A' <= char <= 'Z':
            position = ord(char) - ord('A')
            new_position = (position + 3) % 26
            new_char = chr(new_position + ord('A'))

            ciphertext += new_char
        else:
            ciphertext +=char 
    
    return ciphertext       







# ceasar cipher dekriptalo
def decrypt_caesar(ciphertext):
    plaintext = ""

    for char in ciphertext:
        if 'A' <= char <= 'Z':

            position = ord(char) - ord('A')
            new_position = (position - 3) % 26
            new_char = chr(new_position + ord('A'))


            plaintext += new_char
        else:
            plaintext += char


    return plaintext

#---------------------------------------------------------




# vigenere encript
def encrypt_vigenere(plaintext, keyword):
    
    ciphertext = ""
    keyword = keyword.upper()
    key_index = 0


    if not keyword or not keyword.isascii() or not keyword.isalpha():
        raise ValueError("a kulcs muszaly A-Z betuibol aljon")

    for char in plaintext:
        if 'A' <= char <= 'Z':
            position = ord(char) - ord('A')
            shift = ord(keyword[key_index % len(keyword)]) - ord('A')

            new_position = (position + shift) % 26
            ciphertext += chr(new_position + ord('A'))

            key_index += 1
        else:
            ciphertext += char

    return ciphertext




# vigenere decrypt
def decrypt_vigenere(ciphertext, keyword):
    
    plaintext = ""
    keyword = keyword.upper()
    key_index = 0

    if not keyword or not keyword.isascii() or not keyword.isalpha():
        raise ValueError("A Kulcs muszaly A - Z betuibol aljon")

    for char in ciphertext:
        if 'A' <= char <= 'Z':
            position = ord(char) - ord('A')
            shift = ord(keyword[key_index % len(keyword)]) - ord('A')

            new_position = (position - shift) % 26
            plaintext += chr(new_position + ord('A'))

            key_index += 1
        else:
            plaintext += char

    return plaintext

#-----------------------------------------------------------------------------------

#Scytale Cipher encrypt 
def encrypt_scytale(plaintext, circumference):
    if circumference <= 0:
        raise ValueError("a kerulet pozitiv kell legyen")

    ciphertext = ""

    for i in range(circumference):
        for j in range(i, len(plaintext), circumference):
            ciphertext += plaintext[j]

    return ciphertext

#scytale decript

def decrypt_scytale(ciphertext, circumference):
    if circumference <= 0:
        raise ValueError("Pozitiv legyen a kerulet")

    plaintext = [""] * len(ciphertext)
    index = 0

    for i in range(circumference):
        for j in range(i, len(ciphertext), circumference):
            plaintext[j] = ciphertext[index]
            index += 1

    return "".join(plaintext)


# ------------------------------------------------------------------- 
#railfence cipher enkriptalas
def encrypt_railfence(plaintext, num_rails):
    if num_rails < 2:
        raise ValueError("legalabb 2 sor szukseges!!!!")

    rails = [""] * num_rails

    row = 0
    direction = 1

    for char in plaintext:
        rails[row] += char

        if row == 0:
            direction = 1
        elif row == num_rails - 1:
            direction = -1

        row += direction

    return "".join(rails)



# railfence dekriptalo
def decrypt_railfence(ciphertext, num_rails):
    if num_rails < 2:
        raise ValueError("legalabb 2 sor szukseges")

    pattern = []

    row = 0
    direction = 1


    # megallapitjuk a karakterunk sorait
    for char in ciphertext:
        pattern.append(row)

        if row == 0:
            direction = 1
        elif row == num_rails - 1:
            direction = -1

        row += direction

    # szetosszuk a karaktereket a sorokban
    rails = []
    index = 0



    for i in range(num_rails):
        count = pattern.count(i)
        rails.append(list(ciphertext[index:index + count]))
        index += count

    #eredeti sorrend visszaallitasa
    plaintext = ""

    for i in pattern:
        plaintext += rails[i].pop(0)

    return plaintext


# --------------------------------------------------------------- 
# file feldolgozas 
def read_file():
    filename = input("file neve: ")

    with open(filename, "r", encoding="utf-8") as file:
        text = file.read()

    return text.upper()

# file irasa
def write_file(text):
    filename = input("file amibe mentsuk: ")

    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)

    print("sikeres mentes")


# -------------------------------------------------------------- 
#INTELIGENT Codebreaker



DICTIONARY_PATH = Path(__file__).resolve().parent / "words_alpha.txt"

#altalanos angol szotar betu gyakorisaga
ENGLISH_FREQ = [
    8.17, 1.49, 2.78, 4.25, 12.70, 2.23, 2.02,
    6.09, 6.97, 0.15, 0.77, 4.03, 2.41, 6.75,
    7.51, 1.93, 0.10, 5.99, 6.33, 9.06, 2.76,
    0.98, 2.36, 0.15, 1.97, 0.07
]




def load_dictionary():
    #betolti az angol szotarat

    if not DICTIONARY_PATH.is_file():
        raise FileNotFoundError(
            f"nem talalhato szotar: {DICTIONARY_PATH}"
        )

    with open(DICTIONARY_PATH, "r", encoding="utf-8") as file:
        words = {
            line.strip().upper()
            for line in file
            if line.strip().isascii() and line.strip().isalpha()
        }


    if not words:
        raise ValueError("szotar ures")

    return words


def frequency_score(text):
    #kiszamoljuk az angol betugyakorisagtol valo elterest

    letters = [c for c in text if "A" <= c <= "Z"]

    if not letters:
        return float("inf")

    counts = Counter(letters)
    n = len(letters)
    score = 0

    for i in range(26):
        char = chr(ord("A") + i)

        observed = counts[char]
        expected = n * ENGLISH_FREQ[i] / 100

        score += (observed - expected) ** 2 / expected

    #kissebb ertekek = nagyobb valoszinuseg szavak
    return score




def word_score(text, dictionary):
    #szoveg szotari szavakra bontasa

    text = "".join(c for c in text if "A" <= c <= "Z")

    n = len(text)

    #dinamikus programozas
    best = [0] * (n + 1)

    for i in range(n - 1, -1, -1):



        #ha nem ismerjuk fel a betuket akkor buntetes
        best[i] = best[i + 1] - 2

        #20 betuhosszig vizsgalunk
        for j in range(i + 1, min(n, i + 20) + 1):

            word = text[i:j]

            if word in dictionary:

                #hosszu felismerheto szavak tobbet ernek
                points = len(word) ** 2

                best[i] = max(
                    best[i],
                    points + best[j]
                )

    return best[0]





def show_progress(current, total, bar_length=30):
    #progressBar beepitese

    percent = current / total

    filled = int(bar_length * percent)



    bar = "*" * filled
    bar += "." * (bar_length - filled)



    print(
        f"\r[{bar}] {percent * 100:6.2f}% "
        f"({current}/{total})",
        end="",
        flush=True
    )



    if current == total:
        print()




def crack_vigenere(ciphertext):
    #kiprobaljuk az osszes szotari kulcsot

    dictionary = load_dictionary()

    ciphertext = "".join(
        c for c in ciphertext.upper()
        if "A" <= c <= "Z"
    )

    if not ciphertext:
        raise ValueError("a titkositott szoveg ures")

    # az uzenetnel hosszabb kulcs ervenytelen
    possible_keys = sorted(
        word for word in dictionary
        if len(word) <= len(ciphertext)
    )



    total = len(possible_keys)

    if total == 0:
        raise ValueError("nincsenek kiprobalhato kulcsok")

    results = []


    #TUI
    print("\n========== INTELLIGENT CODEBREAKER ==========")
    print("szotar: ", DICTIONARY_PATH.name)
    print("betoltott szavak:", len(dictionary))
    print("kiprobalando kulcsok:", total)
    print("ciphertext:", ciphertext)
    print()



    show_progress(0, total)

    progress_step = max(1, total // 100)

    for index, key in enumerate(possible_keys, start=1):



        # vignere visszafejtes
        plaintext = decrypt_vigenere(ciphertext, key)

        #angol szavak felismerese
        words = word_score(plaintext, dictionary)

        #betugyakorisag ellenorzese
        frequency = frequency_score(plaintext)

        #vegso pontszam
        score = words - frequency

        results.append((score, key, plaintext))



        # szazalenkonkent frissites
        if index % progress_step == 0 or index == total:
            show_progress(index, total)

    #legjobb pontszamok elore
    results.sort(key=lambda item: item[0], reverse=True)

    return results[:5]



#------------------------------------------------------------------ 



def main():
    text = ""

    while True:
        print("\nSHEPHERDMIKE --- PMKM0005")
        print("\n========== CRYPTO MENU ==========")
        print("Mostani szoveg:", text)

        print("1 - uj szoveg terminalbol")
        print("2 - caesar Encrypt")
        print("3 - caesar Decrypt")
        print("4 - vigenere Encrypt")
        print("5 - vigenere Decrypt")
        print("6 - scytale Encrypt")
        print("7 - scytale Decrypt")
        print("8 - rail Fence Encrypt")
        print("9 - rail Fence Decrypt")
        print("10 - vigenere Codebreaker")
        print("11 - file olvasasbol szoveg")
        print("12 - mentsd fileba")
        print("0 - exit")

        choice = input("Valassz: ")

        if choice == "1":
            text = input("uj szoveg: ").upper()

        elif choice == "2":
            text = encrypt_caesar(text)
            print("enkriptalt:", text)

        elif choice == "3":
            text = decrypt_caesar(text)
            print("dekriptalt:", text)

        elif choice == "4":
            keyword = input("Add meg a kulcsot: ").upper()
            text = encrypt_vigenere(text,keyword)
            print("Enkriptalt:", text)

        elif choice == "5":
            keyword = input("Add meg a kulcsot: ").upper()
            text = decrypt_vigenere(text,keyword)
            print("dekriptalt", text)

        elif choice == "6":
            circumference = int(input("kerulet megadasa: "))
            text = encrypt_scytale(text,circumference)
            print("enkriptalt: ",text)

        elif choice == "7":
            circumference = int(input("kerulet megadasa: "))
            text = decrypt_scytale(text,circumference)
            print("dekriptalt: ",text)


        elif choice == "8":
            num_rails = int(input("sorok szama: "))
            text = encrypt_railfence(text, num_rails)
            print("enkriptalt", text)

        elif choice == "9":
            num_rails = int(input("sorok szama: "))
            text = decrypt_railfence(text, num_rails)
            print("dekriptalt", text)



        elif choice == "10":
            try:
                results = crack_vigenere(text)

                print("\n========== TOP 5 MEGFEJTES ==========")

                for i, (score, key, message) in enumerate(results, start=1):
                    print(f"\n{i}. talalat")
                    print(f"kulcs: {key}")
                    print(f"szoveg: {message}")
                    print(f"pontszam: {score:.2f}")

                print("\n====================================")

                selected = input(
                    "melyik megfelytes tunik okesnak (1-5,0 - megsem): "
                )

                if selected in ["1", "2", "3", "4", "5"]:
                    index = int(selected) - 1

                    if index < len(results):
                        text = results[index][2]
                        print("sikeres megfelytes")
                        print("uj szoveg:", text)
                    else:
                        print("nincs ilyen talalat")

                elif selected == "0":
                    print("az eredeti szoveg megmaradt!!!")

                else:
                    print("hibas valasztas")

            except (ValueError, OSError) as error:
                print("Hiba:", error)

        elif choice == "11":
            text = read_file()
            print("sikeresen beolvasva:", text)
        
        elif choice == "12":
            write_file(text)

        elif choice == "0":
            print("Adj Max pontot PLS :3")
            break

        else:
            print("NUH UH :>")


if __name__ == "__main__":
    main()


