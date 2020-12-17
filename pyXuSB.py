#!/usr/bin/python3

import npyscreen
import os
import sys
import shutil
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
    os.remove("parts.txt")
except:
    print("[!] An error occured while enumerating disk partitions.")
    sys.exit(1)

# A function that copies folders recursively
def copytree(source, destination, symlinks=False, ignore=None):
    for item in os.listdir(source):
        so = os.path.join(source, item)
        de = os.path.join(destination, item)
        if os.path.isdir(so):
            shutil.copytree(so, de, symlinks, ignore)
        else:
            shutil.copy2(so, de)

# An inputbox for entering ISO files
class IsoFileInput(npyscreen.BoxTitle):
    _contained_widget = npyscreen.MultiLineEdit

# Class for main form that handles inputs and iso burning
class MainForm(npyscreen.FormBaseNew):
    def create(self):
        # Getting terminal resolution
        self.y, self.x = self.useable_space()

            # ---------- INPUT AREA ---------- #
        # Getting path of the iso file
        self.isoFile = self.add(
            IsoFileInput, name='Enter >Path< of the ISO image:',
            custom_highlighting=True, max_height=self.y // 10,
            max_width=self.x // 2, relx=20
        )
        # Selecting what operating system we want to
        self.OsType = self.add(
            npyscreen.TitleCombo, name="Select Pendrive Type:",
            values=['Windows Pendrive', 'Linux Pendrive']
        )
        # Selecting USB partition for iso burning
        self.diskParts = self.add(
            npyscreen.TitleCombo, name='Select USB partition',
            values=partitions, rely=10
        )
            # ---------- BUTTONS AREA ---------- #
        # Creating start button that does iso burning
        self.add(
            npyscreen.ButtonPress, name="Start!!",
            when_pressed_function=self.Burner, relx=20,
            rely=15
        )
        # Creating button that repairs USB drivers
        self.add(
            npyscreen.ButtonPress, name="Format/Fix USB",
            when_pressed_function=self.FixUsb, relx=20
        )
        # Creating install button that installs pyXuSB on system
        if os.path.exists("/usr/bin/pyXuSB"):
            pass
        else:
            self.add(
                npyscreen.ButtonPress, name="Install pyXuSB",
                when_pressed_function=self.InstallUsb, relx=20
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
            "Are you sure to quit pyXuSB?", "WARNING",
            editw=2
        )
        # If user selects YES then clean up and exit
        if exiting:
            self.parentApp.setNextForm(None)
            sys.exit(0)
        else:
            pass

    # Defining function that copies pyXuSB to /usr/bin/
    def InstallUsb(self):
        npyscreen.notify_wait("Installing pyXuSB on your system...", "NOTIFICATION")
        try:
            # If there is old version of pyXuSB then remove it.
            if os.path.exists("/usr/bin/pyXuSB"):
                npyscreen.notify_wait("Removing existing pyXuSB", "PROGRESS")
                remove = ['rm', '-rf', '/usr/bin/pyXuSB']
                command = Popen(remove, stderr=PIPE, stdout=PIPE)
                command.wait()
                npyscreen.notify_wait("pyXuSB was successfully removed.", "NOTIFICATION")
            else:
                pass

            # Installation zone
            install = ['cp', 'pyXuSB.py', '/usr/bin/pyXuSB']
            command = Popen(install, stderr=PIPE, stdout=PIPE)
            command.wait()
            npyscreen.notify_confirm("Installation finished :)", "NOTIFICATION")
        except:
            npyscreen.notify_wait("An error occured while installing pyXuSB", "ERROR")

    # Defining function that formats USB drivers to msdos filesystem
    def FixUsb(self):
        # Parsing target partition
        try:
            burnPart = str(self.diskParts.values[self.diskParts.value].replace('\n', ''))
        except:
            pass

        # Asking to user
        question = npyscreen.notify_yes_no(
            "Are you sure to continue? Your all data is going to be deleted.", "WARNING",
            editw=2
        )
        if question:
            try:
                # Wiping all data on target USB drive
                npyscreen.notify_wait(
                    f"Wiping all data on /dev/{burnPart}",
                    "PROGRESS"
                )
                unalloc = ['wipefs', '--all', f'/dev/{burnPart}']
                cmd1 = Popen(unalloc, stderr=PIPE, stdout=PIPE)
                cmd1.wait()

                # Creating msdos label on target USB drive
                npyscreen.notify_wait(
                    f"Creating MSDOS label on /dev/{burnPart}",
                    "PROGRESS"
                )
                labelz = ['parted', '--script', f'/dev/{burnPart}', 'mklabel', 'msdos']
                cmd1 = Popen(labelz, stderr=PIPE, stdout=PIPE)
                cmd1.wait()

                # Creating msdos filesystem on target USB drive
                npyscreen.notify_wait(
                    f"Creating MSDOS file system on /dev/{burnPart}",
                    "PROGRESS"
                )
                fixmeee = ['mkfs.msdos', f'/dev/{burnPart}', '-I']
                cmd1 = Popen(fixmeee, stderr=PIPE, stdout=PIPE)
                cmd1.wait()

                # All done!!
                npyscreen.notify_confirm(
                    f"Partition: /dev/{burnPart} is successfully formatted.",
                    "NOTIFICATION"
                )
            except:
                npyscreen.notify_wait(
                    "Please specify a correct partition to format!!", "ERROR"
                )
        else:
            pass

    # Defining function that handles Start burning button
    def Burner(self):
        # Parsing target partition and ISO file
        try:
            burnPart = str(self.diskParts.values[self.diskParts.value].replace('\n', ''))
            burnISO = str(self.isoFile.value.replace('\n', ''))
        except:
            pass

        # Checking existence for target file
        if os.path.exists(self.isoFile.value):
            pass
        else:
            npyscreen.notify_confirm(
                "Target file not found. Quitting!!", "ERROR"
            )
            sys.exit(0)

        # Asking for user to start ISO burning
        question = npyscreen.notify_yes_no(
            "Are you sure to continue? Your all data is going to be deleted.", "WARNING",
            editw=2
        )
        if question:
            try:
                # ---------- WINDOWS PENDRIVE ----------
                if str(self.OsType.values[self.OsType.value].strip('\n')) == "Windows Pendrive":
                    npyscreen.notify_wait("Creating Windows pendrive...", "NOTIFICATION")

                    # Wiping all data
                    npyscreen.notify_wait(f"Wiping all data on /dev/{burnPart}", "PROGRESS")
                    wiper = ['wipefs', '--all', f'/dev/{burnPart}']
                    command = Popen(wiper, stderr=PIPE, stdout=PIPE)
                    command.wait()

                    # Creating msdos label on target USB drive
                    npyscreen.notify_wait(f"Creating MSDOS label on /dev/{burnPart}", "PROGRESS")
                    labelz = ['parted', '--script', f'/dev/{burnPart}', 'mklabel', 'msdos']
                    command = Popen(labelz, stderr=PIPE, stdout=PIPE)
                    command.wait()

                    # Creating partition on target USB drive
                    npyscreen.notify_wait(f"Creating partition on /dev/{burnPart}", "PROGRESS")
                    mkparts = ['parted', '--script', f'/dev/{burnPart}', 'mkpart', 'primary', 'ntfs', '1MB', '8000MB'] # This is default value for 8GB USB drives
                    command = Popen(mkparts, stderr=PIPE, stdout=PIPE)
                    command.wait()

                    # Creating NTFS file system on target USB drive
                    try:
                        npyscreen.notify_wait(f"Creating NTFS file system on /dev/{burnPart}1", "PROGRESS")
                        createNtfs = ['mkfs.ntfs', '--quick', f'/dev/{burnPart}1']
                        command = Popen(createNtfs, stderr=PIPE, stdout=PIPE)
                        command.wait()
                    except Exception as e:
                        npyscreen.notify_confirm(f"{e}", "ERROR")
                        sys.exit(1)

                    # Mounting file systems to copy
                    try:
                        # First: mounting target partition to /mnt
                        npyscreen.notify_wait(f"Mounting /dev/{burnPart}1 to /mnt", "PROGRESS")
                        mounts = ['mount', f'/dev/{burnPart}1', '/mnt']
                        command = Popen(mounts, stderr=PIPE, stdout=PIPE)
                        command.wait()

                        # Second: Creating WindowsData directory for holding Windows files.
                        create = ['mkdir', '/tmp/WindowsData']
                        command = Popen(create, stderr=PIPE, stdout=PIPE)
                        command.wait()

                        # Third: mounting ISO file to /tmp/WindowsData
                        npyscreen.notify_wait(f"Mounting {burnISO} to /tmp/WindowsData", "PROGRESS")
                        mounts = ['mount', f'{burnISO}', '/tmp/WindowsData']
                        command = Popen(mounts, stderr=PIPE, stdout=PIPE)
                        command.wait()
                    except:
                        npyscreen.notify_confirm("An error occured while mounting files. Quitting!!", "ERROR")
                        sys.exit(1)

                    # Copy time !!!
                    npyscreen.notify_wait("Copying files to target partition. It will take a while!!", "WAIT")
                    copytree("/tmp/WindowsData", "/mnt")

                    # Syncing all
                    npyscreen.notify_wait("Syncing all data. Please wait!!", "WAIT")
                    syncing = ['sync']
                    command = Popen(syncing, stderr=PIPE, stdout=PIPE)
                    command.wait()

                    try:
                        # Writing Microsoft boot records
                        npyscreen.notify_wait(f"Writing Windows boot record to /dev/{burnPart}1", "PROGRESS")
                        writeboo = ['ms-sys', '-n', f'/dev/{burnPart}1']
                        command = Popen(writeboo, stderr=PIPE, stdout=PIPE)
                        command.wait()

                        # Writing Windows MBR to given partition
                        npyscreen.notify_wait(f"Writing Windows MBR to /dev/{burnPart}", "PROGRESS")
                        writembr = ['ms-sys', '-7', f'/dev/{burnPart}']
                        command = Popen(writembr, stderr=PIPE, stdout=PIPE)
                        command.wait()
                    except:
                        npyscreen.notify_confirm(
                            "An error occured while writing boot records.\nMake sure you have >ms-sys< installed correctly.",
                            "ERROR"
                        )
                        sys.exit(1)

                    # Syncing all again
                    npyscreen.notify_wait("Syncing all data. Please wait!!", "PROGRESS")
                    command = Popen(syncing, stderr=PIPE, stdout=PIPE)
                    command.wait()

                    # Enabling boot flag
                    npyscreen.notify_wait(f"Enabling boot flag on /dev/{burnPart}", "PROGRESS")
                    bootflag = ['parted', '--script', f'/dev/{burnPart}', 'set', '1', 'boot', 'on']
                    command = Popen(bootflag, stderr=PIPE, stdout=PIPE)
                    command.wait()

                    # Umounting target USB partition
                    npyscreen.notify_wait(f"Umounting /dev/{burnPart}1", "PROGRESS")
                    umount = ['umount', f'/dev/{burnPart}1']
                    command = Popen(umount, stderr=PIPE, stdout=PIPE)
                    command.wait()

                    # Umounting target ISO file
                    npyscreen.notify_wait(f"Umounting {burnISO}", "PROGRESS")
                    umount = ['umount', '/tmp/WindowsData']
                    command = Popen(umount, stderr=PIPE, stdout=PIPE)
                    command.wait()

                    # Removing WindowsData folder and finish.
                    removv = ['rm', '-rf', '/tmp/WindowsData']
                    command = Popen(removv, stderr=PIPE, stdout=PIPE)
                    command.wait()
                    npyscreen.notify_confirm("Now you can use your USB ;)", "NOTIFICATION")

                else:
                    # ---------- LINUX PENDRIVE ----------
                    npyscreen.notify_wait("Creating Linux pendrive...", "NOTIFICATION")

                    # Wiping all data
                    npyscreen.notify_wait(f"Wiping all data on /dev/{burnPart}", "PROGRESS")
                    wiper = ['wipefs', '--all', f'/dev/{burnPart}']
                    command = Popen(wiper, stderr=PIPE, stdout=PIPE)
                    command.wait()

                    # Creating loop label on target USB drive
                    npyscreen.notify_wait(f"Creating LOOP label on /dev/{burnPart}", "PROGRESS")
                    labelz = ['parted', '--script', f'/dev/{burnPart}', 'mklabel', 'loop']
                    command = Popen(labelz, stderr=PIPE, stdout=PIPE)
                    command.wait()

                    # Creating ext4 file system on target USB drive
                    npyscreen.notify_wait(f"Creating EXT4 file system on /dev/{burnPart}", "PROGRESS")
                    cmdline = ['mkfs.ext4', f'/dev/{burnPart}']
                    command = Popen(cmdline, stderr=PIPE, stdout=PIPE)
                    command.wait()

                    # Copying files from ISO to target partition
                    npyscreen.notify_wait(f"Burning {burnISO} to /dev/{burnPart}.\nIt will take a while!!", "WAIT")
                    cmdline = ['dd', 'bs=4M', f'if={burnISO}', f'of=/dev/{burnPart}', 'status=none', 'oflag=sync']
                    command = Popen(cmdline, stderr=PIPE, stdout=PIPE)
                    command.wait()
                    npyscreen.notify_confirm("Now you can use your USB ;)", "NOTIFICATION")
            except:
                npyscreen.notify_confirm(f"Please specify pendrive type and target partition!!", "ERROR")
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
            'MAIN', MainForm, name='pyXuSB Pendrive Creator v0.3',
            lines=30, columns=90
        )

# Execution area
if __name__ == '__main__':
    try:
        app = MainApp()
        app.run()
    except KeyboardInterrupt:
        print("[+] Goodbye...")
        sys.exit(0)
