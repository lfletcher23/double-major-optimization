import json
import math

def format_solution(x, y, base_dict, program_keys, courses_taken_dict):
    raw_y = raw_y_sol(y)
    raw_x = raw_x_sol(x)
    after_enum = enum_solution_courses(raw_y, courses_taken_dict, base_dict["Buckets"])
    courses_set = after_enum["Solution Courses"]
    to_take = after_enum["To Take"]
    applied = apply_to_programs(courses_set, raw_x, base_dict, program_keys, to_take)
    return applied

def raw_x_sol(x):
    result_dict = {}
    for key, val in x.items():
        bucket = key[0]
        req = key[1]
        val_num = val.varValue
        if val_num > 0:
            if req not in result_dict.keys():
                result_dict[req] = {}
            result_dict[req][bucket] = val_num

    return result_dict

def raw_y_sol(y_dict):
    new_y = {}
    for key, val in y_dict.items():
        new_y[key] = val.varValue
    return new_y


def enum_solution_courses(y_dict, courses_taken_ref, buckets_ref):
    to_take = []
    solution_courses = {}
    for bucket, bucket_attrs in buckets_ref.items():
        already_taken = courses_taken_ref[bucket]["List of Courses"]
        num_new = y_dict[bucket]
        total_courses = int(num_new) + len(already_taken)
        capacity = bucket_attrs["Bucket Size"]
        courses_list = []
        if int(capacity) == total_courses:
            for each_course in bucket_attrs["Bucket Contents"]:
                courses_list.append(each_course)
                if each_course not in already_taken:
                    to_take.append(each_course)
        else:
            courses_list = already_taken.copy()
            for i in range(int(num_new)):
                courses_list.append(bucket)
                to_take.append(bucket)
        if len(courses_list) > 0:
            solution_courses[bucket] = courses_list

    solution_courses["OTHER_TAKEN"] = courses_taken_ref["OTHER_TAKEN"]["List of Courses"]
    super_dict= {"Solution Courses": solution_courses, "To Take": to_take}
    return super_dict

def get_total_used(sol_courses, program_keys, track_applied):
    total_used = {}
    for bucket_key in sol_courses.keys():
        num_used = 0
        for each_program in program_keys:
            used_per_program = track_applied[each_program][bucket_key]
            num_used = max(used_per_program, num_used)
        total_used[bucket_key] = num_used

    return total_used

def count_credits_used(total_used, buckets_ref):
    credits_used = 0
    for bucket_key, num_used in total_used.items():
        if num_used > 0:
            credits_used += buckets_ref[bucket_key]["Credits Each"] * num_used
    return credits_used

def make_track_applied(program_keys, sol_courses):
    track_applied = {}
    for each_program in program_keys:
        track_applied[each_program] = {}
        for bucket_name, course_list in sol_courses.items():
            track_applied[each_program][bucket_name] = 0

    return track_applied

def calc_credit_metrics(stageI_obj, credits_taken, orig_credits_used, num_majors):
    mqp_credits = 9 + 3 * (num_majors - 1)
    pe_credits = 3
    anticip_total = stageI_obj + credits_taken + mqp_credits + pe_credits
    min_needed = max(orig_credits_used + mqp_credits + pe_credits, 135)

    not_used_credits = max(anticip_total - min_needed, 0)
    free_credits = max(min_needed - anticip_total, 0)

    taken_and_used = credits_taken - not_used_credits
    num_left = stageI_obj + mqp_credits + pe_credits + free_credits

    taken_and_to_take = credits_taken + num_left

    counts_dict = {"Taken and Used": taken_and_used, "Stage I obj": stageI_obj, "PE": float(pe_credits), 
    "MQP": float(mqp_credits), "Free credits": float(free_credits), "Not used": not_used_credits, 
    "Min total": float(min_needed), "Number Left": num_left, "Total taken": float(credits_taken),
    "Total": taken_and_to_take}
    
    return counts_dict


def apply_to_programs(sol_courses, x_dict, base_dict, program_keys, to_take):
    result_dict = {}
    track_applied = make_track_applied(program_keys, sol_courses)
    
    # apply courses
    result_dict["ALL_MAJORS"] = apply_courses_helper("ALL_MAJORS", program_keys, sol_courses, track_applied, x_dict, base_dict, to_take)
    for each_program in program_keys:
        result_dict[each_program] = apply_courses_helper(each_program, [each_program], sol_courses, track_applied, x_dict, base_dict, to_take)

    if len(program_keys) > 1:
        total_used_dict = get_total_used(sol_courses, program_keys, track_applied)
    else:
        total_used_dict = track_applied[program_keys[0]]

    credits_used = count_credits_used(total_used_dict, base_dict["Buckets"])
    anticip_credits = 3 + 9 + 3 * (len(program_keys) - 1)
    elect_credits = max(135 - (credits_used + anticip_credits), 0)
    
    elect_credits_left = elect_credits
    elect_courses_list = []
    not_used_list = []
    for bucket_key, bucket_courses in sol_courses.items():
        current_index = total_used_dict[bucket_key]
        for i in range(int(current_index), len(bucket_courses)):
            new_course = get_course_name(bucket_courses[i], base_dict["Buckets"], to_take)
            if elect_credits_left > 0:
                elect_courses_list.append(new_course)
                elect_credits_left += -3
            else:
                not_used_list.append(new_course)
    
    if elect_credits_left > 0:
        courses_needed = math.ceil(elect_credits_left / 3)
        for i in range(courses_needed):
            elect_courses_list.append("[FREE ELECTIVE]")
            to_take.append("FREE ELECTIVE")

    result_dict["ALL_MAJORS"]["Free Electives"] = elect_courses_list
    result_dict["ALL_MAJORS"]["Not used"] = not_used_list

    credit_counts = {"Credits Used": credits_used}
    super_dict = {"Results": result_dict, "Credit Counts": credit_counts}

    return super_dict
                
def apply_courses_helper(program_key, programs_to_count_toward, sol_courses, track_applied, x_dict, base_dict, to_take):
    current_reqs_dict = base_dict[program_key]["Reqs"]
    buckets_ref = base_dict["Buckets"]
    result_dict = {}
    for req, req_attrs in current_reqs_dict.items():
        course_list = []
        req_assigns = x_dict[req]

        for bucket_key, bucket_num in req_assigns.items():
            bucket_courses = sol_courses[bucket_key]
            for i in range(int(bucket_num)):

                current_index = track_applied[programs_to_count_toward[0]][bucket_key]
                course_name = get_course_name(bucket_courses[current_index], buckets_ref, to_take)
                course_list.append(course_name)

                for each_program in programs_to_count_toward:
                    track_applied[each_program][bucket_key] += 1

        req_name = req_attrs["Req Description"]
        if req_name not in result_dict.keys():
            result_dict[req_name] = []
        result_dict[req_name] += course_list
        result_dict[req_name].sort()

    return result_dict

def get_course_name(bucket_key, buckets_ref, to_take):
    if bucket_key in buckets_ref.keys():
        course_name = buckets_ref[bucket_key]["Bucket Description"]
    else:
        split_up = bucket_key.split("_")
        course_name = split_up[0] + " " + split_up[1]
    if bucket_key in to_take:
        course_name = "[" + course_name + "]"
    return course_name

