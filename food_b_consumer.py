"""
    This program listens for work messages contiously. 
    Start multiple versions to add more workers.  

### Name:  Jonathan Nkangabwa
### Date:  February 16, 2023
"""

import pika
import sys
import time
from collections import deque
#####################################################################################

# define variables 
host = "localhost"
food_b_queue = '03-food-B' #correct form of queue name


#######################################################################################
# defining deque

food_b_deque = deque(maxlen=20) # limited to 20 items (the 20 most recent readings)


#We want know if: food A temp. changes less than 1 degrees F in 10 min; trigger food stall alert!



food_stall_alert_limit = 1 # if temp decreased by this , send a food stall alert
#Any food temperature changes less than 1 degree F in 10 minutes (food stall!)

#######################################################################################
## define delete_queue
def delete_queue(host: str, queue_name: str):
    """
    Delete queues each time we run the program to clear out old messages.
    """
    conn = pika.BlockingConnection(pika.ConnectionParameters(host))
    ch = conn.channel()
    ch.queue_delete(queue=queue_name)
########################################################################################
# defining callback for food B queue

def food_B_callback(ch, method, properties, body):
    """ Define behavior on getting a message about the foodA temperature."""
    # decode the binary message body to a string
    message = body.decode()
    print(f" [x] Received {message} on 03 -food-B")
    # acknowledge the message was received and processed 
    # (now it can be deleted from the queue)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    time.sleep(1)
    # def smoker deque queue
    # adding message to the smoker deque
    food_b_deque.append(message)

    # identifying first item in the deque
    food_b_deque_temp = food_b_deque[0]
    # splitting date & timestamp from temp in column
    # will now have date & timestamp in index 0 and temp in index 1
    # this will be looking at what occurred 10mins prior (20 messages ago)
    food_b_deque_split = food_b_deque_temp.split(",")
    # converting temp in index 1 to float and removing last character  
    food_b_temp_1 = float(food_b_deque_split[1][:-1])
   
    # defining current food B temp
    food_b_curr_temp = message
    # splitting date & timestamp from temp in column
    # will now have date & timestamp with index 0 and temp with index 1
    # this will be looking at what occurred 10 mins prior (20 messages ago)
    food_b_curr_column = food_b_curr_temp.split(",")     
    # converting temp in index 1 to float and removing last character    
    food_b_now_temp = float(food_b_curr_column[1][:-1])
    
    # defining food B temperature change and calculating the difference
    # rounding difference to 1 decimal point
    food_b_temp_change = round(food_b_now_temp - food_b_temp_1, 1)
    # defining smoker alert
    if food_b_temp_change >= food_stall_alert_limit:
        print(f" FOOD STALL!! The temperature of the food has changed by 1 degree or less in 10 min (or 20 readings). \n          foodB temp change = {food_b_temp_change} degrees F = {food_b_now_temp} - {food_b_temp_1}")
       

# define a main function to run the program
def main(hn: str, qn: str):
    """ Continuously listen for task messages on a named queue."""

    # when a statement can go wrong, use a try-except block
    try:
        # try this code, if it works, keep going
        # create a blocking connection to the RabbitMQ server
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=hn))

    # except, if there's an error, do this
    except Exception as e:
        print()
        print("ERROR: connection to RabbitMQ server failed.")
        print(f"Verify the server is running on host={hn}.")
        print(f"The error says: {e}")
        print()
        sys.exit(1)

    try:
        # use the connection to create a communication channel
        channel = connection.channel()

        # use the channel to declare a durable queue
        # a durable queue will survive a RabbitMQ server restart
        # and help ensure messages are processed in order
        # messages will not be deleted until the consumer acknowledges
        channel.queue_declare(queue=food_b_queue, durable=True)

        # The QoS level controls the # of messages
        # that can be in-flight (unacknowledged by the consumer)
        # at any given time.
        # Set the prefetch count to one to limit the number of messages
        # being consumed and processed concurrently.
        # This helps prevent a worker from becoming overwhelmed
        # and improve the overall system performance. 
        # prefetch_count = Per consumer limit of unaknowledged messages      
        channel.basic_qos(prefetch_count=1) 

        # configure the channel to listen on a specific queue,  
        # use the callback function named callback,
        # and do not auto-acknowledge the message (let the callback handle it)
        channel.basic_consume( queue=food_b_queue, on_message_callback=food_B_callback)
        # print a message to the console for the user
        print(" [*] Ready for work. To exit press CTRL+C")

        # start consuming messages via the communication channel
        channel.start_consuming()

    # except, in the event of an error OR user stops the process, do this
    except Exception as e:
        print()
        print("ERROR: something went wrong.")
        print(f"The error says: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print()
        print(" User interrupted continuous listening process.")
        sys.exit(0)
    finally:
        print("\nClosing connection. Goodbye.\n")
        connection.close()


# Standard Python idiom to indicate main program entry point
# This allows us to import this module and use its functions
# without executing the code below.
# If this is the program being run, then execute the code below
if __name__ == "__main__":
    # call the main function with the information needed
    main(host, food_b_queue)