'''
Questions:
1. What is the relationship between the time to process versus the number of CPUs?
   Does there appear to be an asymptote? If so, what do you think the asymptote is?
   >
      The time to process exponentially decreases as the number of CPUs increase. It seems to steady out near the end when 
      the CPU count for my machine is reached.
   >
2. Is this a CPU bound or IO bound problem? Why?
   >
      CPU bound problem because it relies on the CPUs of your computer to run and that determines what the results of the time will be
      for the program.
   >
3. Would threads work on this assignment? Why or why not? (guess if you need to) 
   >
      I am going to guess and assume that threads would work on this assignment. This is because of what I have learned about threads so far.
      Threads are able to work depending on how you set it up and execute. 
   >
4. When you run "create_final_video.py", does it produce a video with the elephants
   inside of the screen?
   > Yes, it does produce the video.
'''

from matplotlib.pylab import plt  # load plot library
from PIL import Image
import numpy as np
import timeit
import multiprocessing as mp

# 4 more than the number of cpu's on your computer
CPU_COUNT = mp.cpu_count() + 4  

FRAME_COUNT = 300

RED   = 0
GREEN = 1
BLUE  = 2


def create_new_frame(image_file, green_file, process_file):
    """ Creates a new image file from image_file and green_file """

    # this print() statement is there to help see which frame is being processed
    print(f'{process_file[-7:-4]}', end=',', flush=True)

    image_img = Image.open(image_file)
    green_img = Image.open(green_file)

    # Make Numpy array
    np_img = np.array(green_img)

    # Mask pixels 
    mask = (np_img[:, :, BLUE] < 120) & (np_img[:, :, GREEN] > 120) & (np_img[:, :, RED] < 120)

    # Create mask image
    mask_img = Image.fromarray((mask*255).astype(np.uint8))

    image_new = Image.composite(image_img, green_img, mask_img)
    image_new.save(process_file)

# this function processes each image and calling the create_new_frame function
def process(num):
   image_number = num

   image_file = rf'elephant/image{image_number:03d}.png'
   green_file = rf'green/image{image_number:03d}.png'
   process_file = rf'processed/image{image_number:03d}.png'

   create_new_frame(image_file, green_file, process_file)


if __name__ == '__main__':
    all_process_time = timeit.default_timer()

    # Use two lists: one to track the number of CPUs and the other to track
    # the time it takes to process the images given this number of CPUs.
    xaxis_cpus = []
    yaxis_times = []

   # set the cpu number to 1 so that we can start keeping track
    cpu_number = 1

    # continue in a loop for each CPU count until it reaches the global CPU_COUNT variable
    while cpu_number <= CPU_COUNT:

      start_time = timeit.default_timer()

      # using processes here and the cpu_number variable for the counter
      nums = [x for x in range(1, FRAME_COUNT +1)]
      with mp.Pool(cpu_number) as p:
         p.map(process, nums)

      time_result = timeit.default_timer() - start_time
      print(f'\nTime To Process all images with {cpu_number} cores = {time_result}')

      # append the data for the plot
      xaxis_cpus.append(cpu_number)
      yaxis_times.append(time_result)

      cpu_number += 1

    print(f'Total Time for ALL processing: {timeit.default_timer() - all_process_time}')

    # create plot of results and also save it to a PNG file
    plt.plot(xaxis_cpus, yaxis_times, label=f'{FRAME_COUNT}')
    
    plt.title('CPU Core yaxis_times VS CPUs')
    plt.xlabel('CPU Cores')
    plt.ylabel('Seconds')
    plt.legend(loc='best')

    plt.tight_layout()
    plt.savefig(f'Plot for {FRAME_COUNT} frames.png')
    plt.show()
