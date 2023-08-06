from __future__ import absolute_import, division, print_function

from dnaStreaming.listener import Listener

listener = Listener()


def callback(message, subscription_id):
	relevent_section = message["data"][0]["attributes"]

	if relevent_section["action"] == "del":
	    with open("Output.txt", "w+") as text_file:
	        text_file.write(str(relevent_section["an"]) + ",")

    return True  # If desired return False to stop the message flow. This will unblock the process as well.


listener.listen(callback)