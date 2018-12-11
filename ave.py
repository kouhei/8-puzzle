import sys
input_file = sys.argv[1]# ステップ数でソートしたcsv

data = []
dics = []
with open(input_file) as f:
    data = f.read()

data = data.split("\n")
header = data[0].replace(", ", ",").split(",")

# print(header)

for i, info in enumerate(data[1:]):
    tmp = info.replace(", ", ",").split(",")
    if tmp == ['']:
        continue
    # print(tmp)
    tmp = dict(zip(header, tmp))
    # print(tmp)
    dics.append(tmp)

res = {}
for dic in dics:
    if dic['step'] not in res:
        res[dic['step']] = {'node':0, 'time':0, 'num':0}
    try:
        res[dic['step']]['node'] += int(dic['node'])
        res[dic['step']]['time'] += float(dic['time'])
        res[dic['step']]['num'] += 1
    except Exception as e:
        print(dic)
        raise e


for key in res:
    res[key]['node'] /= res[key]['num']
    res[key]['node'] = int(res[key]['node']*100)/100
    res[key]['time'] /= res[key]['num']
    res[key]['time'] *= 1000
    res[key]['time'] = int(res[key]['time']*1000)/1000
    # res[key]['time'] = int(res[key]['num']*10000000)/1000000000

output_file = input_file.split(".")[0]+"_ave.csv"

with open(output_file, "w") as f:
    f.write("step, node, time\n")
    for key in res:
        f.write(key+", "+str(res[key]['node'])+", "+str(res[key]['time'])+"\n")