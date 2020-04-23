import facebook
import json
import requests
from collections import defaultdict

dict = defaultdict(lambda: [])


def main():
    token = {
        "EAAIjVZBfuKaYBALib1Cfegscp2NBZBlV4ZCplUlZBrl6yP6MYh29S9pGiZCRHA0PaHq2lBOMVBdYFvPoiU4WZBa5YhYnmbGJnxTs1ycup4FwC9joT6YWyMVgbTvZBGUHFiUiTZBbsyI8rfQxK7qKpa7UMbCU558AZAkwKZBiVozCltsWWoaS0Hrmz466mrmWszId7hSxED1WSsngZDZD"}
    graph = facebook.GraphAPI(token)
    fields = ['id', 'posts']
    profile = graph.get_object('me', fields=fields)
    print(profile)  # (json.dumps(profile, indent=4))

    my_function(profile['posts'])

    POSTS = "posts"
    PAGING = "paging"
    NEXT = "next"

    while True:
        print("after")

        if POSTS in profile and PAGING in profile[POSTS] and NEXT in profile[POSTS][PAGING]:
            profile = requests.get(profile[POSTS][PAGING][NEXT]).json()
        elif PAGING in profile and NEXT in profile[PAGING]:
            profile = requests.get(profile[PAGING][NEXT]).json()
        else:
            print("end", profile)
            break

        print(profile)
        my_function(profile)


def my_function(posts):
    places = ["נחל השופט", "נחל פרת", "עין ירקעם", "תל שוכה", "מעיין באר אבא", "נחל שוקק", "נחל חדרה", "נחל ציפורי",
              "נחל שורק", "עין הנציב", "מעיין בית הקשתות", "עין פלוטית -מעיין האהבה", "מעיין חובה",
              "עין יבקע - מעיין הסוסים", "עין מוקש", "מעיין מרים"
                                                     "עין מבוע", "עין אשקף", "עין לימון (עין לימור)",
              "עין שוירח (עין שריר)", "מעיין דביר", "עין ספיר", "סטף", "עין יבקע", "ליפתא", "עין עוזי", "עים דביר",
              "עין שריג", "עין חינדק", "עין לבן", "עין איתמר", "עין ורד", "עין תמר", "עין טייסים"]
    MESSAGE = 'message'
    for post in posts['data']:
        for place in places:
            if MESSAGE in post and place in post[MESSAGE]:
                print(post)
                dict[place].append(post)

with open('post.txt', 'w', encoding='utf-8') as f:

#  fields = ['id','posts']


 if __name__=="__main__":
     main()
     print(dict)
     f.writelines(dict)
     print(repr(dict))
