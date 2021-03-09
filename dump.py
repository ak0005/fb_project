import os
import  utils.const as const

os.system('mongoexport -d '+const.grpId+' -c ' +
          const.PostCollection+' -o '+const.dump+' --pretty')

os.system('mongodump --db '+const.grpId)