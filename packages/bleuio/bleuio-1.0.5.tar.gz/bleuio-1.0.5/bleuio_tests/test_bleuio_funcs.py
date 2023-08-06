# (C) 2020 Smart Sensor Devices AB

import time

from bleuio_lib.bleuio_funcs import BleuIo

# Start
my_dongle = BleuIo()
my_dongle.start_daemon()


def simplescan():
    # Saves the response (string list) of the ATI command to the status variable
    status = my_dongle.ati()
    for i in status:
        # Prints each line of status variable
        print(i)
        # Checks if dongle is in Peripheral
        # If it is it puts the dongle in Central Mode to allow scanning
        if i.__contains__("Peripheral"):
            print(my_dongle.at_central())

    # Runs a scan for 4 seconds then prints out the results, line by line
    scan_result = my_dongle.at_gapscan(timeout=4)
    for y in scan_result:
        print(y)


#simplescan()

# Some more examples of almost every function
# cmd = my_dongle.at_central()
# print(cmd)
# cmd = my_dongle.at_peripheral()
# print(cmd)
# cmd = my_dongle.at()
# print(cmd)
# cmd = my_dongle.ate(0)
# print(cmd)
# cmd = my_dongle.ati()
# print(cmd)
# cmd = my_dongle.ate(1)
# print(cmd)
# cmd = my_dongle.at_advdata()
# print(cmd)
# cmd = my_dongle.at_advdata("04:09:43:41:54")
# print(cmd)
#cmd = my_dongle.at_advdatai("ebbaaf47-0e4f-4c65-8b08-dd07c98c41ca0000000000")
#print(cmd)
# cmd = my_dongle.at_advstart()
# print(cmd)
# time.sleep(2)
# cmd = my_dongle.at_advstop()
# print(cmd)
# cmd = my_dongle.at_advstart("1","500","600","20")
# print(cmd)
# time.sleep(2)
# cmd = my_dongle.at_advstop()
# print(cmd)
# print(my_dongle.at_findscandata("5B0705"))
# time.sleep(4)
# print(my_dongle.stop_scan())
# find = my_dongle.rx_scanning_results
# print("my_dongle.at_findscandata(5B0705)")
# print("="*21)
# print(find)
# print("="*21)
# cmd = my_dongle.at_gapconnect("[0]40:48:FD:E5:2C:D9")
# time.sleep(0.5)
# print(cmd)
# cmd = my_dongle.at_gapdisconnect()
# print(cmd)
# cmd = my_dongle.at_gapscan(10)
# print("my_dongle.at_gapscan(10)")
# print("="*21)
# print(cmd)
# print("="*21)
# print(my_dongle.at_gapscan())
# time.sleep(3)
# print(my_dongle.stop_scan())
# gapscan = my_dongle.rx_scanning_results
# print("my_dongle.at_gapscan()")
# print("="*21)
# print(gapscan)
# print("="*21)
# print(my_dongle.at_gapstatus())
# cmd = my_dongle.at_gattcread("000b")
# print(cmd)
# cmd = my_dongle.at_gattcwrite("000b", "HEJ")
# print(cmd)
# cmd = my_dongle.at_gattcwriteb("000b", "010101")
# print(cmd)
# print(my_dongle.at_scantarget("[1]F3:D1:ED:AD:8A:10"))
# time.sleep(3)
# print(my_dongle.stop_scan())
# scan = my_dongle.rx_scanning_results
# print("my_dongle.at_scantarget([1]F3:D1:ED:AD:8A:10)")
# print("="*21)
# print(scan)
# print("="*21)
# cmd = my_dongle.at_spssend("howdy")
# print(cmd)
# cmd = my_dongle.at_spssend()
# print(cmd)
# my_dongle._send_command("Hello")
# my_dongle.stop_sps()
# time.sleep(0.5)
# help = my_dongle.help()
# print(help)
