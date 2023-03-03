import json
import ast

def df_to_dict_of_lists(df, col_names, literal_eval = [""]):
    result = {}
    for each_name in col_names:
        if each_name in literal_eval:
            new_list = []
            for each_orig in list(df[each_name]):
                with_lit_eval = ast.literal_eval(each_orig)
                new_list.append(with_lit_eval)
        
        else:
            new_list = list(df[each_name])
        
        result[each_name] = new_list
    return result

def get_dict_from_json(json_path):
    with open(json_path) as this_json:
        res_dict = json.load(this_json)
    return res_dict

def transpose_dict_of_lists(dol, index_by):
    non_index_col_keys = []
    list_length = len(dol[index_by])
    
    for key, val in dol.items():
        if key != index_by:
            non_index_col_keys.append(key)

    result_dict = {}
    for i in range(list_length):
        new_dict = {}
        row_key = dol[index_by][i]
        for each_col in non_index_col_keys:
            new_dict[each_col] = dol[each_col][i]
        
        result_dict[row_key] = new_dict
    
    return result_dict    

def make_dict_df_ready(ref_dict, all_cols, index_name="Key"):
    result_dict = {}
    result_dict[index_name] = []
    for each_col in all_cols:
        result_dict[each_col] = []

    for key, val in ref_dict.items():
        result_dict[index_name].append(key)
        for each_col in all_cols:
            new_val = val[each_col]
            result_dict[each_col].append(new_val)

    return result_dict

def write_dict_to_json(ref_dict, new_file_name, indent=4, sort_keys = True):
    f = open(new_file_name, "w")
    json.dump(ref_dict, f, indent=indent, sort_keys=sort_keys)
    f.close()
    print("Dictionary has been written to file:")
    print(new_file_name)