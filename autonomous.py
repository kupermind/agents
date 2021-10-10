import queue
import sys
from datetime import datetime
from random import seed
from random import randint
from threading import Thread

words = ["hello", "sun", "world", "space", "moon", "crypto", "sky", "ocean", "universe", "human"]

def process_message_hello(id, message):
    """
    Function for processing a "hello" message.
    Prints the whole message if the "hello" word presents
    """

    if "hello" in message:
        print(f"Agent {id} received message:", message)
        return message

    return ""


def generate_message_two_words(last_time, seconds = 2):
    """
    Generates a two-word or an empty message using a time interval
    based on the provided last time stamp
    """

    now = datetime.now()
    if (now - last_time).total_seconds() >= seconds:
        ridx = [randint(0, 9), randint(0, 9)]
        two_words = words[ridx[0]] + " " + words[ridx[1]]
        return two_words
    else:
        return ""


class InOutBox:
    """
    Message storage class
    """

    def __init__(self, num_agents):
        self.num_agents = num_agents
        self.queues = {}
        for i in range(num_agents):
            q = queue.Queue()
            self.queues[i] = q

    def put_message(self, to, message):
        self.queues[to].put(message)

    def get_message(self, id):
        if self.queues[id].empty():
            raise ValueError(f"The InOutBox for {id} is empty")
        else:
            return self.queues[id].get()

    def empty(self, id):
        if self.queues[id].empty():
            return True


class Agent:
    """
    Autonomous agent class
    """

    def __init__(self, id, box, limit_messages):
        self.id = id
        self.num_messages_sent = 0
        self.num_messages_recieved = 0
        self.limit_messages = limit_messages
        self.message_handlers = {}
        self.message_behaviours = {}
        self.send_to = []
        self.box = box

    def register_message_handler(self, name, message_handler_function):
        if name in self.message_handlers:
            print("Warning! The handler function with that name already exists and will be overwritten!")
        self.message_handlers[name] = message_handler_function

    def register_message_behaviour(self, name, message_behaviour_function):
        if name in self.message_behaviours:
            print("Warning! The behaviour function with that name already exists and will be overwritten!")
        self.message_behaviours[name] = message_behaviour_function

    def add_send_to(self, id):
        if id not in self.send_to:
            self.send_to.append(id)


    def start(self, message_handler, message_behaviour):
        """
        Communicate messages using specified message handler and
        behavior until the exit condition is satisfied
        """

        if not message_handler in self.message_handlers:
            raise ValueError("The message handler is unknown")
        if not message_behaviour in self.message_behaviours:
            raise ValueError("The message behavior is unknown")

        limit = self.limit_messages * len(self.send_to)
        last_time_sent = datetime.now()
        while True:
            # Generate the message based on time stamp
            send_message = self.message_behaviours[message_behaviour](last_time_sent)
            if send_message:
                # Send messages to all the destinations
                last_time_sent = datetime.now()
                for i in self.send_to:
                    #print(f"sending message {self.num_messages_sent} from {self.id} to {i}:", send_message)
                    self.box.put_message(i, send_message)
                self.num_messages_sent += 1

            # Get all the messages from the box in once
            while not self.box.empty(self.id):
                receive_message = self.box.get_message(self.id)
                self.message_handlers[message_handler](self.id, receive_message)
                #print(f"{self.id} received message:", receive_message)
                self.num_messages_recieved += 1

            # For the simplicity assume that everybody sends and receives the same number of messages
            if (self.num_messages_sent == limit and self.num_messages_recieved == limit):
                break


def main():
    """
    The main function of the program
    """

    # Get the limit of number of messages to send and receive. The default limit is 10
    # Assume that the limit, if specified through the command line argument,
    # does not need to be undergo the dummy test.
    limit_messages = 10
    args = sys.argv[1:]
    if len(args) != 0:
        limit_messages = int(args[0])

    # Initialize number of agents, InOutBox
    # The number of agents is set to 2 as specified per project.
    # However the program can be easily extended to account for more agents.
    num_agents = 2
    box = InOutBox(num_agents)
    print("----- Initial setup -----")
    print(f"Number of agents: {num_agents}. Number of messages to exchange: {limit_messages}\n")

    # Initialize agents, register message handlers and behaviours and start tasks asynchronously
    agents = []
    threads = []
    print("----- Message exchange started -----")
    for i in range(num_agents):
        agent = Agent(i, box, limit_messages)
        agent.add_send_to((i + 1) % num_agents)
        agent.register_message_handler("hello", process_message_hello)
        agent.register_message_behaviour("generate", generate_message_two_words)
        agents.append(agent)
        thread = Thread(target = agent.start, args = ("hello", "generate"))
        thread.start()
        threads.append(thread)

    # Wait for all the tasks to finish
    for i in range(num_agents):
        threads[i].join()

    # Output statistics
    print("\n----- Message exchange finished -----")
    for i in range(num_agents):
        print(f"Agent {agents[i].id} sent {agents[i].num_messages_sent} messages")
        print(f"Agent {agents[i].id} received {agents[i].num_messages_recieved} messages")


if __name__ == "__main__":
    main()
