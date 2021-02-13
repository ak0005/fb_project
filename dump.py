import os
import const as const

os.system('mongoexport -d '+const.grpId+' -c ' +
          const.PostCollection+' -o '+const.dump)
fp = open(const.dump, 'r')
arr = fp.readlines()
fp.close()

fp = open(const.dump, 'w')

fp.write("{\"posts\":[\n")

for i in range(len(arr)-1):
    fp.write(arr[i][:-1]+',\n')

fp.write(arr[-1])
fp.write("]\n}")

fp.close()

# os.system('mongodump --db 161136235596016 -o ./1--C')
