import sys
import ctypes
import numpy as np
import matplotlib.pyplot as plt

dwf=ctypes.cdll.LoadLibrary("libdwf.so")
device_count=ctypes.c_int()
dwf.FDwfEnum(ctypes.c_int(),ctypes.byref(device_count))
hdwf=ctypes.c_int()
dwf.FDwfDeviceOpen(ctypes.c_int(0),ctypes.byref(hdwf))
hdwf=ctypes.c_int()
print("Opening Digilent Device...")
dwf.FDwfDeviceOpen(ctypes.c_int(-1),ctypes.byref(hdwf))
if hdwf.value==0:
        print("Failed to open device")
        sys.exit(1)
print("Device opened successfully")

dwf.FDwfAnalogOutNodeEnableSet(hdwf,0,0,1)
dwf.FDwfAnalogOutNodeFunctionSet(hdwf,0,0,1)
dwf.FDwfAnalogOutNodeFrequencySet(hdwf,0,0,ctypes.c_double(1000))
dwf.FDwfAnalogOutNodeAmplitudeSet(hdwf,0,0,ctypes.c_double(1.0))
dwf.FDwfAnalogOutConfigure(hdwf,0,1)

dwf.FDwfAnalogInChannelEnableSet(hdwf,0,1)
dwf.FDwfAnalogInChannelRangeSet(hdwf,0,ctypes.c_double(5.0))
dwf.FDwfAnalogInFrequencySet(hdwf,ctypes.c_double(100000))
dwf.FDwfAnalogInBufferSizeSet(hdwf,ctypes.c_int(1000))

dwf.FDwfAnalogInConfigure(hdwf,0,1)

sts=ctypes.c_byte()
while True:
        dwf.FDwfAnalogInStatus(hdwf,1,ctypes.byref(sts))
        if sts.value==2:
            break

buf=(ctypes.c_double*2000)()
dwf.FDwfAnalogInStatusData(hdwf,0,buf,2000)
samples=np.fromiter(buf,dtype=float)
vpp=np.max(samples) - np.min(samples)
print("Measured Vpp: ",vpp,"V")

dwf.FDwfDeviceCloseAll()

plt.plot(samples)
plt.title("Captured 1 kHz Sine Wave (1 V Amplitude)")
plt.xlabel("Sample Index")
plt.ylabel("Voltage (V)")
plt.grid(True)
plt.show()

