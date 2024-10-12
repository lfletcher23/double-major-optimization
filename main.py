from Model import user_functions as usr

# program keys input: a list containing either "MATH_MAJOR", "OIE_MAJOR", or both
program_keys = ["MATH_MAJOR", "OIE_MAJOR"]

# must be in the format DEPT_NUM, ex "OIE_2081"
# program does not check for course validity, unrecognized courses assumed to be 3 credits
#courses_taken = ["MA_1021", "MA_1022", "MA_1023", "PH_1110", "CH_1010", "ES_2001", "WR_2001"]

# output will be a txt, do not add .txt to the end
usr.run_model(program_keys, courses_taken, write_output=True, output_name="my_schedule")


