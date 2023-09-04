def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def root(x, n):
    return x ** (1 / n)

def split_float(float_number):
    float_str = "{}".format(float_number)
    parts = float_str.split('e')
    whole_str, exponent_str = parts[0].split('.')
    whole_number = (whole_str)
    decimal_part = (exponent_str)
    return whole_number, decimal_part

def find_integer_ratio(flt):
    if flt == 0:
        sign = 1
    else:
        sign = int(float(flt) // abs(float(flt)))
        
    whole, decimal = split_float(flt)
    whole = abs(int(whole))
    
    base = 10 ** (len(decimal))
    gcd_val = gcd(int(decimal), base)
    
    decimal_form = int(decimal) // gcd_val
    base_form = base // gcd_val
    
    decimal_form += base_form * whole
    return decimal_form * sign, base_form
    
def power_whole_to_frac(whole, fraction):
    val = root(whole, fraction.denominator) ** fraction.numerator
    return val

class Fraction:
    def __init__(self, a, b = 1):
        self.numerator = 0
        self.denominator = b

        if isinstance(a, Fraction):
            self.numerator = a.numerator
            self.denominator = a.denominator

        elif isinstance(a, str):
            if "." in a:
                self.numerator, self.denominator = find_integer_ratio(a)
            else:
                self.numerator, self.denominator = int(a), 1

        elif isinstance(b, float) or isinstance(b, Fraction):
            new = (Fraction(a) / Fraction(b))
            self.numerator = new.numerator
            self.denominator = new.denominator

        elif isinstance(a, int) or (isinstance(a, float) and a.is_integer()):
            self.numerator = int(a)

        elif isinstance(a, float):
            self.numerator, self.denominator = find_integer_ratio(a)

        self.verify()
        
    def verify(self):
        if self.denominator == 0:
            raise ZeroDivisionError("Cannot have fraction with denominator of zero")

    def to_float(self):
        return self.numerator / self.denominator

    def reciprocal(self):
        return Fraction(self.denominator, self.numerator)

    def simplified(self):
        gcd_val = gcd(self.numerator, self.denominator)
        return Fraction(self.numerator // gcd_val, self.denominator // gcd_val)
    
    def simplify(self):
        gcd_val = gcd(self.numerator, self.denominator)
        
        self.numerator //= gcd_val
        self.denominator //= gcd_val
        
    def __add__(self, other):
        if isinstance(other, str):
            return NotImplemented
        
        if isinstance(other, int):
            return Fraction(self.numerator + (self.denominator * other), self.denominator).simplified()
        elif isinstance(other, float):
            return self.__add__(Fraction(other))
        elif isinstance(other, Fraction):
            shared_den = self.denominator * other.denominator
            return Fraction((self.numerator * other.denominator) + (other.numerator * self.denominator), shared_den).simplified()
    
    def __sub__(self, other):
        if isinstance(other, str):
            return NotImplemented
        
        if isinstance(other, int):
            return Fraction(self.numerator - (self.denominator * other), self.denominator).simplified()
        elif isinstance(other, float):
            return self.__sub__(Fraction(other))
        elif isinstance(other, Fraction):
            shared_den = self.denominator * other.denominator
            return Fraction((self.numerator * other.denominator) - (other.numerator * self.denominator), shared_den).simplified()

    def __mul__(self, other):
        if isinstance(other, str):
            return NotImplemented
        
        if isinstance(other, int):
            return Fraction(self.numerator * other, self.denominator)
        elif isinstance(other, float):
            return self.__mul__(Fraction(other))
        elif isinstance(other, Fraction):
            return Fraction(self.numerator * other.numerator, self.denominator * other.denominator).simplified()

    def __truediv__(self, other):
        if isinstance(other, str):
            return NotImplemented
        
        if isinstance(other, int):
            return Fraction(self.numerator, self.denominator) * Fraction(1, other)
        elif isinstance(other, float):
            return self.__mul__(Fraction(other).reciprocal())
        elif isinstance(other, Fraction):
            return self.__mul__(other.reciprocal())
    
    def __str__(self):
        return "{}/{}".format(self.numerator, self.denominator)
    
    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, str):
            return NotImplemented
        
        other_value = 0
        if isinstance(other, int) or isinstance(other, float):
            other_value = float(other)
        elif isinstance(other, Fraction):
            other_value = other.to_float()

        return self.to_float() == other_value
    
    def __lt__(self, other):
        if isinstance(other, str):
            return NotImplemented
        
        other_value = 0
        if isinstance(other, int) or isinstance(other, float):
            other_value = float(other)
        elif isinstance(other, Fraction):
            other_value = other.to_float()

        return self.to_float() < other_value
    
    def to_whole_fraction(self):
        whole, numerator, denominator = self.numerator // self.denominator, self.numerator % self.denominator, self.denominator
        if numerator == 0:
            return str(whole)
        elif whole == 0:
            return str(self)
        return "{} {}/{}".format(whole, numerator, denominator)
    
    def __pow__(self, other):
        if isinstance(other, str):
            return NotImplemented
        if isinstance(other, int):
            print(self.numerator, other)
            return Fraction(self.numerator ** other, self.denominator ** other)
        elif isinstance(other, float):
            return Fraction(float(self) ** other)
        elif isinstance(other, Fraction):
            return Fraction(float(self) ** float(other))
            
    def as_representation(self):
        val = self.to_float()
        if val.is_integer():
            return int(val)
        return val

    def __call__(self):
        return self.as_representation()
    
    def __float__(self):
        return self.to_float()
    
    def __int__(self):
        return int(self.to_float())