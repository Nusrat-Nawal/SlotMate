def calculate_score(req1, req2):
    score = 0

    # COURSE (35)
    if req1.current_course_code == req2.preferred_course_code:
        score += 35

    # SECTION (20)
    if req2.any_section or req2.preferred_section:
        score += 16
    elif req1.current_section == req2.preferred_section:
        score += 20

    # TIME (15)
    if req2.any_time or req2.preferred_time:
        score += 12
    elif req1.current_time == req2.preferred_time:
        score += 15

    # DAY (15)
    if req2.any_day or req2.preferred_days:
        score += 12
    else:
        days1 = set((req1.current_days or "").split(","))
        days2 = set((req2.preferred_days or "").split(","))

        overlap = days1 & days2
        
        if not days2:
             score += 12
        elif len(overlap) == len(days2):
            score += 15
        elif len(overlap) > 0:
            score += 12

    # FACULTY (15)
    if req2.any_faculty or req2.preferred_faculty:
        score += 12
    elif req1.current_faculty == req2.preferred_faculty:
        score += 15

    return score

#Mutual Matching score
def calculate_mutual_score(req_a, req_b):
    a_to_b = calculate_score(req_a, req_b)
    b_to_a = calculate_score(req_b, req_a)

    mutual = (a_to_b + b_to_a) / 2

    return a_to_b, b_to_a, mutual