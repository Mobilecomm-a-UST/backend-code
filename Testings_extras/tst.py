import numpy as np
print(np.nan)
print(type(np.nan))
se={np.nan,np.nan,np.nan,np.nan,2}
print(se)
se.remove(np.nan)
print(se)

print("diff:",{1,2,3}-{1,2,4,4,4,6})