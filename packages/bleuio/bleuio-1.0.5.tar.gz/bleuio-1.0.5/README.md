##Python library for BleuIo

### Instructions
- Install the library by running:
```shell
pip install bleuio
```
- In the python file import:
```python
 from bleuio_lib.bleuio_funcs import BleuIo
```
- Initialise an object with BleuIo. You can leave the parameters empty for auto detection.
```python
# Auto-Detect dongle
my_dongle = BleuIo()
```

```python
# Specific COM port (Win) 'COMX'
my_dongle = BleuIo(port='COM7')
```
```python
# Specific COM port (Linux) 'dev/tty.xxxxx...'
my_dongle = BleuIo(port='/dev/tty.123546877')
```
```python
# Specific COM port (Mac) 'dev/cu.xxxx...'
my_dongle = BleuIo(port='/dev/cu.123546877')
```
- Start the deamon (background process handler) for rt and tx data.
```python
my_dongle.start_daemon()
```

- Access all BleuIo AT-commands from my_dongle object. 
- The functions return a string list.
- Don't forget that you can stop started scans with: 
```python
my_dongle.stop_scan()
```
and SPS streams with:

```python
my_dongle.stop_sps()
```

Just remember that scans and streams will run indefinitely if not otherwise specified.
They will not return data until stopped using .stop_scan() or stop_sps(). 
Once stopped you can collect the data from my_dongle.rx_scanning_results 
or my_dongle.rx_sps_results.
You can get a live feed by listening to .rx_buffer().
 
 Some examples can be found in bleuio_tests\test_bleuio_funcs.py
 
## Functions 
```python
class BleuIo(object):
    def __init__(self, port='auto', baud=57600, timeout=1, debug=False):
        """
        Initiates the dongle. If port param is left as 'auto' it will auto-detect if bleuio dongle is connected.        :param port: str
        :param baud: int
        :param timeout: int
        :param debug: bool
        """

    def start_daemon(self):
        """
        Initiates a thread which manages all traffic received from serial
        and dispatches it to the appropriate callback
        """

    def stop_daemon(self):
        """
        Stops the thread which is monitoring the serial port for incoming
        traffic from the devices.
        """

    def send_command(self, cmd):
        """
        :param cmd: Data to be sent over serial. Can be used with the sps stream.
        """

    async def stop_scan(self):
       """
       Stops any type of scan.
       :return: string[]
       """

    async def stop_sps(self):
        """
        Stops SPS Stream-mode.
        :return: string[]
        """

    def at(self):
        """
        Basic AT-Command.
        :return: string[]
        """

    def ate(self, isOn):
        """
        Turns Echo on/off. ATE0 off, ATE1 on.
        :param isOn: (boolean) True=On, False=Off
        :return: string[]
        """

    def ati(self):
        """
        Device information query.
        :return: string[]
        """

    def atr(self):
        """
        Trigger platform reset.
        :return: string[]
        """

    def at_advdata(self, advdata=""):
        """
        Sets or queries the advertising data.
        :param: if left empty it will query what advdata is set
        :param advdata: hex str format: xx:xx:xx:xx:xx.. (max 31 bytes)
        :return: string[]
        """

    def at_advdatai(self, advdata):
        """
        Sets advertising data in a way that lets it be used as an iBeacon.
        Format = (UUID)(MAJOR)(MINOR)(TX)
        Example: at_advdatai(5f2dd896-b886-4549-ae01-e41acd7a354a0203010400)
        :param: if left empty it will query what advdata is set
        :param advdata: hex str
        :return: string[]
        """

    def at_advstart(self, conn_type="", intv_min="", intv_max="", timer=""):
        """
        Starts advertising with default settings if no params.
        With params: Starts advertising with <conn_type><intv_min><intv_max><timer>.
        :param: Starts advertising with default settings.
        :param conn_type: str
        :param intv_min: str
        :param intv_max: str
        :param timer: str
        :return: string[]
        """

    def at_advstop(self):
        """
        Stops advertising.
        """

    def at_advresp(self, respData=""):
        """
        Sets or queries scan response data. Data must be provided as hex string.
        :param: if left empty it will query what advdata is set
        :param respData: hex str format: xx:xx:xx:xx:xx.. (max 31 bytes)
        :return: string[]
        """

    def at_central(self):
        """
        Sets the device Bluetooth role to central role.
        :return: string[]
        """

    def at_findscandata(self, scandata):
        """
        Scans for all advertising/response data which contains the search params.
        :param scandata: str
        :return: string[]
        """

    def at_gapconnect(self, addr):
        """
        Initiates a connection with a specific slave device.
        :param addr: hex str format: xx:xx:xx:xx:xx:xx
        :return: string[]
        """

    def at_gapdisconnect(self):
        """
        Disconnects from a peer Bluetooth device.
        :return: string[]
        """

    def at_gapscan(self, timeout=0):
        """
        Starts a Bluetooth device scan with or without timer set in seconds.
        :param: if left empty it will scan indefinitely
        :param timeout: int (time in seconds)
        :return: string[]
        """

    def at_gapstatus(self):
        """
        Reports the Bluetooth role.
        :return: string[]
        """

    def at_gattcread(self, uuid):
        """
        Read attribute of remote GATT server.
        :param uuid: hex str format: xxxx
        :return: string[]
        """

    def at_gattcwrite(self, uuid, data):
        """
        Write attribute to remote GATT server in ASCII.
        :param uuid: hex str format: xxxx
        :param data: str
        :return: string[]
        """

    def at_gattcwriteb(self, uuid, data):
        """
        Write attribute to remote GATT server in Hex.
        :param uuid: hex str format: xxxx
        :param data: hex str format: xxxxxxxx..
        :return: string[]
        """

    def at_peripheral(self):
        """
        Sets the device Bluetooth role to peripheral.
        :return: string[]
        """

    def at_scantarget(self, addr):
        """
        Scan a target device. Displaying it's advertising and response data as it updates.
        :param addr: hex str format: xx:xx:xx:xx:xx:xx
        :return: string[]
        """

    def at_spssend(self, data=""):
        """
        Send a message or data via the SPS profile.
        Without parameters it opens a stream for continiously sending data.
        :param: if left empty it will open Streaming mode
        :param data: str
        :return: string[]
        """

    def help(self):
        """
        Shows all AT-Commands.
        :return: string[]
        """

```

#Enjoy!