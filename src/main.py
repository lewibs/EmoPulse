import boosted
import daylio

def main():
    print("Hey, I hope youre ready to know your depest darkest secrets and problems...")
    print("Anyways lets have some fun and get started :)")
    boostedManager = boosted.Boosted()
    daylioManager = daylio.Daylio()

    print(boostedManager._data)
    print(daylioManager._data)


if __name__ == '__main__':
    main()