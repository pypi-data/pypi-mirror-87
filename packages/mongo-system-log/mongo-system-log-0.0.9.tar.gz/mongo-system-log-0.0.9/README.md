The idea behind this package is possibility to you use some client or something like the Metabase for collect and analyse logs of your application. Its need two environments variables:  
* MONGO_DB  
* MONGO_URL    

Its works with two collections:  
* error  
* info

sample  
~~~python
from mongo_system_log import *
log = LogThis(get_module_name())
log.error('error message')
log.info('info message')
~~~
get_module_name()  
* This function gets module and file name that called it. Must be called on instantiate the LogThis class.

