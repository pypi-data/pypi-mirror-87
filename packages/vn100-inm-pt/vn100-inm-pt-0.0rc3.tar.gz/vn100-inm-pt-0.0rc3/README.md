# The vn100-inm-pt package

## 1. How to use?

### 1.a. Requirements

First of all, there must be ready the following 4 items:

1. The user's health_diagnostics callback function: this must be a string message argument field. For example:
~~~
def onerror(msg: str):
    print("health: {}".format(msg))
~~~
2. The inm_output callback function: this must be a dictionary message argument field. For example:
~~~
def ondata(msg: dict):
    print("data: {}".format(msg))
~~~
3. The vn-100's structural data message architecture descriptor database: this is an SQLite database. The manufacturer default name is "vn100.db".
4. The vn-100's structural data message architecture descriptor database connection implementation: this is a SQLite database connection, from the python's default sqlite3 library.
For example, you can get a connection with the following function:
~~~
import sqlite3
import os
def sqlite3_db_connection(db_filename: str):
    # Check if db_file is a file:
    print(os.path.isfile(db_filename))
    if (not os.path.isfile(db_filename)):
        raise FileNotFoundError("The SQLite database file {} doesn't exist.".format(
            db_filename))
    return sqlite3.connect(db_filename)
~~~

### 1.b. The "run" basic implementation
Now you are ready for make the implementation of the "run" main function. So, you must write the following code piece:
~~~
from vn100 import run
run(
    onerror=onerror,
    ondata=ondata,
    db_connection=sqlite3_db_connection("vn100.db"))
~~~

Now yo can run this python script. First it will check the INM settings, next it will begin to print the output data through the "ondata" function callback. For any reason, if the callback functions or internal functions becomes slower, warning or error messages will be printed through the "onerror" function callback.


## 2. A briefing about the full implementation

The full arguments list that could be passed when it's created are as follows:
~~~
from vn100 import run
run(
    onerror: Callable=None, 
    ondata: Callable=None, 
    hwconfig: dict=hwc, 
    mpconfig: dict=mpc, 
    inm_config: dict=inm_usd, 
    db_connection: Any=None, 
    spsettings: dict=sps, 
    connsettings: dict=usc)
~~~

Where:

- onerror: is the user callback function with a string argument, where the health watchdogs will report delays or lack failures from the library framework operation.

- ondata: is the user callback function with a dictionary argument, where the INM parsed output messages will be written.

**Note: If both "onerror" and "ondata" is not passed (default is None for both), the system won't start.**

- hwconfig: is a dictionary with all the health watchdogs timers values. It's recommended leave the default configuration (don't worry for pass it).

- mpconfig: is a dictionary with all the main performance configuration. Buffer sizes, dead-time function timers are on this. It's recommended leave the default configuration (don't worry for pass it).

- inm_config: is a dictionary with some INM user settings. There can specify the output variables, some of them, update asynchronous data output frequency, INM serial port settings, low-pass FIR and Kalman filters, and more. See the VN-100 user's manual for detailed information.

- db_connection: is an instance of the sqlite3.connect('filename'), from the Python's sqlite3 default library, where the filename argument shall be the filename of the vn-100's structural data message architecture descriptor database. The manufacturer default name is "vn100.db".

- spsettings: is a dictionary with the serial port settings of this machine. Bit (or baud) rate, parity, data bits and stop bits must be coherent respect to the INM serial port settings values. The next is the default dictionary values:

~~~
serial_port_settings = {
    "port": "/dev/ttyUSB0",
    "bit_rate": 115200
}
~~~

- connsettings: is a dictionary with the RPC communication channel settings. This is a UDP port, with the IP address and port number. The next is the default dictionary values:

~~~
udp_connection_settings = {
    "IP_address": "0.0.0.0",
    "port": 27800
}
~~~

## 3. The RPC service

The vn100-inm-pt library has a RPC service, where through this, it can make settings changes or improve INM tasks that need to be supplied from outer information, for example, the current speed for AHRS calculations to improve accurate results.

Let's go to the following link: https://github.com/palcort-tech/internal-vn100. Go to the folder named "clients", into this a "hmi_client.py" source code is supplied. This module has 3 classes:

- CksmFletcher16
- UDP_Client
- VN100_HMI_Client

The main is the latter. This class describes all the possible RPC that can be made. The next section we are going to demonstrate an example that how some of them works.

### **WARNING: the frequency among each RPC must be less than 0.5 Hz (2 s per RPC).**

## 4. RPC demonstration for the Palcort Tech's ADM

The ADM is a monitor and register device designed for aircrafts. This brings a VectorNav INM VN-100, that supplies information about AHRS, atmospheric temperature and pressure. For AHRS calculations, the INM needs the internal 3D accelerometer, 3D gyro, 3D magnetometer and external information about speed, that it must be supplied via the RPC channel communication. Furthermore, for more accurate magnetometer measurements, through such latter channel, the current global position coordinates must be filled.

Let's do the RPC needed. On this demonstration we are going to use the hmi_client module. 

## The current aircraft or ship speed
For the current speed to improve AHRS computing accuracy, you must make the following RPC:

~~~
hmi_client.velocity_aiding_set_velocity_compensation_measurement(
    VelocityX=0.0)
~~~

Where the "VelocityX" field is the current aircraft or ship linear velocity, normally supplied from a GNSS/GPS module. This value units are in m/s.

## The current aircraft or ship global position
For the current global position to improve accuracy of magnetometer measurements, you must make the following RPC. The next example, there is made an RPC with the relative GNSS information of Bogotá/Colombia city location (aircraft or ship at ground), at the beginning of year 2020:
~~~
hmi_client.world_magnetic_gravity_set_reference_vector_configuration(
    UseMagModel="ENABLE",
    UseGravityModel="ENABLE",
    RecalcThreshold=1000,
    Year=2020.0,
    Latitude=4.62,
    Longitude=-74.06,
    Altitude=2600.0)
~~~

Where:

- UseMagModel and UseGravityModel fields must be setted as "ENABLE" to improve AHRS and magnetometer computing accuracy.
- RecalcThreshold is the limit value of a traveled distance segment until to recalculate the reference vectors from supplied GNSS/GPS information. Default value is 1000 (m).
- Year is a single precision floating point value (32 bits) with the reference date expressed as a decimal year.
- Latitude, Longitude and Altitude are a double precision floating point value (64 bits) with the reference latitude, longitude and altitude position. Latitude and Longitude are in degrees and the Altitude is in meters.

### **WARNING: since the RPC answer time is moderately high (between 1 to 2 s), it's important to bear in mind that the frequency among RPC never must be higher than 0.5 Hz. The recommended value is 0.5 Hz (2 s per RPC), or less.**

## 5. Health watchdog callback messages

As we have seen before at "Requirements" section, a user health callback function should be provided for error messages, as it is described at "onerror" callback function example. There are 2 kind of possible callback messages that the library can send, according to there can happen:

- DELAYED: if callback function is None, the system throws log messages at WARNING level. This kind of string message presents the following format:

~~~
"DELAYED: {class_name}::{timer_name}"
~~~
When a DELAYED issue is thrown, means that a process is more delayed than permitted, according to the manufacturer's benchmarks and the performance promises. It could be since all the CPU performance use is overloaded or main performance configuration settings descriptor is wrong written according to the user's INM settings and the whole the device use case, then the performance settings could be not affordable to supply the minimal requirements to the statu quo operation. On these cases, contact the manufacturer to fix the issues, specially when these cases often occurs.


- UNHEALTHY: if callback function is None, the system throws log messages at ERROR level. This kind of string message presents the following format:

~~~
"UNHEALTHY: {class_name}::{timer_name}"
~~~
When an UNHEALTHY issue is thrown, means that a process is much more delayed than permitted, according to the manufacturer's benchmarks and the performance promises, and according to the related DELAYED issues. It could be due to such process is lacked, because a hardware trouble (mismatches, or it is faulty), or because the same troubles described on DELAYED issues. It's possible that these kind of issues could be happend, for sporadic cases it could resolve just restarting the service, otherwise, if these often occurs, it must be checked the main performance configuration settings descriptor or, at worst case, the source code to fix the issues or bugs respectively, as soon as possible.

**Notice: for both DELAYED and UNHEALTHY cases, the quotation marks are not into the message content.**

## 6. INM Output object-formatted messages

As we have seen before at "Requirements" section, a user output messages callback function should be provided for INM output messages, as it is described at "ondata" callback function example. Each message that will returned shows the following structure:
~~~
{'type': 'binary', 
'content': 
    {'yaw': 
        {'field': 'YawPitchRoll', 
        'group': 'GROUP_1', 
        'units': 'degrees', 
        'value': -24.123159408569336}, 
    'pitch': 
        {'field': 'YawPitchRoll', 
        'group': 'GROUP_1', 
        'units': 'degrees', 
        'value': 0.6942007541656494}, 
    'roll': 
        {'field': 'YawPitchRoll', 
        'group': 'GROUP_1', 
        'units': 'degrees', 
        'value': 1.5082707405090332}, 
    'rate[0]': 
        {'field': 'AngularRate', 
        'group': 'GROUP_1', 
        'units': 'rad/s', 
        'value': -0.00045149121433496475}, 
    'rate[1]': 
        {'field': 'AngularRate', 
        'group': 'GROUP_1', 
        'units': 'rad/s', 
        'value': -8.948612958192825e-05}, 
    'rate[2]': 
        {'field': 'AngularRate', 
        'group': 'GROUP_1', 
        'units': 'rad/s', 
        'value': -0.00015626102685928345}, 
    'accel[0]': 
        {'field': 'Accel', 
        'group': 'GROUP_1', 
        'units': 'm/s^2', 
        'value': 0.11937554180622101}, 
    'accel[1]': 
        {'field': 'Accel', 
        'group': 'GROUP_1', 
        'units': 'm/s^2', 
        'value': -0.2576184868812561}, 
    'accel[2]': 
        {'field': 'Accel', 
        'group': 'GROUP_1', 
        'units': 'm/s^2', 
        'value': -9.837200164794922}, 
    'mag[0]': 
        {'field': 'MagPres', 
        'group': 'GROUP_1', 
        'units': 'Gauss', 
        'value': 0.18978460133075714}, 
    'mag[1]': 
        {'field': 'MagPres', 
        'group': 'GROUP_1', 
        'units': 'Gauss', 
        'value': 0.08719169348478317}, 
    'mag[2]': 
        {'field': 'MagPres', 
        'group': 'GROUP_1', 
        'units': 'Gauss', 
        'value': -0.011340515688061714}, 
    'temp': 
        {'field': 'MagPres', 
        'group': 'GROUP_1', 
        'units': '°C', 
        'value': 26.924348831176758}, 
    'pres': 
        {'field': 'MagPres', 
        'group': 'GROUP_1', 
        'units': 'KPa', 
        'value': 75.0790023803711}}}
~~~

Basically each message is formatted as a python dictionary. At the first level, 2 main keys "type" and "content" always are present. "type" says if the message is "binary" or "ascii-formatted string" emitted from the INM output serial port. The "content" has all the parsed and formatted message data. 

Let's just go to analyze the "binary" messages, because the "string" messages are only for configuration purposes. Earlier shows the structure like the previously example. Into the "content" value, there are some keys, each one with the variable names and then each one has the "field", "group", "units" and "value" keys. First two indicates what the "field" and "group" is the variable classified, according to the structural architecture of data of the INM device (see the VectorNav VN-100 INM user's manual for more information). The "units" key has the unit name that the physical magnitude of the variable is measured. The "value" has the magnitude of such variable.