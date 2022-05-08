from matplotlib import pyplot as plt
from bulkhead_model import Bulkhead

# Plotting the weight of the bulkhead with respect to screw length


def plot_mass_with_load(bh):

    plt.xlabel("Rated load(N)")
    plt.ylabel("Bulkhead mass(g)")
    for i in range(100, 2000, 10):
        bh.max_rated_load = i
        plt.plot(i, bh.bulkhead_mass()*1000,"bo", markersize=1)
    plt.show()

def plot_mass_with_screw_length(bh):

    plt.xlabel("Screw Length(mm)")
    plt.ylabel("Bulkhead mass(g)")
    for i in range(2,14,2):
        bh.max_screw_length = i/1000
        plt.plot(i,bh.bulkhead_mass(),"ro")

    plt.show()

def acrylic_bulkhead():
    bh = Bulkhead()
    bh.bulkhead_shear_strength = 30000000
    bh.bulkhead_yield_strength = 65000000  # https://www.matweb.com/search/datasheet.aspx?bassnum=O1303
    bh.bulkhead_density = 1180  # kg/m3
    
    return bh

plot_mass_with_load(acrylic_bulkhead())