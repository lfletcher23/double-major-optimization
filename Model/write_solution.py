    
def write_output_file(file_name, solution, program_keys, run_times, counts_dict, major_names):
    save_name = file_name + ".txt"
    effective_keys = ["ALL_MAJORS"] + program_keys
    with open(save_name, "w") as sol_f:
        
        sol_f.write("\n<<<<<<<<<<<<< Credits >>>>>>>>>>>>>\n \n")
        sol_f.write(str(counts_dict["Total"]))
        sol_f.write(" TOTAL")
        sol_f.write("\n-------------------------------\n")
        sol_f.write(str(counts_dict["Number Left"]))
        sol_f.write(" REMAINING \n    ")
        sol_f.write(str(counts_dict["Stage I obj"]))
        sol_f.write(" Academic Courses \n    ")
        sol_f.write(str(counts_dict["Free credits"]))
        sol_f.write(" Free Electives \n    ")
        sol_f.write(str(counts_dict["MQP"]))
        sol_f.write(" MQP \n    ")
        sol_f.write(str(counts_dict["PE"]))
        sol_f.write(" PE")
        sol_f.write("\n \n")
        sol_f.write(str(counts_dict["Total taken"]))
        sol_f.write(" TAKEN\n    ")
        sol_f.write(str(counts_dict["Taken and Used"]))
        sol_f.write(" Applied\n    ")
        sol_f.write(str(counts_dict["Not used"]))
        sol_f.write(" Excess\n")

        
        sol_f.write("\n\n<<<<<<<<<<<<< Run Time >>>>>>>>>>>>>")
        sol_f.write("\n\nTOTAL RUN TIME: ")
        sol_f.write(str(run_times["Entire Run Total"]))
        sol_f.write("\n----------------------------------------\n    ")
        sol_f.write("Stage I solve: ")
        sol_f.write(str(run_times["Stage I Solve"]))
        sol_f.write("\n    ")
        sol_f.write("Stage II solve: ")
        sol_f.write(str(run_times["Stage II Solve"]))


        sol_f.write("\n\n\n<<<<<<<<<<<<< Tracking Sheet >>>>>>>>>>>>>\n")
        sol_f.write("[Brackets indicate courses that have yet to be taken] \n \n")
        for each_program in effective_keys:
            program_name = major_names[each_program]
            sol_f.write(program_name)
            sol_f.write("\n____________________________________\n")
            sol_f.write("\n \n")
            for req_name, req_courses in solution[each_program].items():
                sol_f.write(req_name)
                sol_f.write("\n")
                sol_f.write("----------------------------\n")
                for each_course in req_courses:
                    sol_f.write("    ")
                    sol_f.write(each_course)
                    sol_f.write("\n")
                sol_f.write("\n")
            sol_f.write("\n \n")

    print("Output saved to:")
    print(save_name)
