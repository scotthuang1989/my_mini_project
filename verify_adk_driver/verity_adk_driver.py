import os
import re
import argparse
from bs4 import BeautifulSoup, SoupStrainer
import pandas as pd
from pandas import DataFrame


ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path")

FLAGS = ap.parse_args()

# end result
# formatr is:
# {device_name:{driver_version_1:[file_name_list], driver_version_1:[file_name_list],...},
#  device_name_2:...}
device_version_collection = DataFrame()

def get_all_result(folder):
  result_file_list = []
  for dir_path, dirnames, filenames in os.walk(folder):
    for result_file in filenames:
      if re.match(r"JobResults_.*.xml", result_file):
        result_file_list.append(os.path.join(dir_path, result_file))
  return result_file_list


def get_driver_version(result_file):
  file_name = os.path.split(result_file)[-1]
  links = SoupStrainer('device')
  soup = BeautifulSoup(open(result_file, 'rb'), "lxml", parse_only=links)
  device_list_node = soup.find_all("device")
  for device_node in device_list_node:
    device_name = device_node.find("name").contents[0]
    driver_version = device_node.find("version").contents[0]
    device_version_collection.loc[file_name, device_name] = driver_version


if __name__ == "__main__":
  all_result_files = get_all_result(FLAGS.path)
  print("start processing, total file is: ", len(all_result_files))
  for index, result_file in enumerate(all_result_files):
    print("\r processing %d / %d: %s" % (index+1, len(all_result_files), result_file))
    get_driver_version(result_file)
    # if index > 1:
    #   break
  device_version_collection.fillna(0, inplace=True)

  print("starting find differences")
  # build a boolean list
  different_verion_index = []
  for i, col in enumerate(device_version_collection.columns):
    if len(set(device_version_collection.loc[:, col])) > 1:
      different_verion_index.append(True)
    else:
      different_verion_index.append(False)
  different_verion = device_version_collection.loc[:, different_verion_index]
  print("*"*30)
  print("Device have different driver versions")
  print("*"*30)
  for diff in different_verion.columns.tolist():
    print(diff)
