
def create_programs_dict(buckets_ref, reqs_ref, runs_and_programs, req_sreq_fields):
    programs_ref = {}
    for run_name, programs_list in runs_and_programs.items():
        programs_ref[run_name] = {}
        ref_name = run_name
        if run_name[-5:] == "_ONLY":
            ref_name = run_name[:-5]
        
        programs_ref[run_name]["Buckets"] = buckets_ref[ref_name]
        for each_program in programs_list:
            buckets_per_req = get_buckets_per_req(reqs_ref[each_program], buckets_ref[ref_name])
            new_subdict = make_reqs_subdict(reqs_ref[each_program], buckets_per_req, req_sreq_fields["REQ_ATTRS"], req_sreq_fields["SREQ_ATTRS"])
            programs_ref[run_name][each_program] = new_subdict  

    return programs_ref

def make_reqs_subdict(reqs_ref, buckets_per_req, req_attrs, sreq_attrs):
    subdict = {}
    subdict["Reqs"] = {}
    subdict["Sreqs"] = {}
    for each_req in reqs_ref["Reqs"].keys():
        subdict["Reqs"][each_req] = {}
        corr_buckets = buckets_per_req["Reqs"][each_req]
        subdict["Reqs"][each_req]["Buckets"] = corr_buckets
        for each_attr in req_attrs:
            subdict["Reqs"][each_req][each_attr] = reqs_ref["Reqs"][each_req][each_attr]

    for each_sreq in reqs_ref["Sreqs"].keys():
        subdict["Sreqs"][each_sreq] = {}
        corr_buckets = buckets_per_req["Sreqs"][each_sreq]
        subdict["Sreqs"][each_sreq]["Buckets"] = corr_buckets
        for each_attr in sreq_attrs:
            subdict["Sreqs"][each_sreq][each_attr] = reqs_ref["Sreqs"][each_sreq][each_attr]
        subdict["Sreqs"][each_sreq]["Sreq Type"] = reqs_ref["Sreqs"][each_sreq]["Sreq Type"]
    
    return subdict


def get_buckets_per_req(reqs_input, buckets_input):
    merged_dict = {}
    merged_dict["Reqs"] = {}
    merged_dict["Sreqs"] = {}
    sreq_sublists = {}
    
    for buck_key, buck_info in buckets_input.items():
        reqs_that_bucket_goes_to = buck_info["Req Keys"]
        
        for current_req in reqs_that_bucket_goes_to:
            if current_req in reqs_input["Reqs"].keys():

                if current_req not in merged_dict["Reqs"].keys():
                    merged_dict["Reqs"][current_req] = []
                merged_dict["Reqs"][current_req].append(buck_key)
      
            elif current_req in reqs_input["Sreqs"].keys():

                if current_req not in merged_dict["Sreqs"].keys():
                    merged_dict["Sreqs"][current_req] = []
                merged_dict["Sreqs"][current_req].append(buck_key)

            else:
                orig_req_name = current_req[:-5]
                if orig_req_name in reqs_input["Sreqs"].keys():

                    if current_req not in sreq_sublists.keys():
                        sreq_sublists[current_req] = []
            
                    sreq_sublists[current_req].append(buck_key)
    
    if len(sreq_sublists.keys()) > 0:
        for sublist_name, sublist in sreq_sublists.items():
            orig_req_name = sublist_name[:-5]
            
            if orig_req_name not in merged_dict["Sreqs"].keys():
                merged_dict["Sreqs"][orig_req_name] = []
            
            merged_dict["Sreqs"][orig_req_name].append(sublist)

    return merged_dict

