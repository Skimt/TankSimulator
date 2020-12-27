import matplotlib.pyplot as mpl

class Tank:
    Fill = 0
    def __init__(self, area = 0, height = 0, output = 0, fill = 0):
        self.Output = output
        self.Area = area
        self.Fill = fill
        self.Volume = area * height

dt = 0.1
start = 0
end = 4000
intervals = int((end - start) / dt)

xAxis = [0] * intervals
yAxis = [0] * intervals

tank = Tank(area = 13.4, height = 15, output = 25, fill = 134)
maxFeedRate = 25 / 0.45     # 55.5556 [kg/sec] maximum
feedDelay = 250             # [sec]
density = 145               # [kg/m^3]

for i in range(start, intervals):

    isDelayReached = i > feedDelay / dt
    isTankNotFull = tank.Fill < tank.Volume
    
    u = 0.45 # [%]
    if isDelayReached and isTankNotFull:
        u = 0.5 # [%]

    tank.Fill += ((maxFeedRate * u) - tank.Output) * dt / density # [L]
    
    xAxis[i] = i * dt # [sec]
    yAxis[i] = tank.Fill / tank.Area # [m]

# Print and display
print("Fill (  0 s):\t" + str(round(yAxis[0] * tank.Area, 4)) + " / " + str(round(tank.Volume, 2)) + " [L]")
print("Fill (250 s):\t" + str(round(yAxis[2500] * tank.Area, 4)) + " / " + str(round(tank.Volume, 2)) + " [L]")
print("Fill (251 s):\t" + str(round(yAxis[2510] * tank.Area, 4)) + " / " + str(round(tank.Volume, 2)) + " [L]")
print("Fill (500 s):\t" + str(round(yAxis[-1] * tank.Area, 4)) + " / " + str(round(tank.Volume, 2)) + " [L]")

# Plotting
figure, axes = mpl.subplots()
axes.set(xlabel = "Seconds [s]", ylabel = "Height [m]", title = "Sawdust tank")
axes.grid()
mpl.plot(xAxis, yAxis)
mpl.show()