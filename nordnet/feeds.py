class FeedInputHandler():
	def __init__(self):
		self.buffered_input = ''

	def handle_input(self, input):
		self.buffered_input = self.buffered_input + input
		split_input = self.buffered_input.split('\n')
		complete_chunks = split_input[0:-1]

		for chunk in complete_chunks:
			self.handle_data_chunk(chunk)

		# remove the handled chunks from buffered input
		self.buffered_input = ''.join(split_input[-1:])

	def handle_data_chunk(self, chunk):
		pass