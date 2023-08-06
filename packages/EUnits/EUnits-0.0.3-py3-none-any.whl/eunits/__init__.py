si_base_units = {
    'kg':{'factor':1,'base':[1,0,0,0,0,0,0]},
    'm':{'factor':1,'base':[0,1,0,0,0,0,0]},
    's':{'factor':1,'base':[0,0,1,0,0,0,0]},
    'A':{'factor':1,'base':[0,0,0,1,0,0,0]},
    'K':{'factor':1,'base':[0,0,0,0,1,0,0]},
    'mol':{'factor':1,'base':[0,0,0,0,0,1,0]},
    'cd':{'factor':1,'base':[0,0,0,0,0,0,1]}
    }

si_derived_units = {
    'N':{'factor':1,'base':[1,1,-2,0,0,0,0]},
    'Pa':{'factor':1,'base':[1,-1,-2,0,0,0,0]},
    'J':{'factor':1,'base':[1,2,-2,0,0,0,0]},
    'W':{'factor':1,'base':[1,2,-3,0,0,0,0]},
    'C':{'factor':1,'base':[0,0,-1,1,0,0,0]},
    'F':{'factor':1,'base':[-1,-2,4,2,0,0,0]},
    'M':{'factor':1000,'base':[0,-3,0,0,0,1,0]},
    'Hz':{'factor':1,'base':[0,0,-1,0,0,0,0]},
    'V':{'factor':1,'base':[1,2,-3,-1,0,0,0]},
    'W':{'factor':1,'base':[1,2,-2,-1,0,0,0]},
    'T':{'factor':1,'base':[1,0,-2,-1,0,0,0]},
    'Ω':{'factor':1,'base':[1,2,-3,-2,0,0,0]},
    'S':{'factor':1,'base':[-1,-2,3,2,0,0,0]},
    'H':{'factor':1,'base':[1,2,-2,-2,0,0,0]},
    'P':{'factor':0.1,'base':[1,-1,-1,0,0,0,0]},
    'ha':{'factor':10**4,'base':[0,2,0,0,0,0,0]},
    'l':{'factor':10**-3,'base':[0,-3,0,0,0,0,0]},
    't':{'factor':10**3,'base':[1,0,0,0,0,0,0]}
    }

common_time_units = {
    'min':{'factor':60,'base':[0,0,1,0,0,0,0]},
    'h':{'factor':3600,'base':[0,0,1,0,0,0,0]},
    'day':{'factor':86400,'base':[0,0,1,0,0,0,0]}
    }


imperial_units = {}

atomic_units = {
    'ℏ':{'factor':1.0545718e-34,'base':[1,2,-1,0,0,0,0]},
    'e':{'factor':1.602176634e-19,'base':[0,0,1,1,0,0,0]},
    'eV':{'factor':1.602176634e-19,'base':[1,2,-2,0,0,0,0]},
    'a0':{'factor':5.29177210903e-11,'base':[0,1,0,0,0,0,0]},
    'me':{'factor':9.109383701528,'base':[1,0,0,0,0,0,0]},
    'Eh':{'factor':4.3597447222071e-18,'base':[1,2,-2,0,0,0,0]},
    'Å':{'factor':10**-10,'base':[0,1,0,0,0,0,0]}
    }
    
def metric_prefixing(input_units):
    prefixes = {
        'y':10**-24,
        'z':10**-21,
        'a':10**-18,
        'f':10**-15,
        'p':10**-12,
        'n':10**-9,
        'μ':10**-6,
        'm':10**-3,
        'c':10**-2,
        'd':10**-1,
        'da':10**1,
        'h':10**2,
        'k':10**3,
        'M':10**6,
        'G':10**9,
        'T':10**12,
        'P':10**15,
        'E':10**18,
        'Z':10**21,
        'Y':10**24
        }
    out = {}

    for key, value in input_units.items():
        if key != 'kg':
            for prefix, multiplier in prefixes.items():
                out[prefix+key] = {'factor':multiplier*value['factor'],'base':value['base']}
        if key == 'kg':
            for prefix, multiplier in prefixes.items():
                out[prefix+'g'] = {'factor':multiplier/1000,'base':[1,0,0,0,0,0,0]}
        out['g'] = {'factor':1/1000,'base':[1,0,0,0,0,0,0]}

    return out

prefixed_si_units = metric_prefixing({**si_base_units, **si_derived_units})

base_units = si_base_units
    
supported_units = {
    **si_base_units,
    **si_derived_units,
    **prefixed_si_units,
    **common_time_units,
    **imperial_units,
    **atomic_units,
}

class Quantity:
    """A class with a magnitude and a unit"""
    def __init__(self, magnitude, unit_string):
        self.magnitude = magnitude
        self.unit_string = unit_string

        self.units_list = list(supported_units.keys())
        self.unit_exps = [0] * len(self.units_list)

        self.base_units_list = list(base_units.keys())
        self.base_unit_exps = [0] * len(self.base_units_list)
        
        for input_unit in unit_string.split():
            for test_unit in self.units_list:
                if input_unit == test_unit:
                    self.unit_exps[self.units_list.index(test_unit)] += 1
                    self.base_unit_exps = [a+b for a, b in
                                           zip(self.base_unit_exps,supported_units[test_unit]['base'])]
                        
                elif input_unit.startswith(test_unit+'^'):
                    self.unit_exps[self.units_list.index(test_unit)] += int(input_unit.split('^',1)[1])
                    self.base_unit_exps = [a+b for a, b in zip(self.base_unit_exps,[x * int(input_unit.split('^',1)[1]) for x in supported_units[test_unit]['base'] ])]

        self.base_magnitude = self.magnitude
        for i in range(len(self.unit_exps)):
            self.base_magnitude *= supported_units[self.units_list[i]]['factor'] ** self.unit_exps[i]
        
        self.base_unit_string = ''
        for i in range(len(self.base_unit_exps)):
            if self.base_unit_exps[i] == 1:
                self.base_unit_string += self.base_units_list[i] + ' '
            elif self.base_unit_exps[i] != 0:
                self.base_unit_string += self.base_units_list[i] +'^'+str(self.base_unit_exps[i])+' '

    ## Basic Operators
    def __str__(self):
        return str(self.magnitude)+' '+self.unit_string

    def __repr__(self):
        return str(self)

    def __neg__(self):
        return Quantity(-self.magnitude, self.unit_string)
    
    def __abs__(self):
        if self.magnitude < 0:
            return -self
        else:
            return self

    def __round__(self,n=0):
        return Quantity(round(self.magnitude,n),self.unit_string)
    
    def __int__(self):
        return int(self.magnitude)
    
    def __float__(self):
        return self.magnitude

    ## Additive Operators
    def __add__(self,other):
        if type(other) == type(self):
            if self.base_unit_string == other.base_unit_string:
                q = Quantity(self.base_magnitude + other.base_magnitude, self.base_unit_string)
                return q.in_units(self.unit_string)

            else:
                print('PROBLEM: MISMATCHED UNITS')
        else:
            print('PROBLEM: CANNOT ADD UNIT QUANTITY TO DIMENSIONLESS QUANTITY')

    def __iadd__(self,other):
        return self + other

    def __radd__(self,other):
        return self + other
    
    def __sub__(self,other):
        return self + -other

    def __isub__(self,other):
        return self - other

    def __rsub__(self,other):
        return other + -self

    ## Multiplicative operators
    def __mul__(self,other):
        if type(other) == type(self):
            quant = self.magnitude * other.magnitude
            out_unit_exps = [a+b for a,b in zip(self.unit_exps, other.unit_exps)]
            out_unit_string = ''
            for i in range(len(out_unit_exps)):
                if out_unit_exps[i] == 1:
                    out_unit_string += (self.units_list[i] +' ')
                elif out_unit_exps[i] != 0:
                    out_unit_string += (self.units_list[i] +'^'+str(out_unit_exps[i])+' ')

            return Quantity(quant, out_unit_string)

        else:
            quant = self.magnitude * other
            out_unit_string = self.unit_string
            return Quantity(quant, out_unit_string)

    def __imul__(self,other):
        return self * other
    
    def __rmul__(self,other):
        return self * other
            
    def __truediv__(self,other):
        if type(other) == type(self):
            quant = self.magnitude / other.magnitude
            out_unit_exps = [a-b for a,b in zip(self.unit_exps, other.unit_exps) ]
            out_unit_string = ''
            for i in range(len(out_unit_exps)):
                if out_unit_exps[i] == 1:
                    out_unit_string += self.units_list[i] + ' '
                elif out_unit_exps[i] != 0:
                    out_unit_string += self.units_list[i] +'^'+str(out_unit_exps[i])+' '

            return Quantity(quant, out_unit_string)
        else:
            quant = self.magnitude / other
            out_unit_string = self.unit_string
            return Quantity(quant, out_unit_string)

    def __itruediv__(self,other):
        return self / other

    def __rtruediv__(self,other):
        other = Quantity(other, ' ')
        return other / self

    def __floordiv__(self,other):
        div = self / other
        return Quantity(div.magnitude, div.unit_string)

    def __ifloordiv__(self,other):
        return self // other
    
    def __rfloordiv__(self,other):
        return other // self

    def __mod__(self, other):
        div = self / other
        floor = self // other
        return Quantity(div.magnitude-floor.magnitude, div.unit_string)

    def __imod__(self, other):
        return self % other
    
    def __rmod__(self, other):
        return other % self

    def __pow__(self,other):
        quant = self.magnitude ** other
        out_unit_exps = [a*other for a in self.unit_exps]
        out_unit_string = ''
        for i in range(len(out_unit_exps)):
            if out_unit_exps[i] == 1:
                out_unit_string += self.units_list[i] + ' '
            elif out_unit_exps[i] != 0:
                out_unit_string += self.units_list[i] +'^'+str(out_unit_exps[i])+' '
        return Quantity(quant, out_unit_string)

    def __ipow__(self, other):
        return self ** other
    
    def __rpow__(self,other):
        if self.base_unit_string == '':
            return other ** self.base_magnitude
        else:
            print('PROBLEM: EXPONENTIATING A UNIT QUANTITY')

    def sqrt(self):
        return self**0.5

    ## Comparison Operators
    def __lt__(self,other):
        if self.base_unit_string == other.base_unit_string:
            if self.base_magnitude < other.base_magnitude:
                return True
            else:
                return False
        else:
            print('PROBLEM: UNIT MISMATCH')
            
    def __eq__(self,other):
        if self.base_unit_string == other.base_unit_string:
            if self.base_magnitude == other.base_magnitude:
                return True
            else:
                return False
        else:
            print('PROBLEM: UNIT MISMATCH')

    def __gt__(self,other):
        if self.base_unit_string == other.base_unit_string:
            if self.base_magnitude > other.base_magnitude:
                return True
            else:
                return False
        else:
            print('PROBLEM: UNIT MISMATCH')

    def __le__(self,other):
       return not (self > other)

    def __ne__(self,other):
       return not (self == other)

    def __ge__(self,other):
        return not (self < other)

    ##Convert Units

    def in_units(self, desired_unit_string):
        desired_base_unit_exps = [0] * len(self.base_unit_exps)
        desired_unit_exps = [0] * len(self.unit_exps)
        for input_unit in desired_unit_string.split():
            for test_unit in self.units_list:
                if input_unit == test_unit:
                    desired_unit_exps[self.units_list.index(test_unit)] += 1
                    desired_base_unit_exps = [a+b for a, b in
                                           zip(desired_base_unit_exps,supported_units[test_unit]['base'])]
                        
                elif input_unit.startswith(test_unit+'^'):
                    desired_unit_exps[self.units_list.index(test_unit)] += int(input_unit.split('^',1)[1])
                    desired_base_unit_exps = [a+b for a, b in zip(desired_base_unit_exps,[x * int(input_unit.split('^',1)[1]) for x in supported_units[test_unit]['base'] ])]
        if desired_base_unit_exps == self.base_unit_exps:
            out_magnitude = self.magnitude
            for i in range(len(self.unit_exps)):
                out_magnitude *= (supported_units[self.units_list[i]]['factor']) ** (self.unit_exps[i] - desired_unit_exps[i])
        
            return Quantity(out_magnitude, desired_unit_string)
        else:
            print('PROBELM: UNITS MISMATCH')
    
    def as_base(self):
        return Quantity(self.base_magnitude, self.base_unit_string)
