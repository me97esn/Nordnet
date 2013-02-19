class FeedInputHandler():
	def __init__(self):
		self.buffered_input = ''

	def handle_input(self, input):
		self.buffered_input = self.buffered_input + input
		split_input = self.buffered_input.split('\n')
		complete_chunks = split_input[0:-1]
		
		for chunk in complete_chunks:
			print "handle chunk %s" % chunk
			self.handle_data_chunk(chunk)

		# TODO remove the handled chunks from buffered input

	def handle_data_chunk(self, chunk):
		pass