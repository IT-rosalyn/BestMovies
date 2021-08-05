import os
import numpy as np
os.environ.setdefault('DJANGO_SETTINGS_MODULE','Best_movies_project.settings')

import django
django.setup()
from Best_movies.models import Movie,Review
def populate():

    for c in Movie.objects.all():
        rate_list = []
        for p in Review.objects.filter(movie=c):

            rate_list.append(p.rating)

        if len(rate_list):
            print(c.name,"mean:",np.mean(rate_list))
            c.people=len(rate_list)
            c.average_rating=np.mean(rate_list)
            c.save()
if __name__=="__main__":
    print("starting")
    populate()
