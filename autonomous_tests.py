import unittest
from autonomous import *

class TestStringMethods(unittest.TestCase):

    def test_with_hello(self):
        message = process_message_hello(0, "hello sky")
        self.assertEqual(message, "hello sky")

    def test_without_hello(self):
        message = process_message_hello(0, "crypto sky")
        self.assertEqual(message, "")

    def test_integration_two_messages(self):
        limit_messages = 2
        num_agents = 2
        box = InOutBox(num_agents)
        seed(0)

        # Initialize agents, register message handlers and behaviours and start tasks asynchronously
        agents = []
        threads = []
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

        for i in range(num_agents):
            self.assertEqual(agents[i].num_messages_sent, limit_messages)
            self.assertEqual(agents[i].num_messages_recieved, limit_messages)

if __name__ == '__main__':
    unittest.main()
