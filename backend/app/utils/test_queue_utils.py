import unittest
from queue_utils import pdf_analysis_queue, nlp_analysis_queue

class TestQueueSystem(unittest.TestCase):
    
    def test_pdf_queue(self):
        # Add a mock task to the PDF queue
        pdf_analysis_queue.put({'file_path': 'dummy.pdf', 'file_extension': 'pdf'})
        # Check if the queue size increased
        self.assertEqual(pdf_analysis_queue.qsize(), 1)
    
    def test_nlp_queue(self):
        # Add a mock text to the NLP queue
        nlp_analysis_queue.put({'text': 'Hello, world!'})
        # Check if the queue size increased
        self.assertEqual(nlp_analysis_queue.qsize(), 1)

if __name__ == '__main__':
    unittest.main()