import csv
import os
import argparse
import re


parser = argparse.ArgumentParser()
parser.add_argument("--dir_name", action=None)
parser.add_argument("--dir_name2", action=None)
args = parser.parse_args()

files_and_dirs = os.listdir(args.dir_name)
# Filter out only the files
files_all = [f for f in files_and_dirs if os.path.isfile(os.path.join(args.dir_name, f))]
files_static_old = [f for f in files_all if "static" in f]
files_dynamic = []
files_static = []
for f in files_static_old:
    if f.replace("static", "dynamic") in files_all:
        files_static.append(f)
        files_dynamic.append(f.replace("static", "dynamic"))

results = {}
for i in range(len(files_static)):
    key = files_static[i].replace("static", "").replace(".txt", "")
    with open(os.path.join(args.dir_name, files_static[i]), 'r') as file:
        # Read all lines into a list
        lines1 = file.readlines()
    lines1 = [l for l in lines1 if ("total_traffic" in l or ", cycles:" in l)]
    with open(os.path.join(args.dir_name, files_dynamic[i]), 'r') as file:
       # Read all lines into a list
       lines2 = file.readlines()
    if os.path.exists(os.path.join(args.dir_name2, files_static[i])):
        with open(os.path.join(args.dir_name2, files_static[i]), 'r') as file:
            # Read all lines into a list
            lines3 = file.readlines()
    else:
        lines3 = []
    if len(lines1) == 0 or len(lines2) == 0:
        continue
    print(os.path.join(args.dir_name, files_static[i]))
    lines2 = [l for l in lines2 if ("total_traffic" in l or ", cycles:" in l)]
    lines3 = [l for l in lines3 if ("total_traffic" in l or ", cycles:" in l)]
    bandwidth = 1
    bandwidth2 = 1
    cycles = 1
    for a in lines1:
        print("STATIC ", re.findall(r'-?[0-9]*\.?[0-9]+', a)[0], re.findall(r'-?[0-9]*\.?[0-9]+', a)[1])
        if "total_traffic" in a:
            #print("band ", re.findall(r'-?[0-9]*\.?[0-9]+', a)[0])
            bandwidth *= float(re.findall(r'-?[0-9]*\.?[0-9]+', a)[0])
        elif "cycles:" in a:
            #print("cyc ", re.findall(r'-?[0-9]*\.?[0-9]+', a)[0])
            #print(re.findall(r'-?[0-9]*\.?[0-9]+', a)[1])
            cycles *= float(re.findall(r'-?[0-9]*\.?[0-9]+', a)[1])
    for a in lines2:
        print("DYNAMIC ", re.findall(r'-?[0-9]*\.?[0-9]+', a)[0], re.findall(r'-?[0-9]*\.?[0-9]+', a)[1])
        if "total_traffic" in a:
            bandwidth /= float(re.findall(r'-?[0-9]*\.?[0-9]+', a)[0])
            bandwidth2 /= float(re.findall(r'-?[0-9]*\.?[0-9]+', a)[0]) 
        elif "cycles:" in a:
            cycles /= float(re.findall(r'-?[0-9]*\.?[0-9]+', a)[1])
    for a in lines3:
        if "total_traffic" in a:
            bandwidth2 *= float(re.findall(r'-?[0-9]*\.?[0-9]+', a)[0])
    results[key] = (bandwidth, bandwidth2, cycles) 

print(results)
