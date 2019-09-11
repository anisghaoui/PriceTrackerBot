import PriceTrackerBot as ptb

if __name__ == '__main__':
	bot = ptb.PriceTrackerBot()
	bot.run(1) # in days. if no arguments : keeps running
	print("done")
	