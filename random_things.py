'''           testing the driver by openning my Git account

from msedge.selenium_tools import Edge, EdgeOptions

options = EdgeOptions()

options.use_chromium = True
driver = Edge(options=options)

driver.get('https://github.com/FranciscoMFR')

'''

import time
# ts stores the time in seconds
ts = time.time()
  
# print the current timestamp
print(ts)