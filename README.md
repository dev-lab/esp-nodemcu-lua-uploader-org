# NodeMCU Lightning-Fast File Uploads
A Python script for fast file upload to NodeMCU ESP board.
The script was written and shared by **Markus Gritsch** in article [**Lightning-Fast File Uploads**](http://www.esp8266.com/viewtopic.php?f=22&t=1026&start=16) on [ESP8266 Community Forum](http://www.esp8266.com).

## Installation
Markus Gritsch describes the installation in the following [post](http://www.esp8266.com/viewtopic.php?p=23403#p23403):
>* Place 'myNodeMcu.sublime-build' into %APPDATA%\Sublime Text 3\Packages\User
>* From the Sublime Text window menu select Tools->Build System->myNodeMcu
>* Press F7 to upload.
>
>You should use Sublime 3 and install Python 2.7 and pyserial.
>
>Edit 'myNodeMcu.sublime-build' to match where you placed 'uploader.py'.
>
>Edit 'uploader.py' for the COM port number you are using. 

## Usage
http://www.esp8266.com/viewtopic.php?p=5813#p5813 :
>Use Python 2 and give the Lua file as the first argument to the script:
>```
>python uploader.py test.lua
>```
>Edit the `uploader.py` file first to match your serial port.

### Usage Details
The script is configured to use baud rate `115200` by default (see the second line of [`uploader.py`](uploader.py)):
```python
com_port = 'COM4'
baud_rate = 115200
# baud_rate = 9600
```
In case if your ESP module was flashed to use another baud rate for serial communication (and there is nothing in already loaded lua code which changes the baud rate), you have to override it with supplied [`init.lua`](init.lua) module:
```lua
uart.setup(0,115200,8,0,1,1)
```
Just do the following steps to be able to upload your files in `115200` baud rate:
1. Change the `baud_rate` to `9600` (or to the baud rate supported by your NodeMCU ESP module) in [`uploader.py`](uploader.py).
2. Execute: 
    ```
    python uploader.py init.lua`
    ```
3. Restart ESP module.
4. Change back `baud_rate` to `115200` in [`uploader.py`](uploader.py).

From now on, your NodeMCU ESP instance will be able to receive files in lightning speed.

### Author
The author of the scripts is **Markus Gritsch**. He originally published it in article: [**Lightning-Fast File Uploads**](http://www.esp8266.com/viewtopic.php?p=5694#p5694) on Dec 25, 2014. The files in this repository are taken from the updated version, [published by Markus on Mar 25, 2015](http://www.esp8266.com/viewtopic.php?p=12590#p12590).

