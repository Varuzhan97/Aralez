def AVERAGE(data):
    data = data.reshape((4,-1), order='F')
    b = 1/len(data)
    x = np.int16(0)
    for c in data:
        x+=c*b
    return x.astype(np.int16)

frame = np.frombuffer(frame, np.int16)
frame = AVERAGE(frame)
frame = frame.tobytes()
---------------------------------------------------------
frame = np.frombuffer(frame, np.int16)
data = frame.reshape((4,-1), order='F')
b = 1/len(data)
x = np.int16(0)
for c in data:
    x+=c*b
frame = x.astype(np.int16)
frame = frame.tobytes()
