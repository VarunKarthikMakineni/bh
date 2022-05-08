import numpy as np

class Bulkhead:

    def __init__(self):
        
        # design values
        self.max_rated_load = 2000 # N
        self.airframe_thickness = 0.0025 # m
        self.bulkhead_diameter = 0.14 # m

        # configurable values
        self.safety_factor = 1
        self.screw_count = 4
        self.max_screw_length = 0.010 # m

        # screw properties
        self.screw_shear_strength = 375000000 # N/m2 for grade 8.8 steel bolts

        # bulkhead properties
        self.bulkhead_yield_strength = 240000000 # N/m2 for aluminium 6061-T6 according to wikipedia
        self.bulkhead_shear_strength = 207000000 # N/m2 for aluminium 6061-T6 according to asm.matweb.com
        self.bulkhead_density = 2700 # kg/m3

        self.update()

    def update(self):
        self.max_design_load = self.max_rated_load * self.safety_factor

    def screw_size(self):
        
        self.update()

        # returns the size of a metric screw that can handle the design loads
        # calculations are meant to avoid 

        # screw dia based on screw shear
        screw_area = (self.max_design_load / self.screw_count) / self.screw_shear_strength
        screw_dia = (( 4 * screw_area / np.pi ) ** 0.5)
        screw_dia *= 1000 # mm
        screw_dia = np.ceil(screw_dia) # round up to next mm
        screw_dia = max(screw_dia,2) # minimum dia is 2mm


        # screw length based on bearing stress assuming perfect fit
        # bearing_area = (self.max_design_load / self.screw_count) / self.bulkhead_yield_strength
        # screw_length = bearing_area / screw_dia
        # screw_length = max(screw_length , 0.006) # minimum length of 6mm inside bulkhead, which is an arbitrary value for now
        # screw_length += self.airframe_thickness # add airframe thickness

        screw_length = self.max_screw_length
        screw_length *= 1000 # mm
        screw_length = np.ceil(screw_length) # round up to nearest mm
        screw_length += screw_length % 2 # make sure length is even because they are widely available

        return screw_dia/1000, screw_length/1000 # in m and m

    def bulkhead_thickness(self):

        self.update()

        # returns thickness of bulkhead in mm
        # minimum thickness of bulkhead required based on shear tear out, assuming load is uniformly distributed on all four screws

        total_surfaces_in_shear = 2 * self.screw_count
        minimum_area_in_shear = (self.max_design_load / total_surfaces_in_shear) / self.bulkhead_shear_strength
        
        screw_dia,screw_length = self.screw_size()
        length_of_screw_in_bulkhead = screw_length - self.airframe_thickness
        
        edge_thickness = minimum_area_in_shear / length_of_screw_in_bulkhead
        
        if(edge_thickness < 0.002):
            edge_thickness = 0.002

        self.edge_thickness = screw_dia
        # this thickness value will not include the hole because obtained thickness is very small compared ot screw sizes
        bulkhead_thickness = 2 * edge_thickness + screw_dia

        return bulkhead_thickness

    def bulkhead_mass(self):
        
        self.update()
        volume = self.bulkhead_thickness() * np.pi * self.bulkhead_diameter ** 2 / 4
        mass = volume * self.bulkhead_density
        return mass