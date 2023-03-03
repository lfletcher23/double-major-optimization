import basic_data_funcs as bd

def upload_buckets(all_dfs, bucket_fields):
    all_buckets = {}

    for each_sheet in bucket_fields["BUCKET_SHEETS"]:
        each_dict = read_bucket_sheet(all_dfs[each_sheet], bucket_fields)
        all_buckets[each_sheet] = each_dict
    
    return all_buckets

def read_bucket_sheet(bucket_df, bucket_fields):
    as_dict_of_lists = bd.df_to_dict_of_lists(bucket_df, bucket_fields["BUCKET_SHEET_COLS"], literal_eval = bucket_fields["BUCKET_LITERAL_EVAL"])
    num_rows = len(as_dict_of_lists["Bucket Key"])
    result_dict = {}

    for i in range(num_rows):
        indiv_dict = {}
        
        for each_attr in bucket_fields["BUCKET_ATTRS"]:
            indiv_dict[each_attr] = as_dict_of_lists[each_attr][i]

        result_dict[as_dict_of_lists["Bucket Key"][i]] = indiv_dict
        
    return result_dict

