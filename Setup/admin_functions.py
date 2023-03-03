import basic_data_funcs as bd
from Setup import setup_buckets as sb
from Setup import setup_reqs as sr
from Setup import setup_programs as sp
import pandas as pd


def reload_all(name_prefix, save_all_files=True, config_path = "config.json"):
    config_file = bd.get_dict_from_json(config_path)
    all_req_dfs = pd.read_excel(config_file["REQS_PATH"], sheet_name= None)
    reqs_ref = sr.upload_reqs(all_req_dfs, config_file["REQ_SREQ_FIELDS"])
    if save_all_files:
        bd.write_dict_to_json(reqs_ref, name_prefix + "_reqs.json")
    else:
        print("Requirements updated but not saved")
    all_bucket_dfs = pd.read_excel(config_file["BUCKETS_PATH"], sheet_name=None)
    buckets_ref = sb.upload_buckets(all_bucket_dfs, config_file["BUCKET_FIELDS"])
    if save_all_files:
        bd.write_dict_to_json(buckets_ref, name_prefix + "_buckets.json")
    else:
        print("Buckets updated but not saved")
    programs_dict = sp.create_programs_dict(buckets_ref, reqs_ref, config_file["RUNS_AND_PROGRAMS"], config_file["REQ_SREQ_FIELDS"])
    bd.write_dict_to_json(programs_dict, name_prefix + "_programs.json")

def reload_buckets(name_prefix, reqs_ref, save_all_files= True, config_path="config.json"):
    config_file = bd.get_dict_from_json(config_path)
    buckets_path = config_file["BUCKETS_PATH"]
    bucket_dfs = pd.read_excel(config_file["BUCKETS_PATH"], sheet_name=None)
    buckets_ref = sb.upload_buckets(bucket_dfs, config_file["BUCKET_FIELDS"])
    if save_all_files:
        bd.write_dict_to_json(buckets_ref, name_prefix + "_buckets.json")
    else:
        print("Buckets updated but not saved")

    programs_dict = sp.create_programs_dict(buckets_ref, reqs_ref, config_file["RUNS_AND_PROGRAMS"], config_file["REQ_SREQ_FIELDS"])
    bd.write_dict_to_json(programs_dict, name_prefix + "_programs.json")


