import numpy as np
import matplotlib.pyplot as plt

m_O = 33.3
m_D = 31.89
V1 = 50
V2 = 31.5
Msoil = 20
WHC = (V1-V2)/Msoil
x = 0.4
y = 5e-3
w = (x*WHC + 1)*m_D/m_O - 1
conc = y*m_D/m_O / (w - y*m_D/m_O)
print(WHC, w, conc)
print(w*10)