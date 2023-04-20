import os.path

# this makes a function which requests that the user inputs a valid file path and then returns the path
def makeFileRequester(name):
    def fileRequester():
        path = input(f'Please input the file path for {name}: ')
        
        if os.path.isfile(path):
            return path
        else:
            print("Error: not a valid file.")
            return fileRequester()


    return fileRequester