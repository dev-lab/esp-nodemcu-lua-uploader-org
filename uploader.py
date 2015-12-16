com_port = 'COM4'
baud_rate = 115200
# baud_rate = 9600
hardware_has_rts_reset = False
do_lua_file_after_upload = True

save_lua = \
r"""file.remove('%s')
    file.open('%s', 'w')
    uart.on('data', 255,
      function (d)
        c = tonumber(d:sub(1, 4))
        d = d:sub(5, 4+c)
        file.write(d)
        if c ~= 251 then
          uart.on('data')
          file.close()
        end
        uart.write(0, '\r')
      end, 0)"""
save_lua = ' '.join([line.strip() for line in save_lua.split('\n')]).replace(', ', ',')

import os, serial, sys

prompt = '\n> '
def read_till_prompt(do_log=False):
    data = ''
    while data[-3:] != prompt:
        d = ser.read()
        if do_log:
            sys.stdout.write(d)
            if d == '':
                sys.stdout.write('.')
        data += d
    return data

ser = serial.Serial(com_port, baud_rate, timeout=1)
# Opening the serial port changes DTR and RTS to 0.
if hardware_has_rts_reset:
    sys.stdout.write('Reset... ')
    ser.setDTR(False) # Setting them to False sets their logic level back to 1.
    ser.setRTS(False)
    read_till_prompt() # Wait until Lua has booted after the reset caused by RTS.
                       # This waits forever in case RTS is not connected to RESET.
    sys.stdout.write('done.\n')
else:
    sys.stdout.write('If nothing happens, try setting hardware_has_rts_reset = True\n')

file_path = sys.argv[1]
file_name = os.path.basename(file_path)
save_command = save_lua % (file_name, file_name) + '\r'
assert len(save_command) < 256, 'save_command too long: %s bytes' % len(save_command)
ser.write(save_command)
response = read_till_prompt()
assert response == save_command + prompt, response

f = open( file_path, 'rb' ); content = f.read(); f.close()
pos = 0
chunk_size = 251 # 255 (maximum) - 4 (hex_count)
while pos <= len(content):
    data = content[pos : pos + chunk_size]
    pos += chunk_size
    count = len(data)
    if count != chunk_size:
        data += ' ' * (chunk_size - count) # Fill up to get a full chunk to send.
    hex_count = '0x' + hex(count)[2:].zfill(2) # Tell the receiver the real count.
    ser.write(hex_count + data)
    assert ser.read(1) == '\r'
    percent = int(100 * pos / ((len(content) + chunk_size) / chunk_size * chunk_size))
    sys.stdout.write('%3s %%\n' % percent)

if do_lua_file_after_upload and file_name.endswith('.lua'):
    ser.write('dofile("%s")\r' % file_name)
    read_till_prompt(do_log=True)

ser.close()
