# Search Algorithm - uses a binary search to search an ordered list of words
# Louis Slater
# 03/01/23
# for first term programming assessment

# performs a binary search on a given list between indexes
def binary_search(list, search_item, start_index, end_index):
    
    # no indexes left to search
    if start_index > end_index:
        return None # word not found

    # find the middle element of the list
    middle_index=(start_index+end_index)//2
    middle_item = list[middle_index]

    # if the item is found then return the position in the list
    if search_item == middle_item:
        return middle_index + 1

    # recurse through the first half of the list
    if search_item < middle_item:
        return binary_search(list, search_item, start_index, middle_index-1)

    #recurse through second half of the list
    return binary_search(list, search_item, middle_index+1, end_index)

# prepare the user input for a binary search
def search(words, input):
    result = binary_search(words,input.lower(),0 ,len(words)-1)
    if result is None:
        print("Oops, that word cannot be found")
        return

    print("The line number is: " + str(result))

# creates words list from file
def get_words_from_file(filename):
    words=[]
    with open(filename, encoding='UTF-8') as file:
        try:
            for line in file:
                words.append(line.lower().rstrip()) # make all words lower and strip \n or spaces
        except:
            print("failed to read file, make sure the file format is UTF-8")
            quit()

        return words

# start main program
words=get_words_from_file("dictionary.txt")

user_input=input("Enter the name of the item to search:")

search(words, user_input)