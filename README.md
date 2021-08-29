# rehearsal-recording
An easy tool to record your rehearsals. 

## Architecture

## Raspberry Pi: Embedded software
The Raspberry Pi runs a Linux operating system. A Python application will be started as main application. This application connects to the MQTT bus to recieve commands and send information. The Python application requires to be very stable. Therefore, the design pattern "state machine" is implemented. The software is able to be in certain states. Events are used to transition from one state to another. These events can be generated from different sources, like the MQTT bus or hardware switches.

### Finite state machine design
The following finite state machine has been developed:

![fsm]

#### START
When the Raspberry Pi is started, it will startup Linux and all required resources. As last, the Python application is started. When the initialisation is ready, the READY event is generated. It will go to the IDLE state.

#### IDLE
In this state, the software is waiting on the INITIATE event. At this moment, no user is using the recording application. In order to use the product, it is required to link the client application (usually a mobile web application) with this software. Initiation is done by pressing the button and initiates the event INITIATE and will go to the LINK state.

#### LINK
When the button is clicked over MQTT a message is sent that the device wants to link itself to a client. During the LINK state, the device expect two values from the client. One value below the 10 that represents the number of times, the button must be pressed. The second value represents the ID of the client, so the device knows that is must listen to these commands. When this proces takes too much time, a TIMEOUT event is generated and the proces will stop. When it is successfull, a READY event is generated and the client and the software is linked together.

#### WAIT
The software waits on commands from the client. In this case, the client is able to start a record. When the software does not recieve for a time commands from the client, and a TIMEOUT event will be generated. It will stop the link with the client and new clients can be accepted. The client is also able to send a LOGOUT event to stop de link with the client. When the client want to record a new song, it sends a RECORD event. This event can contain the name of the song. When the song alreay exists (even when the date is put before the name) it appends the number of takes of the song. During this state, the client is able to send configuration data to setup the microphone for recording.

#### RECORD
The software starts recording from the microphone as source. When the client submits the event STOP, the recording is stopped and the state SAVE is activated.

#### SAVE
During this state, the recording is saved to the server, so the client is able to download the recordings. When the recording is saved, the event READY is triggered.


[fsm]: images/fsm.png "Finite State Machine"