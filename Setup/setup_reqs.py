import basic_data_funcs as bd

def upload_reqs(reqs_upload, req_sreq_fields):
    reqs_df = reqs_upload["Reqs"]
    sreqs_df = reqs_upload["Sreqs"]
    
    starting_reqs_dict = bd.df_to_dict_of_lists(reqs_df, req_sreq_fields["REQ_SHEET_COLS"])
    starting_sreqs_dict = bd.df_to_dict_of_lists(sreqs_df, req_sreq_fields["SREQ_SHEET_COLS"], literal_eval= req_sreq_fields["SREQ_LITERAL_EVAL"])

    formatted_reqs_dict = make_reqs_dict(starting_reqs_dict, req_sreq_fields["REQ_ATTRS"])
    add_sreqs_dict(formatted_reqs_dict, starting_sreqs_dict, req_sreq_fields["SREQ_ATTRS"])
    
    return formatted_reqs_dict

def make_reqs_dict(reqs_input, req_attrs):
    prog_keys = reqs_input["Program Key"]
    req_keys = reqs_input["Req Key"]
    
    num_rows = len(req_keys)
    result_dict = {}

    for i in range(num_rows):
        prog_key = prog_keys[i]
        if prog_key not in result_dict.keys():
            result_dict[prog_key] = {}
            result_dict[prog_key]["Reqs"] = {}

        req_dict = {}
        for attr in req_attrs:
            req_dict[attr] = reqs_input[attr][i]
        
        result_dict[prog_key]["Reqs"][req_keys[i]] = req_dict
    
    return result_dict

def add_sreqs_dict(reqs_dict, sreqs_input, sreq_attrs):
    sreq_keys = sreqs_input["Sreq Key"]
    num_rows = len(sreq_keys)
    
    for i in range(num_rows):
        this_prog_key = sreqs_input["Program Key"][i]
        if "Sreqs" not in reqs_dict[this_prog_key].keys():
            reqs_dict[this_prog_key]["Sreqs"] = {}
        
        sreq_dict = {}
        sreq_key = sreq_keys[i]
        sreq_type = str(sreqs_input["Sreq Type"][i])
        sreq_dict["Sreq Type"] = sreq_type
        for attr in sreq_attrs:
            sreq_dict[attr] = sreqs_input[attr][i]
        
        reqs_dict[this_prog_key]["Sreqs"][sreq_key] = sreq_dict
    
    return reqs_dict