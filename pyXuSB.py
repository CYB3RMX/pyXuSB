#!/usr/bin/python3

import npyscreen
import os
import sys
import psutil
from subprocess import Popen, PIPE

# Checking permissions
if int(os.getuid()) != 0:
    print("[!] You need root permissions to use this tool.")
    sys.exit(1)

# Enumerating all partitions
try:
    command = "lsblk -o name -n -s -l > parts.txt"
    os.system(command)
    partitions = open("parts.txt", "r").readlines()
except:
    print("[!] An error occured while enumerating disk partitions.")
    sys.exit(1)

# An inputbox
class IsoFileInput(npyscreen.BoxTitle):
    _contained_widget = npyscreen.MultiLineEdit

# Class for main form that handles inputs and iso burning
class MainForm(npyscreen.FormBaseNew):
    def create(self):
        # Getting terminal resolution
        self.y, self.x = self.useable_space()

        # Getting path of the iso file
        self.isoFile = self.add(
            IsoFileInput, name='Enter >Path< of the ISO image:',
            custom_highlighting=True, max_height=self.y // 10,
            max_width=self.x // 2, relx=20
        )
        # Selecting USB partition for iso burning
        self.diskParts = self.add(
            npyscreen.TitleCombo, name='Select USB partition',
            values=partitions, rely=10
        )
        # Creating start button that does iso burning
        self.add(
            npyscreen.ButtonPress, name="Start Burning!!",
            when_pressed_function=self.Burner, relx=20,
            rely=15
        )
        # Creating button that repairs USB drivers
        self.add(
            npyscreen.ButtonPress, name="Format/Fix USB!!",
            when_pressed_function=self.FixUsb, relx=20
        )
        # Creating exit button
        self.add(
            npyscreen.ButtonPress, name="Qu1t pyXuSB",
            when_pressed_function=self.ExitButton, relx=20,
            rely=20
        )

    # Defining exit button function
    def ExitButton(self):
        # Ask to user for exit
        exiting = npyscreen.notify_yes_no(
            "Are you sure to quit pyXuSB?", "Notification",
            editw=2
        )
        # If user selects YES then clean up and exit
        if exiting:
            self.parentApp.setNextForm(None)
            if os.path.exists("parts.txt"):
                os.remove("parts.txt")
            sys.exit(0)
        else:
            pass

    # Defining function that formats USB drivers to msdos filesystem
    def FixUsb(self):
        # Asking to user
        question = npyscreen.notify_yes_no(
            "Are you sure to continue? Your all data is going to deleted.", "Notification",
            editw=2
        )
        if question:
            try:
                # Creating unallocated partition
                unalloc = ['mkfs.msdos', f'/dev/{self.diskParts.values[self.diskParts.value]}'.strip('\n'), '-I']
                cmd1 = Popen(unalloc, stderr=PIPE, stdout=PIPE)

                # Make sure it is completely formatted.
                fixmeee = ['mkfs.msdos', f'/dev/{self.diskParts.values[self.diskParts.value]}'.strip('\n')]
                cmd1 = Popen(fixmeee, stderr=PIPE, stdout=PIPE)

                # Notification
                npyscreen.notify_confirm(
                    "Partition: "+ f"/dev/{self.diskParts.values[self.diskParts.value]}".strip('\n') + " is successfully formatted.",
                    "Notification"
                )
            except:
                npyscreen.notify_wait(
                    "Please specify a correct partition to format!!", "Notification"
                )
        else:
            pass

    # Defining function that handles Start burning button
    def Burner(self):
        # Checking existence for target file
        if os.path.exists(self.isoFile.value):
            pass
        else:
            npyscreen.notify_confirm(
                "Target file not found. Quitting!!", "Notification"
            )
            sys.exit(0)

        # Asking for user to start ISO burning
        question = npyscreen.notify_yes_no(
            "Are you sure to continue? Your all data is going to deleted.", "Notification",
            editw=2
        )
        if question:
            # Creating unallocated partition on target USB
            cmdline = ['mkfs.msdos', f'/dev/{self.diskParts.values[self.diskParts.value]}'.strip('\n'), '-I']
            command = Popen(cmdline, stderr=PIPE, stdout=PIPE)
            # Make sure target USB driver is completely formatted :)
            cmdline = ['mkfs.msdos', f'/dev/{self.diskParts.values[self.diskParts.value]}'.strip('\n')]
            command1 = Popen(cmdline, stderr=PIPE, stdout=PIPE)
            npyscreen.notify_confirm(
                f"Created unallocated partition on /dev/{self.diskParts.values[self.diskParts.value]}"
            )

            # Then start burning
            npyscreen.notify_confirm(
                f"Burning {self.isoFile.value} to /dev/{self.diskParts.values[self.diskParts.value]}\nIt will take a while. Please wait!!"
            )
            try:
                cmdline = ['dd', 'bs=4M', f'if={self.isoFile.value}'.strip('\n'), f'of=/dev/{self.diskParts.values[self.diskParts.value]}'.strip('\n'),
                        'conv=fdatasync,noerror', 'status=none']
                command2 = Popen(cmdline, stderr=PIPE, stdout=PIPE)
                npyscreen.notify_confirm(
                    "ISO burning is completed. Now you can use your USB ;)",
                    "Notification"
                )
            except:
                sys.exit(1)
        else:
            pass

# Class for main application
class MainApp(npyscreen.NPSAppManaged):
    # When application starts
    def onStart(self):
        npyscreen.setTheme(
            npyscreen.Themes.TransparentThemeLightText
        )
        # Our main application
        self.addForm(
            'MAIN', MainForm, name='pyXuSB ISO File Burner v0.2',
            lines=30, columns=90
        )

# Execution area
if __name__ == '__main__':
    try:
        app = MainApp()
        app.run()
        if os.path.exists("parts.txt"):
            os.remove("parts.txt")
    except KeyboardInterrupt:
        print("[+] Goodbye...")
        if os.path.exists("parts.txt"):
            os.remove("parts.txt")
