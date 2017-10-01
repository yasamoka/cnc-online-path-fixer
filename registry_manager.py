import winreg
import sys

class RegistryManager:
  REG_KEYS = (
    "SOFTWARE\\Electronic Arts\\EA Games\\Command and Conquer Generals Zero Hour",
    "SOFTWARE\\WOW6432Node\\Electronic Arts\\EA Games\\Command and Conquer Generals Zero Hour",
  )

  SUBKEYS = (
    "ergc",
  )

  VALUES = (
    ("InstallPath", winreg.REG_SZ),
    ("Language", winreg.REG_SZ),
    ("Version", winreg.REG_DWORD),
  )

  def __init__(self):
    self.__exists = self.__locate()

  def __locate(self):
    key_found = False
    for reg_key in RegistryManager.REG_KEYS:
      try:
        self.__key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_key, 0, winreg.KEY_ALL_ACCESS)
        self.__reg_key = reg_key
        key_found = True
        break
      except OSError:
        pass

    if key_found:
      return True
    else:
      return False

  def exists(self):
    return self.__exists

  def __refresh(self):
    try:
      winreg.CloseKey(self.__key)
      self.__key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, self.__reg_key, 0, winreg.KEY_ALL_ACCESS)
    except OSError:
      raise Exception("Zero Hour registry key was deleted during runtime.")
    self.__values = self.__get_values(self.__key)

  def __get_values(self, key):
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

  def __getValue(self, value_idx):
    if not self.__exists:
      return None
    self.__refresh()
    value_name, value_type = RegistryManager.VALUES[value_idx]
    if value_name in self.__values.keys():
      return self.__values[value_name][1]
    else:
      return None

  def __setValue(self, value_idx, value_type, value):
    if not self.__exists:
      return False
    value_name, value_type = RegistryManager.VALUES[value_idx]
    winreg.SetValueEx(self.__key, value_name, 0, value_type, value)
    return True

  def getInstallPath(self):
    return self.__getValue(0)

  def getLanguage(self):
    return self.__getValue(1)

  def getVersion(self):
    return self.__getValue(2)

  def setInstallPath(self, data):
    return self.__setValue(0, winreg.REG_SZ, data)