from nose.tools import *
from nordnet.feeds import *
from mock import Mock, MagicMock


def test_read_part_of_message():
	msg1 = "{"
	msg2 = "   "
	msg3 = "}"

	ih = FeedInputHandler()
	ih.postData = Mock()
	
	ih.handle_input(msg1)
	ok_(not ih.postData.called)

	ih.handle_input(msg2)
	ok_(not ih.postData.called)

	ih.handle_input(msg1)
	ih.postData.assert_called_with( msg1 + msg2 + msg3)
