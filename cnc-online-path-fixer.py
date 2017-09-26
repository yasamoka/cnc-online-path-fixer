import winreg
import sys
import os

REG_KEYS = (
  ("Zero Hour Retail / Origin (32-bit Windows)", "SOFTWARE\\Electronic Arts\\EA Games\\Command and Conquer Generals Zero Hour"),
  ("Zero Hour Retail / Origin (64-bit Windows)", "SOFTWARE\\WOW6432Node\\Electronic Arts\\EA Games\\Command and Conquer Generals Zero Hour"),
)

SUBKEYS = (
  "ergc",
  )

VALUES = (
  "Language",
  "UserDataLeafName",
  "Version",
  "MapPackVersion",
  "InstallPath",
  )

def get_subkeys(key):
  i = 0
  subkeys = list()
  while True:
    try:
      subkey = winreg.EnumKey(key, i)
      subkeys.append(subkey)
      i += 1
    except OSError as e:
      break
  return subkeys

def get_values(key):
  i = 0
  values = dict()
  while True:
    try:
      value = winreg.EnumValue(key, i)
      values[value[0]] = value
      i += 1
    except OSError as e:
      break
  return values

key_found = False
for reg_key in REG_KEYS:
  description, path = reg_key
  try:
    print("Attempting to open {} registry key ... ".format(description), end='')
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_ALL_ACCESS)
    print("success.")
    key_found = True
    break
  except OSError:
    print("not found", end='')
    pass
  print(".")

if not key_found:
  print("No registry key found. Exiting ...")
  sys.exit(0)

print()

subkeys_found = get_subkeys(key)
values_found = get_values(key)

for subkey in SUBKEYS:
  print("Searching for subkey \"{}\" ... ".format(subkey), end='')
  if subkey in subkeys_found:
    print("found", end='')
  else:
    print("not found", end='')
  print(".")

for value in VALUES:
  print("Searching for value \"{}\" ... ".format(value), end='')
  if value in values_found.keys():
    print("found (\"{}\")".format(values_found[value][1]), end='')
  else:
    print("not found", end='')
  print(".")

zero_hour_install_path = input("Enter the Zero Hour install path: ")
try:
  assert os.path.isdir(zero_hour_install_path)
except AssertionError:
  print("Directory does not exist. Exiting ...")
  sys.exit(0)

print("Setting value \"InstallPath\" data to \"{}\" ... ".format(zero_hour_install_path), end='')
winreg.SetValueEx(key, "InstallPath", 0, winreg.REG_SZ, zero_hour_install_path)
print("done.")