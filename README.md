# Autonomous agents
The goal of this project is to simulate a behavior of two autonomous agents
that communicate asynchronously.

## Project directory scope
The directory consists of the following files:

- `autonomous.py` - code implementation;
- `autonomous_tests.py` - a couple of unit and one integration test

## Design and implementation
There are two major abstractions that could be extracted from the problem definition:
agents and in-out-box for the agents message exchange. For these purposes, two classes
were defined: `Agent` and `InOutBox`. In reality, the concept would include more
abstractions, i.e., messages themselves, buffers, connectors, etc. However, the
simplified version of the task allows us to work with just two classes.

Since message handler and agent behavior can be specified, it is logical to implement
the specified handler and behavior as separate functions and have the ability to provide
them as function pointers in the `Agent` class.

The `InOutBox` class is implemented with the concept of the queue, where each queue
corresponds to a specific agent and serves as an in- and out-box as specified by the
problem definition.

The number of agents is set to two, however the program can be easily adapted for more
agents. The logic of the program is loop-based and not constrained by the number of
agents. There is a possibility to set the list of agents which specifies where the local
agent is going to send messages to.

Threads were chosen as a means to provide asynchronous behavior. Every agent acts
independently and does not prevent another agent from sending or receiving a message.
When the message is generated, it is sent to another (all) agent(s). At the same time,
when the in-out-box is not empty for a local agent, it extracts all available messages
in one shot to avoid queue overflow, which obviously does not happen in the specified
scenario.

We assume that the program stops when each agent sends and receives a specified number
of messages, which is the same for every agent in this exercise. Obviously, the stopping
condition can be modified to account, i.e., for other combinations of sends and receives;
the requirement of sending specific messages stating that the communication is over; or
providing a time limit for message exchange; etc.

There are a lot of simplicities that were implied by the project definition. For example,
two seconds on nowadays machines is more than enough time to send message(s) to agent(s),
and receive message(s), if any, such that the loop for sending-receiving messages triggers
the time for generating a new message almost exactly at every two seconds. Otherwise,
we would need to take the message generation routine as a stand-alone thread (and
ultimately a class abstraction) and check if the new message is generated. At the same
time, to avoid in-out-box overflow, we would need to create yet another abstraction that
tracks the number of received messages and extracts a specific number from one to all of
them, ultimately leading to the in-out-message scheduler implementation.

Python version 3.8.5 was used to implement the project.

## Usage
The program usage is as follows:

`python3 autonomous.py [limit_number_messages]`

By default, the limit of the number of messages to exchange between agents is set to 10.
This number can be supplied as an argument from the command line. The assumption is that
the provided command line number does not need to undergo the dummy test, i.e. it is a
positive integer number.

Other parameters are hardcoded in the code, however can be easily adjusted, if the
project needs further adaptation. This includes the number of agents, the time interval
for random message generation, and the ability to define other message handlers and
agent behaviors.

## Tests
For the testing purposes, run the following command:

`python3 autonomous_tests.py`

Two unit tests check if the message generation routine provides a correct output message
based on the input parameters. The integration test checks that the number of sent and
received messages is exactly equal to two for both agents.