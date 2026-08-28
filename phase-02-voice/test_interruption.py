import time

from interruption import InterruptionMonitor


monitor = InterruptionMonitor()

monitor.start()

print("Monitor is running.")
print("Say something to trigger interruption.")

while not monitor.interrupted():

    time.sleep(0.1)

print("Interruption detected.")

monitor.stop()