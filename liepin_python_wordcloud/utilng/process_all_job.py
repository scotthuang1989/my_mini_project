import json


def concat_jobs(filename):
    all_jobs = json.load(open(filename,'r', encoding='utf-8'))
    job_text = ""
    print("There are {} jobs".format(len(all_jobs)))
    for job in all_jobs:
        job_text += job["job_content"]
    return job_text
