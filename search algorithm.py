# Search Algorithm - uses a binary search to search an ordered list of words


def binary_search(list, search_item, start_index, end_index):
    if start_index > end_index:
        return None

    middle_index=(start_index+end_index)//2
    middle_item = list[middle_index]
    print(middle_item)
    if search_item == middle_item:
        return middle_index + 1
    elif search_item < middle_item:
        return binary_search(list, search_item, start_index, middle_index-1)
    else:
        return binary_search(list, search_item, middle_index+1, end_index)

def search(words, input):
    return binary_search(words,input.lower(),0 ,len(words)-1)

def get_words_from_file(filename):
    words=[]
    with open(filename, encoding='UTF-8') as file:
        try:
            for line in file:
                words.append(line.lower().rstrip())
        except:
            print("failed to read file, make sure the file format is UTF-8")
            quit()

        return words

#start
words=get_words_from_file("dictionary.txt")

while True: 
    user_input=input("Enter the name of the item to search:")

    print(search(words, user_input))