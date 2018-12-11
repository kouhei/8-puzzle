import sys
from functools import reduce
csv_path = sys.argv[1]
sort_key = sys.argv[2]
output_file_name = csv_path.split(".")[0]+"_sorted."+csv_path.split(".")[1]
dics = []
data_li = []

with open(csv_path) as f:
    data = f.read()

data = data.split("\n")
headers = data[0].replace(", ", ",").split(",")

if sort_key not in headers:
    raise Exception("無効なソートキー", sort_key)


for e in data[1:-1]:
    tmp = e.replace(", ", ",").split(",")
    data_li.append(tmp)
data_li = sorted(data_li, key=lambda data: int(data[headers.index(sort_key)]))

with open(output_file_name, "w") as f:
    f.write(data[0]+"\n")
    for e in data_li:
        tmp = ""
        for ee in e:
            tmp += str(ee)+", "
        tmp = tmp[:-2]
        f.write(tmp+"\n")