from nose.tools import *
from nordnet.feeds import *
#from mock import Mock, MagicMock
from exam.mock import Mock

def test_read_part_of_message():
	msg1 = "{"
	msg2 = "1"
	msg3 = "}\n{"
	msg4 = "2}\n"
	msg5 = "{3}\n{4"

	ih = FeedInputHandler()
	ih.handle_data_chunk = Mock()
	
	ih.handle_input(msg1)
	ok_(not ih.handle_data_chunk.called)

	ih.handle_input(msg2)
	ok_(not ih.handle_data_chunk.called)

	ih.handle_input(msg3)
	ih.handle_data_chunk.assert_called_with( '{1}')

	ih.handle_data_chunk.reset_mock()
	ih.handle_input(msg4)
	ih.handle_data_chunk.assert_called_with( '{2}')
	#ih.handle_data_chunk.assert_not_called_with( '{1}')

	############
	# Can not get assert_not_called_with to work, aserting the
	# buffered input instead
	ok_(ih.buffered_input == '', "input should be empty, but was '%s'" % ih.buffered_input)
	print "+"*35
	print "buffered input: '%s'" % ih.buffered_input

	ih.handle_input(msg5)
	#ih.handle_data_chunk.assert_not_called_with( '{1}')
	#ih.handle_data_chunk.assert_not_called_with( '{2}')
	ih.handle_data_chunk.assert_called_with( '{3}')
	ok_(ih.buffered_input == '{4', "input should be '{4', but was '%s'" % ih.buffered_input)
	
	
