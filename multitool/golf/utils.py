from datetime import datetime, date

def is_null(result):
    try:
        test = result[0]
    except:
        return 1
    else:
        return 0

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
    course_list = []
    course_avg_dict = {}
    for course in golf_courses:
        Course = {}
        Course['name'] = course.name
        course_pars = []
        course_pars.extend((course.h1Par, course.h2Par, course.h3Par, course.h4Par, course.h5Par, course.h6Par, course.h7Par, course.h8Par,
                        course.h9Par, course.h10Par, course.h11Par, course.h12Par, course.h13Par, course.h14Par, course.h15Par, course.h16Par,
                        course.h17Par, course.h18Par))
        Course['pars'] = course_pars
        course_list.append(Course)   
        course_key = course.name
        course_key = course_key.replace(" ", "_")
        course_avg_dict[course_key] = {'par_3_total': 0, 'par_3_cnt': 0, 'par_4_total': 0, 'par_4_cnt': 0, 'par_5_total': 0, 'par_5_cnt': 0}

    par_3_total = 0
    par_4_total = 0
    par_5_total = 0
    par_3_cnt = 0
    par_4_cnt = 0
    par_5_cnt = 0
    par_3_avg = 0
    par_4_avg = 0
    par_5_avg = 0
    if is_null(golf_rounds) is 0:
        for golf_round in golf_rounds:
            course_name = golf_round.course_played
            scores = []
            scores.extend((golf_round.h1Score, golf_round.h2Score, golf_round.h3Score, golf_round.h4Score, golf_round.h5Score, golf_round.h6Score, golf_round.h7Score, golf_round.h8Score,
                            golf_round.h9Score, golf_round.h10Score, golf_round.h11Score, golf_round.h12Score, golf_round.h13Score, golf_round.h14Score, golf_round.h15Score, golf_round.h16Score,
                            golf_round.h17Score, golf_round.h18Score))
            for course in course_list:
                index = 0
                if course['name'] == course_name:
                    while True:
                        course_key = course_name
                        course_key = course_key.replace(" ", "_")
                        course_avg = course_avg_dict[course_key]

                        score = scores[index]
                        pars = course['pars']
                        if score == 0:
                            break
                        
                        if pars[index] == 3:
                            course_avg['par_3_total'] += 1
                            course_avg['par_3_cnt'] += score
                            par_3_total += 1
                            par_3_cnt += score
                        elif pars[index] == 4:
                            course_avg['par_4_total'] += 1
                            course_avg['par_4_cnt'] += score
                            par_4_total += 1
                            par_4_cnt += score
                        elif pars[index] == 5:
                            course_avg['par_5_total'] += 1
                            course_avg['par_5_cnt'] += score
                            par_5_total += 1
                            par_5_cnt += score
                        else:
                            break
                        index += 1
                        if index > 17:
                            break
        try:
            for course in golf_courses:
                course_key = course.name
                course_key = course_key.replace(" ", "_")
                course_obj = course_avg_dict[course_key] 
                if course_obj['par_3_total'] > 0:
                    course_obj['par_3_avg'] = round(course_obj['par_3_cnt']/course_obj['par_3_total'],2)
                else:
                    course_obj['par_3_avg'] = 0

                if course_obj['par_4_total'] > 0:
                    course_obj['par_4_avg'] = round(course_obj['par_4_cnt']/course_obj['par_4_total'],2)
                else:
                    course_obj['par_4_avg'] = 0

                if course_obj['par_5_total'] > 0:
                    course_obj['par_5_avg'] = round(course_obj['par_5_cnt']/course_obj['par_5_total'],2)
                else:
                    course_obj['par_5_avg'] = 0
                
            par_3_avg = round(par_3_cnt/par_3_total,2)
            par_4_avg = round(par_4_cnt/par_4_total,2)
            par_5_avg = round(par_5_cnt/par_5_total,2)

            total = {}
            total['par_3_avg'] = par_3_avg
            total['par_4_avg'] = par_4_avg
            total['par_5_avg'] = par_5_avg

            course_avg_dict['Total'] = total
        except:
            print(':(')

    # Payload['par_3_avg'] = par_3_avg
    # Payload['par_4_avg'] = par_4_avg
    # Payload['par_5_avg'] = par_5_avg
    # return Payload
    return course_avg_dict