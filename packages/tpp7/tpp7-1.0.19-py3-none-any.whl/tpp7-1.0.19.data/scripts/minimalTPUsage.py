import matplotlib.pyplot as plt
from Oscillo import Oscillo

devList = Oscillo.getDeviceList()
osc = Oscillo.openDevice(devList[0])

hc = osc.getHardcopy()
plt.imsave('hardcopy.png', hc)

plt.figure()
plt.imshow(hc)
plt.show()

activeChannelList = osc.getActiveChannelList()
data = osc.getChannelListData(activeChannelList)
plt.figure()
osc.plotData(data)
plt.show()
