from datetime import datetime
from math import log

from django.http import HttpResponseBadRequest


def epoch_seconds(date):
    epoch = datetime(1970, 1, 1)
    min_time = datetime.min.time()
    td = datetime.combine(date, min_time) - epoch
    return td.days * 86400 + td.seconds + (float(td.microseconds)/1000000)

def score(ups, downs):
    return ups + downs

def hot(ups, downs, date):
    s = score(ups, downs)
    order = log(max(abs(s), 1), 10)
    sign = 1 if s > 0 else -1 if s < 0 else 0
    seconds = epoch_seconds(date) - 1134028003
    return round(sign * order + seconds / 45000, 7)
    
def check_has_user_voted(model, user, bulletin):
    try:
        model.objects.get(user=user, bulletin=bulletin)
        return True

    except model.DoesNotExist:
        return False

def cast_vote(bulletin, vote_value, vote):
    vote.has_voted = True
    # Upvote
    if vote_value == 1:
        vote.value = vote_value
        bulletin.upvotes = bulletin.upvotes + 1

        # Calculate score
        age = bulletin.date_created
        score = hot(ups=bulletin.upvotes, downs=bulletin.downvotes, date=age)
        bulletin.score = bulletin.score + score
        bulletin.save()
        vote.save()
    # Downvote
    elif vote_value == -1:
        vote.value = vote_value
        bulletin.downvotes = bulletin.downvotes + 1

        # Calculate score
        age = bulletin.date_created
        score = hot(ups=bulletin.upvotes, downs=bulletin.downvotes, date=age)
        bulletin.score = bulletin.score - score

        bulletin.save()
        vote.save()
    # Cancel vote
    elif vote_value == 0:
        # If user previously downvoted the post
        if vote.value == -1:
            vote.value = 0
            bulletin.downvotes = bulletin.downvotes - 1

            # Calculate score
            age = bulletin.date_created
            score = hot(ups=bulletin.upvotes, downs=bulletin.downvotes, date=age)
            bulletin.score = bulletin.score - score

            bulletin.save()
            vote.save()  

        # If user previously upvoted the post
        elif vote.value == 1:
            vote.value = 0
            bulletin.upvotes = bulletin.upvotes - 1
            
            # Calculate score
            age = bulletin.date_created
            score = hot(ups=bulletin.upvotes, downs=bulletin.downvotes, date=age)
            bulletin.score =  bulletin.score - score

            bulletin.save()
            vote.save()  
        elif vote.value == 0:
            pass

    else:
        return HttpResponseBadRequest()
