import numpy as np
import mayavi.mlab as mlab
import os
import sys

if __name__ == '__main__':
    path = os.path.dirname(__file__)

    print(path)
    with open(os.path.join(path,'meshplottercfg.txt'),'r') as cfgfile:
        for line in cfgfile:
            if 'PHI_MIN' in line:
                PHI_MIN = int(line.split('=')[1])
            elif 'PHI_MAX' in line:
                PHI_MAX = int(line.split('=')[1])
            elif 'DELTA_PHI' in line:
                DELTA_PHI = int(line.split('=')[1])
            elif 'THETA_MIN' in line:
                THETA_MIN = int(line.split('=')[1])
            elif 'THETA_MAX' in line:
                THETA_MAX = int(line.split('=')[1])
            elif 'DELTA_THETA' in line:
                DELTA_THETA = int(line.split('=')[1])

    phi, theta = np.meshgrid(np.arange(PHI_MIN,   PHI_MAX,   DELTA_PHI),
                             np.arange(THETA_MIN, THETA_MAX, DELTA_THETA))

    X_ = np.zeros(phi.shape)
    Y_ = np.zeros(phi.shape)
    Z_ = np.zeros(phi.shape)

    filename = sys.argv[1]

    with open(filename, 'r') as file:
        print('Importando arquivo...')
        for line in file:
            #if i % 10 == 0:
            s = line.split()
            x = float(s[0])
            y = float(s[1])
            z = float(s[2])
            p = float(s[3])
            t = float(s[4])
            print(p)
            print(t)
            try:
                i = list(phi[0,:]).index(int(round(p)))
                j = list(theta[:,0]).index(int(round(t)))

                X_[i, j] = x
                Y_[i, j] = y
                Z_[i, j] = z
            except:
                pass

    print('Plotando.')
    mlab.mesh(X_, Y_, Z_)
    mlab.show()