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

def get_par_averages(golf_courses, golf_rounds):
    Payload = {}
    courseList = []
    for course in golf_courses:
        Course = {}
        Course['name'] = course.name
        course_pars = []
        course_pars.extend((course.h1Par, course.h2Par, course.h3Par, course.h4Par, course.h5Par, course.h6Par, course.h7Par, course.h8Par,
                        course.h9Par, course.h10Par, course.h11Par, course.h12Par, course.h13Par, course.h14Par, course.h15Par, course.h16Par,
                        course.h17Par, course.h18Par))
        Course['pars'] = course_pars
        courseList.append(Course)    

    par3Total = 0
    par4Total = 0
    par5Total = 0
    par3Cnt = 0
    par4Cnt = 0
    par5Cnt = 0
    if golf_rounds.count() > 0:
        for golf_round in golf_rounds:
            courseName = golf_round.course_played
            scores = []
            scores.extend((golf_round.h1Score, golf_round.h2Score, golf_round.h3Score, golf_round.h4Score, golf_round.h5Score, golf_round.h6Score, golf_round.h7Score, golf_round.h8Score,
                            golf_round.h9Score, golf_round.h10Score, golf_round.h11Score, golf_round.h12Score, golf_round.h13Score, golf_round.h14Score, golf_round.h15Score, golf_round.h16Score,
                            golf_round.h17Score, golf_round.h18Score))
            for course in courseList:
                index = 0
                if course['name'] == courseName:
                    while True:
                        score = scores[index]
                        pars = course['pars']
                        if score == 0:
                            break
                        
                        if pars[index] == 3:
                            par3Total += 1
                            par3Cnt += score
                        elif pars[index] == 4:
                            par4Total += 1
                            par4Cnt += score
                        elif pars[index] == 5:
                            par5Total += 1
                            par5Cnt += score
                        else:
                            break
                        index += 1
                        if index > 17:
                            break
        par3Avg = round(par3Cnt/par3Total,2)
        par4Avg = round(par4Cnt/par4Total,2)
        par5Avg = round(par5Cnt/par5Total,2)
    else:
        par3Avg = 0
        par4Avg = 0
        par5Avg = 0

    Payload['par3Avg'] = par3Avg
    Payload['par4Avg'] = par4Avg
    Payload['par5Avg'] = par5Avg
    return Payload