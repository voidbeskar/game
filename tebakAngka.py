import random

def main():
    print("Selamat datang di permainan Tebak Angka!")
    print("Saya telah memilih sebuah angka antara 1 hingga 100.")
    print("Coba tebak angka tersebut!")

    # Generate a random number between 1 and 100
    number_to_guess = random.randint(1, 100)
    attempts = 0

    while True:
        try:
            guess = int(input("Masukkan tebakan Anda: "))
            attempts += 1

            if guess < number_to_guess:
                print("Terlalu rendah! Coba lagi.")
            elif guess > number_to_guess:
                print("Terlalu tinggi! Coba lagi.")
            else:
                print(f"Selamat! Anda menebak angka {number_to_guess} dengan {attempts} percobaan.")
                break
        except ValueError:
            print("Harap masukkan angka yang valid.")

if __name__ == "__main__":
    main()