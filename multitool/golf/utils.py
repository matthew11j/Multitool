from datetime import datetime, date

def submit_round(form):
    # Calculating front, back, total Scores
    # Defaulting empty scores
    scores = []
    scores.extend((form.h1Score, form.h2Score, form.h3Score, form.h4Score, form.h5Score, form.h6Score, form.h7Score, form.h8Score,
                        form.h9Score, form.h10Score, form.h11Score, form.h12Score, form.h13Score, form.h14Score, form.h15Score, form.h16Score,
                        form.h17Score, form.h18Score))
    front = 0
    back = 0
    cnt = 0
    for score in scores:
        if not score.data:
            score.data = 0
        int_score = int(score.data)
        if cnt < 9:
            front = front + int_score
        else:
            back = back + int_score
        cnt = cnt + 1
    total = back + front

    # Defaulting empty putts
    putts = []
    putts.extend((form.h1Putt, form.h2Putt, form.h3Putt, form.h4Putt, form.h5Putt, form.h6Putt, form.h7Putt, form.h8Putt,
                        form.h9Putt, form.h10Putt, form.h11Putt, form.h12Putt, form.h13Putt, form.h14Putt, form.h15Putt, form.h16Putt,
                        form.h17Putt, form.h18Putt))
    for putt in putts:
        if not putt.data:
            putt.data = 0

    if not form.date_played.data:
        form.date_played.data = date(2020,1,1)

    form.frontScore.data = front
    form.backScore.data = back
    form.totalScore.data = total
     
    return form