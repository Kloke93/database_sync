SyncDataBase defines a database based 
on a python dictionary serialized in a file and synchronized. 
It is intended to be used through threading and multiprocessing:
SyncDataBase(mode, file_name="dbfile.bin"):
* 'mode' is a flag where 0 is multiprocessing and 1 is threading
* 'file_name' indicates where is the database file located

There are three possible actions:
1) set_value(key, val) takes a key and sets a value for it in the dictionary and returns if the operation was successful
2) get_value(key) searches a value according to the given key and returns it if found (if not it returns none)
3) delete_value(key) deletes key:value pair and returns the value deleted (if nothing was deleted it returns none)