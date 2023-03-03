from Model import create_model as cm
from pulp import *

def run_model(program_keys, courses_taken_dict, base_dict, name_prefix, write_LP=False):
    
    model = LpProblem("SchedulingCourses", LpMinimize)
    vars_dict = cm.setup_x_y_vars(model, base_dict, program_keys, courses_taken_dict)
    cm.add_requirement_constraints(model, vars_dict["X"], program_keys, base_dict)
    track_SRs = cm.add_sreqs(model, vars_dict["X"], program_keys, base_dict)
    
    cm.set_objective(model, vars_dict["Y"], base_dict["Buckets"], 1)
    record_LP(model, write_LP, 1, name_prefix)
    model.solve(PULP_CBC_CMD(msg=0))
    min_cred = model.objective.value()
    stage1_delta = model.solutionTime

    cm.set_objective(model, vars_dict["Y"], base_dict["Buckets"], 2, max_credits = min_cred)
    record_LP(model, write_LP, 2, name_prefix)
    model.solve(PULP_CBC_CMD(msg=0))
    stage2_delta = model.solutionTime

    vars_dict["Solve Times"] = {"Stage I": stage1_delta, "Stage II": stage2_delta}
    vars_dict["Objectives"] = {"Stage I": min_cred, "Stage II": model.objective.value()}

    return vars_dict

def setup_courses_taken(courses_list, buckets_dict):
    credits_taken = 0
    matches_ref = match_taken_courses(courses_list, buckets_dict)
    taken_ref = make_empty_taken_ref(buckets_dict)
    for course, buckets in matches_ref.items():
        matched_bucket = "No match found"
        if len(buckets) == 1:
            matched_bucket = buckets[0]
        elif len(buckets) > 1:
            matched_bucket = choose_correct_bucket(course, buckets, buckets_dict)
        
        if matched_bucket != "No match found":
            taken_ref[matched_bucket]["Taken"] += 1
            taken_ref[matched_bucket]["List of Courses"].append(course)
            credits_taken += buckets_dict[matched_bucket]["Credits Each"]
        else:
            taken_ref["OTHER_TAKEN"]["Taken"] += 1
            taken_ref["OTHER_TAKEN"]["List of Courses"].append(course)
            taken_ref["OTHER_TAKEN"]["Bucket Size"] += 1
            credits_taken += 3
    larger_dict = {"Taken Ref": taken_ref, "Credits Taken": credits_taken}
    return larger_dict

def get_program_run_name(program_keys):
    if len(program_keys) < 2:
        program_run_name = program_keys[0] + "_ONLY"
    else:
        major_keys = []
        for each_program in program_keys:
            major_keys.append(each_program.split("_")[0])
        major_keys.sort()
        program_run_name = major_keys[0] + "_" + major_keys[1] + "_DOUBLE"
    return program_run_name

def record_LP(model, to_write, stage_num, name_prefix):
    if to_write:
        file_name = name_prefix + "_LP_stage" + str(stage_num) + ".lp"
        model.writeLP(file_name)
        print("LP written to:")
        print(file_name)

def match_taken_courses(courses_list, buckets_dict):
    matches_ref = {}
    for each_course in courses_list:
        matches_ref[each_course] = []
        course_dept = each_course.split("_")[0]
        search_string = course_dept + "_DEPT"
        
        for key, val in buckets_dict.items():
            contents = val["Bucket Contents"]
            for each_item in contents:
                if each_course == each_item:
                    matches_ref[each_course].append(key)
                    break
                elif search_string == each_item[:len(search_string)]:
                    matches_ref[each_course].append(key)

    return matches_ref


def make_empty_taken_ref(buckets_dict):
    taken_ref = {}
    for key, val in buckets_dict.items():
        taken_ref[key] = {}
        taken_ref[key]["Bucket Size"] = val["Bucket Size"]
        taken_ref[key]["List of Courses"] = []
        taken_ref[key]["Taken"] = 0
        
    taken_ref["OTHER_TAKEN"] = {}
    taken_ref["OTHER_TAKEN"]["Bucket Size"] = 0
    taken_ref["OTHER_TAKEN"]["List of Courses"] = []
    taken_ref["OTHER_TAKEN"]["Taken"] = 0
    return taken_ref


def choose_correct_bucket(course, buckets_list, buckets_dict):
    exact_match = False
    level_match = False
    dept_match = False
    
    split_course = course.split("_")
    course_dept = split_course[0]
    course_level = split_course[1][0]
    dept_match_key = course_dept + "_DEPT"
    level_match_key = course_dept + "_DEPT_" + str(course_level) + "000_L"
    matched_bucket = "No match found"
    for each_bucket in buckets_list:
        if not exact_match:
            contents = buckets_dict[each_bucket]["Bucket Contents"]
            if course in contents:
                exact_match = True
                matched_bucket = each_bucket
            elif not exact_match and level_match_key in contents:
                level_match = True
                matched_bucket = each_bucket
            elif not level_match and not exact_match and dept_match_key in contents:
                dept_match = True
                matched_bucket = each_bucket
    return matched_bucket