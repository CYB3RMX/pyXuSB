#!/usr/bin/python3

import npyscreen
import os
import sys
import psutil

# Checking permissions
if int(os.getuid()) != 0:
	print("You need root permissions to use this tool.")
	sys.exit(1)

# Enumerating all partitions
try:
	command = "lsblk -o name -n -s -l > parts.txt"
	os.system(command)
	partitions = open("parts.txt", "r").readlines()
except:
	print("An error occured while enumerating disk partitions.")
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
			max_width=self.x // 2
		)
		self.diskParts = self.add(
			npyscreen.TitleCombo, name='Select USB partition',
			values=partitions, rely=10
		)
		self.add(
			npyscreen.ButtonPress, name="Start Burning!!",
			when_pressed_function=self.Burner, relx=15,
			rely=15
		)
		self.add(
			npyscreen.ButtonPress, name="Exit",
			when_pressed_function=self.ExitButton, relx=15
		)
	def afterEditing(self):
		pass
	
	def ExitButton(self):
		exiting = npyscreen.notify_yes_no(
			"Are you sure to quit pyXuSB?", "Notification",
			editw=2
		)
		if exiting:
			self.parentApp.setNextForm(None)
			if os.path.exists("parts.txt"):
				os.remove("parts.txt")
			sys.exit(0)
		else:
			pass

	def Burner(self):
		# Checking existence for target file
		if os.path.exists(self.isoFile.value):
			pass
		else:
			npyscreen.notify_confirm(
						"Target file not found quitting!!"
					)
			sys.exit(0)

		# Asking for user
		question = npyscreen.notify_yes_no(
			"Are you sure to continue?", "Notification",
			editw=2
		)
		if question:
			npyscreen.notify_confirm(
				f"Burning {self.isoFile.value} to {self.diskParts.values[self.diskParts.value]}"
			)
			command = f"dd bs=4M if={self.isoFile.value} of=someEmpty.dd conv=fdatasync status=none"
			os.system(command)
			while True:
				if "dd" in (proc.name() for proc in psutil.process_iter()):
					pass
				else:
					npyscreen.notify_confirm(
						"ISO burning is completed now you can use your USB ;)"
					)
					break
		else:
			pass

# Class for main application
class MainApp(npyscreen.NPSAppManaged):
	def onStart(self):
		npyscreen.setTheme(npyscreen.Themes.TransparentThemeLightText)
		self.addForm(
			'MAIN', MainForm, name='pyXuSB ISO File Burner v0.1',
			lines=30, columns=90
		)

if __name__ == '__main__':
	try:
		app = MainApp()
		app.run()
		if os.path.exists("parts.txt"):
			os.remove("parts.txt")
	except KeyboardInterrupt:
		print("Goodbye...")
		if os.path.exists("parts.txt"):
			os.remove("parts.txt")
