from time import sleep

def run(args, flags):
    count = 0

    while True:
        if(flags[1]):
            break
        elif(flags[2]):
            while not flags[1]:
                sleep(5)
        
        print("Still alive~ %d" % (count))
        count += 1
        
        sleep(5)

    return "i am dead now"
