#!/usr/bin/env python

import sys
import csv
import random
import math
import operator

# Recommender constants
NUM_RATINGS = 20
NUM_NEIGHBOURHOODS = 10
NUM_RECOMMENDATIONS = 20
MIN_RATING_RECOMMENDATION = 4
RANDOM_RATINGS = False

# Terminal color constants
PINK = '\033[95m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
ENDCOLOR = '\033[0m'


def ReverseSortAndTrimDictionary(dictionary, max_results):
    """ Sort in reverse order and cut dictionary to fit a maximum value"""

    sorted_dictionary = sorted(dictionary.items(), key=operator.itemgetter(1))
    sorted_dictionary.reverse()

    result = []
    i = 1
    for k, v in sorted_dictionary:
        result.append(k)
        if i >= max_results:
            break
        i += 1

    return result


def Average(user):
    """ Get the average rating from an user movies dictionary """

    average = 0
    for id_movie in user:
        average += user[id_movie]

    return average / len(user)


def Neighbors(allRatings, userRatings):
    """ Find the k-nearest neighbours """

    neighbors = {}

    userAverage = Average(userRatings)

    for user in allRatings:

        matches = []

        for movie_id in userRatings:

            if movie_id in allRatings[user]:
                matches.append(movie_id)

        matchRate = 0

        if len(matches):

            numerator = 0.0
            userDenominator = 0.0
            otherUserDenominator = 0.0

            for movie in matches:

                u = userRatings[movie] - userAverage
                v = allRatings[user][movie] - Average(allRatings[user])
                numerator += u * v
                userDenominator += u * u
                otherUserDenominator += v * v

            if userDenominator == 0 or otherUserDenominator == 0:
                matchRate = 0
            else:
                matchRate = numerator / math.sqrt(userDenominator) * math.sqrt(otherUserDenominator)

            if matchRate > 0:
                neighbors[user] = matchRate

    sorted_neighbors = ReverseSortAndTrimDictionary(neighbors, NUM_NEIGHBOURHOODS)
    result = {}
    for neighbor in sorted_neighbors:
        result[neighbor] = neighbors[neighbor]

    return result


def Recommendations(allRatings, userRatings, neighbors, movies):
    """ Get recommendation based on neighbor ratings """

    userAverage = Average(userRatings)

    predictedRatings = {}

    for movie in movies:
        if movie not in userRatings:

            numerator = 0.0
            denominator = 0.0

            for neighbor in neighbors:
                if movie in allRatings[neighbor]:

                    matchRate = float(neighbors[neighbor])

                    numerator += float(matchRate * (allRatings[neighbor][movie] - Average(allRatings[neighbor])))
                    denominator += abs(matchRate)

            predictedRating = 0.0
            if (denominator > 0):
                predictedRating = float(userAverage + float(numerator / denominator))

                # Uncomment this to limit the predicted ratings to 5
                # if (predictedRating > 5):
                #     predictedRating = 5

            if predictedRating >= MIN_RATING_RECOMMENDATION:
                predictedRatings[movie] = float(predictedRating)

    return predictedRatings


def ReadMovies(file):
    csvfile = open(file)
    csvreader = csv.reader(csvfile, delimiter='|')
    movies = {}
    for row in csvreader:
        id_movie = int(row[0])
        title_movie = row[1]
        movies[id_movie] = title_movie.decode('unicode_escape')
    csvfile.close()
    return movies


def ReadRatings(file):
    csvfile = open(file)
    csvreader = csv.reader(csvfile, delimiter='\t')
    ratings = []
    for row in csvreader:
        ratings.append(row)
    csvfile.close()

    return ratings


def CreateRatingsDictionary(ratings):
    """ Create an optimized dictionary with user ratings"""

    allRatings = {}
    for n in range(1, len(ratings)):
        allRatings[n] = {}

    for row in ratings:
        id_user = int(row[0])
        id_movie = int(row[1])
        rating = int(row[2])
        allRatings[id_user][id_movie] = rating

    return allRatings


if __name__ == "__main__":
    """ Program entrypoint """

    if len(sys.argv) == 2 and sys.argv[1] == 'auto':
        RANDOM_RATINGS = True

    movies = ReadMovies('ml-data/u.item')
    ratings = ReadRatings('ml-data/u.data')
    allRatings = CreateRatingsDictionary(ratings)

    print("%s+------------------+" % PINK)
    print("%s| User data:       |" % PINK)
    print("%s+------------------+ %s" % (PINK, ENDCOLOR))

    # Get a random dictionary of NUM_RATINGS movies
    sample = dict((k, movies[k]) for k in random.sample(movies, NUM_RATINGS))
    userRatings = {}

    for movie_id in sample:
        movie_title = sample[movie_id]

        rating = random.randint(1, 5)

        if not RANDOM_RATINGS:
            while True:
                try:
                    rating = int(raw_input("Enter rating for '%s': " % movie_title))
                    if rating < 1 or rating > 5:
                        raise ValueError
                    break
                except ValueError:
                    print("%sPlease, enter a number between 1 and 5.%s" % (YELLOW, ENDCOLOR))

        print("%s%s%s \t %s" % (BLUE, ("*" * rating), ENDCOLOR, movie_title))

        userRatings[movie_id] = rating

    neighborhoods = Neighbors(allRatings, userRatings)
    recommendations = Recommendations(allRatings, userRatings, neighborhoods, movies)

    print("%s+------------------+" % PINK)
    print("%s| Recommendations: |" % PINK)
    print("%s+------------------+" % PINK)

    trimmed = ReverseSortAndTrimDictionary(recommendations, NUM_RECOMMENDATIONS)

    for movie_id in trimmed:
        print("%s%f%s: %s" % (GREEN, recommendations[movie_id], ENDCOLOR, movies[movie_id]))
        # print("%s%d%s: %s" % (GREEN, recommendations[movie_id], ENDCOLOR, movies[movie_id]))
