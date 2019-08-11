# IWR1443-Gesture-Classifier
Python program to receive data from TI IWR1443 mmWave sensor and classify twirl and swipe motions. The TI gesture demo was ported over from IWR1443 ES 2.0 to IWR1443 ES 3.0. The program has been tested in both Windows and Linux and can accurately determine the occurrence of a twirl or swipe motion.

The program configures serial ports and sends over a sensor chirp configuration file. It then receives metrics for the gesture classification from the mmmWave sensor. The metrics are then passed into a two layer neural network in order to determine whether there was an occurrence of a twirl or a swipe. Two neural networks are included, one ported over from the TI Matlab demo, and one we constructed to more effectively classify the gestures. If no twirl is detected, the data is passed through a handcrafted gesture classifier from the TI library. Currently most of the false detection analysis is not needed, however it is provided in the case of environmental differences.

Although the swipe and twirl occurrence detection works accurately, the neural network still needs to be improved and trained. In addition, the mmWave sensor can return different data depending on the environment. Because the project is still in development, please feel free to contact about any questions or ideas.

# Required Python Packages
numpy - array manipulations and neural network

pyserial - receive data from the sensor over serial

# Python Files
main_gesture.py
- send_config_to_sensor(p_form, config_file): Takes platform and config fileas parameters. It initializes serial ports and sends config file to sensor. Returns cli and data port serial objects
- process_data(data_port): Takes data_port as parameter. It is the main data path, reads data buffer obtaining 4 packets from the sensor, and then callsgesture classification functions. Prints type of gesture.
main_classifier.py

