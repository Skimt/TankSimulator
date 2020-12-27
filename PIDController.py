

class PIDController:

    """
    The PID Controller calculates the proportional, integral, and derivative 
    of the differential error found between SP and PV. 
    """

    SetPoint = 0
    Kp = 0
    Ti = 0
    Td = 0
    Manual = 0

    integral = 0
    processVariableLast = 0
    minLimit = 0
    maxLimit = 0

    def __init__(self, setPoint = 100, minLimit = 0, maxLimit = 1):
        self.SetPoint = setPoint
        self.minLimit = minLimit
        self.maxLimit = maxLimit

    # Returns the CV
    def GetControlVariable(self, processVariable, deltaTime):

        # Error
        error = self.SetPoint - processVariable

        # Proportional gain
        proportional = self.Kp * error
        
        # Integral gain
        self.integral += (self.Kp / self.Ti) * error * deltaTime
        self.integral = self.Clamp(self.integral)

        # Derived gain
        derivative = self.Kp * self.Td * ((processVariable - self.processVariableLast) / deltaTime)
        self.processVariableLast = processVariable

        # Control Variable
        return self.Clamp(self.Manual + proportional + self.integral + derivative)

    # Tune Kp and Ti using Ziegler-Nichols' PI method. 
    def TuneZNPI(self, tu):

        self.Manual = 0
        self.Kp = 0.45 * self.Kp
        self.Ti = tu / 1.2

    # Tune Kp and Ti using Relaxed Ziegler-Nichols' method.
    def TuneRZNPI(self, tu):
        
        self.Manual = 0
        self.Kp = 0.25 * self.Kp
        self.Ti = 1.25 * tu

    # Tune Kp and Ti using Good Gain method
    def TuneGG(self, tou):

        self.Manual = 0
        self.Kp = 0.8 * self.Kp
        self.Ti = 1.5 * tou

    # Tune Kp and Ti using Skogestad method
    def TuneSkogestad(self, ki, tc, tau):

        self.Manual = 0
        self.Kp = 1 / (ki * (tc + tau))
        self.Ti = 2 * (tc + tau)
    
    # Clamp value between min-max. 
    def Clamp(self, value):
        if value < self.minLimit: value = self.minLimit
        if value > self.maxLimit: value = self.maxLimit
        return value