import mongo_db_interactions as mongo
import time
import os
#load the data textfile and returns a list of the elements of the latest line logged
def get_data_from_text_file(fname):
    with open(fname) as infile:
        data_list = [line.rstrip("\n") for line in infile]
        data = data_list[-1].split()
    return data

#write data from textfile into the database
def txt_to_db():
    data = get_data_from_text_file("assets/data.txt")
    id=data[0]
    temperature = data[1]
    humidity = data[2]
    battery = data[3]
    mongo.write_data(id,temperature,humidity,battery)

if __name__ == '__main__':
    last_change = 0
    while True:
        time.sleep(0.1)
        if os.stat("assets/data.txt").st_mtime != last_change:
            txt_to_db()
            last_change = os.stat("assets/data.txt").st_mtime