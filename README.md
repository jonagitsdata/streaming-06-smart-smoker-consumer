# streaming-06-smart-smoker-consumer
## Author: Jonathan Nkangabwa
## Date: February 16th, 2023 

Continuation from module 05 by creating a consumer
## OVERVIEW:

This code takes a csv file and creates a producer with three queues. Each column of the csv will be sent to individual queues. Then, three consumers will be created to read the queues.

## BEFORE YOU BEGIN:

Before you start, make sure you have 
pika, 
deque, 
RabbitMQ, 
an active conda environment, 
and open anaconda prompt terminal installed and running.

## How to run program:

To run the program, use: 
**bbq_producer.py file** (make sure to check and update your host if needed) Also, make sure to update the 
**bbq_smoker_consumer.py**, 
**food_a_consumer.py**, 
and **food_b_consumer.py** files (with your host)
**smoker-temps.csv** (4 columns: Time, Channel1 or Smoker temp., Channel2 or Food A temp., and Channel3 or Food B temp.)
## Assignment: Smart Smoker

We monitor temperatures of a smoker and the food too ensure the food comes out cooked and delicious. Unfortunately, long cooks can occur, which can lead to:

-food temp stall, where the food hits a certain temperature and moisture ceases, so it typically will stay at this temperature for some extended period of time.
We monitor this through:

## SENSORS
Sensors will help us track the temperatures and generate a livestream of history for both our smoker and food over an extended period of time. This is time-series data, and is streaming data in motion.

## STREAMING

We will record 3 temperatures every 30 seconds (2 per minute):
- smoker temperature
- Food A's temperature
- Food B's temperature

## SIGNIFICANT EVENTS

We are curious if the smoker temperature decreases by more than 15 degrees F in 2.5 minutes(set off smoker alert) and any food temperature change less than 1 degree F in 10 minutes (set off food stall alert)

# SMART SYSTEM

We will create a Producer to simulate streaming series of temperature readings from the smoker and food. We will also create three consumers (one for each queue) to monitor temperatures streamed from producer file. They will alert us about significant events.

## CONSUMER REQUIREMENTS

- Alert sent:
    ~ smoker temp. decreases by more than 15 degrees in 2.5 min (smoker alert!)
    ~ food A or food B temp. changes less than 1 degree F in 10 min (food stall!)
- Time Windows:
    ~ smoker = 2.5 min
    ~ food A/ food B = 10 min
- Deque (Max length):
    ~ smoker deque = one reading every .5 min, max length 5 (2.5 minutes * 1 read/.5 min)
    ~ food A/B deque = one reading every .5 min, max length 20 ( 10 min * 1 read/.5 min)
- Monitoring:
    ~Smoker temp decreases by 15 F or more in 2.5 min (5 total readings) --> smoker alert!
    ~ food temp change in F is less than 1 degree or less in 10 min (20 total readings) --> food stall alert!

## OPTIONAL: Email/Text Notifications

We can also choose to have our consumers send an email or text message when a significant event occurs.

## SCREENSHOTS: **added to bottom**
<img width="1136" alt="bbq_producer" src="https://user-images.githubusercontent.com/104871382/219955506-6286dd87-bccc-4f68-b7d2-b37a0bf25c55.png">
<img width="682" alt="bbq_smoker" src="https://user-images.githubusercontent.com/104871382/219955528-db5627c3-553e-47e9-bf35-c421ca57828c.png">
<img width="638" alt="food_a_monitor" src="https://user-images.githubusercontent.com/104871382/219955557-81feaf15-18e5-42e3-9bf7-095c1addc8f5.png">
<img width="638" alt="food_b_monitor" src="https://user-images.githubusercontent.com/104871382/219955573-95762c38-8ea8-4d76-99d6-e780ac6c3bbd.png">
<img width="1430" alt="smoker_alert" src="https://user-images.githubusercontent.com/104871382/219955579-54637bd0-fc16-4733-9a49-04291bf846a5.png">
<img width="1430" alt="food_a_stall" src="https://user-images.githubusercontent.com/104871382/219955593-84d23e1c-b004-4807-b45c-8400e45d8407.png">
<img width="1430" alt="food_b_stall" src="https://user-images.githubusercontent.com/104871382/219955605-a8f7b463-798f-4233-b956-8f967b9d8513.png">
<img width="1430" alt="mod 6" src="https://user-images.githubusercontent.com/104871382/219955659-25f197a3-e330-4bc0-86e9-de6edccf2a8c.png">
