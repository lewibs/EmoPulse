import json
import datamanager

def main():
    print("\nHey, I hope youre ready to know your depest darkest secrets and problems...")
    print("Anyways lets have some fun and get started :)\n")
    
    dataManager = datamanager.DataManager()

    dataManager.writeData("data")


if __name__ == '__main__':
    main()