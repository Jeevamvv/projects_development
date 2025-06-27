import subprocess

subprocess.run("python3 trigger.py", shell=True)
subprocess.run("python3 constants.py", shell=True)
subprocess.run("python3 gap.py", shell=True)
subprocess.run("python3 logger_mod.py", shell=True)
subprocess.run("python3 utils.py", shell=True)
subprocess.run(["python3", "Classic_Bluetooth_Profile/opp.py"])
subprocess.run(["python3", "Classic_Bluetooth_Profile/a2dp.py"])
subprocess.run(["python3", "Classic_Bluetooth_Profile/hfp.py"])
subprocess.run(["python3", "Classic_Bluetooth_Profile/pbap.py"])

