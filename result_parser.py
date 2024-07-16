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
exit()

lines = [l for l in lines if (("improvement" in l or "ssname " in l or "failed" in l or "best reorder factor" in l))]
lines = [l for l in lines if not ("print" in l or " = " in l)]
result_keys = []
result_fields = ["ssname"]
result_values = []
vals = []

for l in lines:
    if "ssname" in l:
        result_keys.append(l.split(" ")[-1].replace("\n", "").replace(" ", ""))
        if len(vals) > 0:
            result_values.append(vals)
            # print("last vals ", last_val, len(result_values))
        del vals
        vals = []
    elif "improvement" in l or "reorder factor" in l:
        print(l)
        print(re.findall(r'-?[0-9]*\.?[0-9]+', l))
        if len(result_values) == 0:
            result_fields.append(l.replace(re.findall(r'-?\d*\.?\d+', l)[-1], "").replace("\n", ""))
        last_val = float(re.findall(r'-?\d*\.?\d+', l)[-1])
        vals.append(last_val)
    else:
        result_keys.pop(-1)
result_values.append(vals)
result_dict = {}
for r, _ in enumerate(result_keys):
    result_dict[result_keys[r]] = result_values[r]

csv_file = "output"+ args.file_name+".csv"
print(result_dict)

print(result_fields)
# Get the keys and rows
# Writing to CSV
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(result_fields)
    # Write the header
    for r, _ in enumerate(result_keys):
        print(r, _, result_dict[_])
        # writer.writerow([_].extend(result_dict[_]]))  # Write the data

