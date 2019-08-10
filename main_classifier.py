import numpy as np
from swipe_classifier import swipe_prediction
from twirl_neural_network import neural_network

gesture_type = 0
gesture_length = 20  # length of gesture
counter_for_prediction = 0
prediction_result = 0
counter = 0
wt_range_arr = np.zeros(gesture_length, 'float32')
wt_doppler_arr = np.zeros(gesture_length, 'float32')
range_disp_arr = np.zeros(gesture_length, 'float32')
vel_disp_arr = np.zeros(gesture_length, 'float32')
angle_arr = np.zeros(gesture_length, 'float32')
inst_energy_arr = np.zeros(gesture_length, 'float32')
num_detectpts_arr = np.zeros(gesture_length, 'float32')
# statistics for twirl detection
twirl_range_avg = np.zeros(100, dtype='float32')
twirl_avg_neg_doppler = np.zeros(100, dtype='float32')
twirl_avg_pos_doppler = np.zeros(100, dtype='float32')
twirl_pos_num_detections = np.zeros(100, dtype='float32')
twirl_neg_num_detections = np.zeros(100, dtype='float32')
twirl_angle_val = np.zeros(100, dtype='float32')


def process_gesture_metrics(data_buffer, packet_size, num_packets):
   global gesture_type
   if twirl_detect(data_buffer, packet_size, num_packets) == 1:
       return 1
   elif twirl_detect(data_buffer, packet_size, num_packets) == -1:
       return 2
   else:
       gesture_metrics = np.reshape(data_buffer, (num_packets, packet_size))
       for i in range(4):
           if swipe_detect(gesture_metrics[i, :]) == 1:
               return 3
       return 0


def twirl_detect(data_buffer, packet_size, num_packets):

   global twirl_range_avg, twirl_avg_neg_doppler, twirl_avg_pos_doppler, twirl_pos_num_detections
   global twirl_neg_num_detections, twirl_angle_val
   global counter
   global nn_input_data
   global y
   l_training = 10

   data_temp = np.reshape(data_buffer, (packet_size, num_packets))
   twirl_range_avg = np.append(twirl_range_avg[num_packets:12], data_temp[3, :])
   twirl_avg_neg_doppler = np.append(twirl_avg_neg_doppler[num_packets:12], data_temp[8, :])
   twirl_avg_pos_doppler = np.append(twirl_avg_pos_doppler[num_packets:12], data_temp[5, :])
   twirl_pos_num_detections = np.append(twirl_pos_num_detections[num_packets:12], data_temp[4, :])
   twirl_neg_num_detections = np.append(twirl_neg_num_detections[num_packets:12], data_temp[7, :])
   twirl_angle_val = np.append(twirl_angle_val[num_packets:12], data_temp[12, :])

   nn_input = np.concatenate((twirl_pos_num_detections[(np.size(twirl_pos_num_detections) - l_training):],
                              twirl_neg_num_detections[(np.size(twirl_neg_num_detections)) - l_training:],
                              twirl_avg_pos_doppler[(np.size(twirl_avg_pos_doppler) - l_training):],
                              twirl_avg_neg_doppler[(np.size(twirl_avg_neg_doppler) - l_training):],
                              twirl_range_avg[(np.size(twirl_range_avg)) - l_training:]), axis=None)
   nn_input = np.array(nn_input)[np.newaxis]
   nn_output = neural_network(nn_input.T)

   l_one = 11
   angle_val_temp = twirl_angle_val[(np.size(twirl_angle_val) - l_one):] - np.average(twirl_angle_val)
   corr_one = np.sum(
       np.multiply(angle_val_temp, twirl_pos_num_detections[(np.size(twirl_pos_num_detections) - l_one):]))
   corr_two = np.sum(
       np.multiply(angle_val_temp, twirl_neg_num_detections[(np.size(twirl_neg_num_detections) - l_one):]))
   c_one = (np.sum(twirl_pos_num_detections[(np.size(twirl_pos_num_detections) - l_one):]) > 20) & \
           (np.sum(twirl_neg_num_detections[(np.size(twirl_neg_num_detections) - l_one):]) > 20)
   if(corr_two>0):
        return 1
   else:
        return 0

def swipe_detect(gesture_metrics):
   global gesture_length
   range_res = 0.046875
   vel_res = 0.0380479
   global wt_range_arr
   global wt_doppler_arr
   global range_disp_arr
   global vel_disp_arr
   global angle_arr
   global inst_energy_arr
   global num_detectpts_arr
   for i in range(0, gesture_length - 1):
       # set each element to the next one; cycling through the arrays
       wt_range_arr[i] = wt_range_arr[i + 1]
       wt_doppler_arr[i] = wt_doppler_arr[i + 1]
       range_disp_arr[i] = range_disp_arr[i + 1]
       vel_disp_arr[i] = vel_disp_arr[i + 1]
       inst_energy_arr[i] = inst_energy_arr[i + 1]
       num_detectpts_arr[i] = num_detectpts_arr[i + 1]
       angle_arr[i] = angle_arr[i + 1]

   # set each array to appropriate gesture metric
   wt_range_arr[gesture_length - 1] = gesture_metrics[3] * range_res
   wt_doppler_arr[gesture_length - 1] = gesture_metrics[2] * vel_res
   range_disp_arr[gesture_length - 1] = gesture_metrics[9] * range_res
   vel_disp_arr[gesture_length - 1] = gesture_metrics[10] * vel_res
   inst_energy_arr[gesture_length - 1] = gesture_metrics[4]
   num_detectpts_arr[gesture_length - 1] = gesture_metrics[1]
   angle_arr[gesture_length - 1] = (180.0 * np.arcsin((gesture_metrics[12] / 32.0))) / 3.1415
   global prediction_result
   global counter_for_prediction
   if (prediction_result != 1) | (counter_for_prediction > 15):
       prediction_result = swipe_prediction(wt_range_arr, wt_doppler_arr, range_disp_arr, vel_disp_arr,
                                            inst_energy_arr, num_detectpts_arr, angle_arr)
       counter_for_prediction = 0
       return prediction_result

   else:
       counter_for_prediction += 1

