# taken from 
# https://stackoverflow.com/questions/6198372/most-pythonic-way-to-provide-global-configuration-variables-in-config-py/6199300#6199300
class App:
  __conf = {
    "username": "",
    "password": "",
    "MYSQL_PORT": 3306,
    "MYSQL_DB": 'mydb',
    "MYSQL_DB_TABLES": ['tb_users', 'tb_groups']
  }
  __setters = ["username", "password"]

  @staticmethod
  def config(name):
    return App.__conf[name]

  @staticmethod
  def set(name, value):
    if name in App.__setters:
      App.__conf[name] = value
    else:
      raise NameError("Name not accepted in set() method")