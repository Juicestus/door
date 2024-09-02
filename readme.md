# Door

Software for the robot that opens my door for me. Contains the device software and the iPhone app used to open the door.

## Important files

- `door.py`: Python script that controls the hardware. 
- `door`: Project directory for the iPhone app.
- `door.xcodeproj`: Project metadata for iPhone app.

## Crontab entry

```sh
@reboot sudo /usr/bin/python3 /home/door/door/door.py > /home/door/door/door.log 2>&1
```

