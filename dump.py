import os
import const as const

os.system('mongoexport -d '+const.grpId+' -c ' +
          const.PostCollection+' -o '+const.dump)
