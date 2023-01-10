import itertools
from string import digits, punctuation, ascii_letters
import win32com.client as client
from datetime import datetime
import time


# symbols = digits + punctuation + ascii_letters
# print(symbols)


def brut_excel_doc():
    print("***Hello friend!***")

    try:
        password_length = input("Введите длину пароля, от скольки - до скольки символов, например 3 - 7: ")
        password_length = [int(item) for item in password_length.split("-")]
    except:
        print("проверьте введенные данные")

    print("Если пароль содержит только цифры, введите: 1\nЕсли пароль содержит только буквы, введите: 2\n"
          "Если пароль содержит цифры и буквы, введите: 3\nЕсли пароль содержит цифры, буквы и спецсимволы, введите: 4")

    try:
        choise = int(input(": "))
        if choise == 1:
            possible_symbols = digits
        elif choise == 2:
            possible_symbols = ascii_letters
        elif choise == 3:
            possible_symbols = digits + ascii_letters
        elif choise == 4:
            possible_symbols = digits + ascii_letters + punctuation
        else:
            possible_symbols = "О.о что ты хочешь?"
        print(possible_symbols)
    except:
        print("О.о что ты хочешь?")

    # brute excel doc
    start_timestamp = time.time()
    print(f"Started of - {datetime.utcfromtimestamp(time.time()).strftime('%H:%M:%S')}")

    count = 0
    for pass_length in range(password_length[0], password_length[1] + 1):
        for password in itertools.product(possible_symbols, repeat=pass_length):
            password = "".join(password)
            #print(password)

            opened_doc = client.Dispatch("Excel.Application")
            count += 1

            try:
                opened_doc.Workbooks.Open(
                    r"C:\Users\Dell\PycharmProjects\NewsPars\parolpach\nomer.xlsx",
                    False,
                    True,
                    None,
                    password
                )

                time.sleep(0.1)
                print(f"Finished at - {datetime.utcfromtimestamp(time.time()).strftime('%H:%M:%S')}")
                print(f"Password cracking time - {time.time() - start_timestamp}")

                return print(f"Attempt #{count} Password is: {password}")
            except:
                print(f"Attempt #{count} Incorrect {password}")
                pass



def main():
    brut_excel_doc()


if __name__ == "__main__":
    main()