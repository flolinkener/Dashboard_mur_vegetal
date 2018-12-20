import random
import time
while True:
    time.sleep(0.5)
    file = open("assets/data.txt", "a")
    file.write(str(random.randint(1,9))+ " " +str(random.randint(1,100))+ " " +str(random.randint(1,100))+ " " +str(random.randint(1,100))+ "\n")
