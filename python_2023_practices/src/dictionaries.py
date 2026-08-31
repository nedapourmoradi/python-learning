
# dictionary 
book_genre = {
    'fiction': 'Harry Potter',
    'literature': 'To be or not to be',
    'history': 'Alexandra',
    'novel': 'The Great Gatsby'
}

print(book_genre['fiction'])

book_genre.update({
    'literary_fiction': 'Harry Potter',
    'fiction': 'Harry Potter'
})

book_genre.update({
    'metaphysics': 'The Journey of Soul'
})

book_genre.pop('history')

del book_genre['novel']

###
print(book_genre.keys())
print(book_genre.values())

squared_number = {
    key: key ** 2
    for key in range(10)
}

print(squared_number)


###
library = {
    'metaphysics': {
        'The Journey of Soul',
        'The Power of Now'
    },
    'novel': {
        'The Great Gatsby',
        'Pride and Prejudice'
    },
}

print(library)


###
city_presence = {
    'New York': True,
    'Berlin': True,
    'Tokyo': True,
    'Sydney': True
}

print('London' in city_presence)
print('Tokyo' in city_presence)

student_score = {
    'Alice': 88,
    'Bob': 95
}


###
student_score.setdefault('Bob', 2)
student_score.setdefault('Charlie', 0)

print(student_score)


###
preferences = {
    'color': 'blue',
    'food': 'pizza',
    'drink': 'water'
}

preferences.update({'drink': 'orange juice'})

print(preferences)


###
stock_A = {
    'apples': 5,
    'oranges': 7
}

stock_B = {
    'oranges': 12,
    'bananas': 3
}

stock_A.update(stock_B)

print(stock_A)


####
account_info = {
    'user1': {
        'name': 'Alice',
        'password': 'alice123'
    },
    'user2': {
        'name': 'Bob',
        'password': 'bobsecure'
    }
}

print(account_info['user1']['password'])

account_info['user2']['name'] = 'Jack'

print(account_info)

