import maglev
import englishauction

from typing import Any, List, Callable

class EnglishAuction:
	"""
	An Auction Library
	Timed auction starting at a low price and increasing until no more bids are made.
	Also supports reserve price and automatic bidding.
	"""
	def __init__(self):
		bus = maglev.maglev_MagLev.getInstance("default")
		lib = englishauction.englishauction_EnglishAuction(bus)

	def Create(self, start: float, end: float, startingPrice: float, reservePrice: float, priceIncrement: float) -> str:
		"""		Create a new auction
		Args:
			start (float):start time of auction
			end (float):end time of auction
			startingPrice (float):starting price of auction
			reservePrice (float):reserve price for the auction (0 = none)
			priceIncrement (float):price increments for bids in the auction
		Returns:
			auctionId
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [start, end, startingPrice, reservePrice, priceIncrement]
		ret = None
		def Create_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('EnglishAuction.Create', args, Create_Ret)
		return ret

	def GetStart(self, auctionId: str) -> float:
		"""		Get the start of an auction
		Will return a timestamp in milliseconds
		Args:
			auctionId (str):auction id
		Returns:
			start of auction
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [auctionId]
		ret = None
		def GetStart_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('EnglishAuction.GetStart', args, GetStart_Ret)
		return ret

	def GetEnd(self, auctionId: str) -> bool:
		"""		Check if auction has ended
		Args:
			auctionId (str):auction id
		Returns:
			true if auction has ended, false otherwise
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [auctionId]
		ret = None
		def GetEnd_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('EnglishAuction.GetEnd', args, GetEnd_Ret)
		return ret

	def HasStarted(self, auctionId: str) -> bool:
		"""		Check if an auction has started yet
		Args:
			auctionId (str):auction id
		Returns:
			true if auction has started, false otherwise
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [auctionId]
		ret = None
		def HasStarted_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('EnglishAuction.HasStarted', args, HasStarted_Ret)
		return ret

	def HasEnded(self, auctionId: str) -> bool:
		"""		Check if an auction has ended yet
		Args:
			auctionId (str):auction id
		Returns:
			true if auction has ended, false otherwise
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [auctionId]
		ret = None
		def HasEnded_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('EnglishAuction.HasEnded', args, HasEnded_Ret)
		return ret

	def Bid(self, auctionId: str, userId: str, price: float):
		"""		Create a bid in an auction
		Args:
			auctionId (str):auction id
			userId (str):user id
			price (float):price bud
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [auctionId, userId, price]
		ret = None
		def Bid_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('EnglishAuction.Bid', args, Bid_Ret)

	def GetHighestBidder(self, auctionId: str) -> Any:
		"""		Get the highest bidder in an auction
		Args:
			auctionId (str):auction id
		Returns:
			
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [auctionId]
		ret = None
		def GetHighestBidder_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('EnglishAuction.GetHighestBidder', args, GetHighestBidder_Ret)
		return ret

	def GetHighestBids(self, auctionId: str, numBids: float) -> List[Any]:
		"""		Get the highest bids in an auction
		Args:
			auctionId (str):auction id
			numBids (float):max number of highest bids to return
		Returns:
			Highest bids for the specified auction
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [auctionId, numBids]
		ret = None
		def GetHighestBids_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('EnglishAuction.GetHighestBids', args, GetHighestBids_Ret)
		return ret

	def GetNumberOfBids(self, auctionId: str) -> float:
		"""		Get the number of bids in an auction
		Args:
			auctionId (str):auction id
		Returns:
			Number of bids placed in the specified auction
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [auctionId]
		ret = None
		def GetNumberOfBids_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('EnglishAuction.GetNumberOfBids', args, GetNumberOfBids_Ret)
		return ret

	def GetPriceIncrement(self, auctionId: str) -> float:
		"""		Get the price increment for the specified auction
		Args:
			auctionId (str):auction id
		Returns:
			Price increment
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [auctionId]
		ret = None
		def GetPriceIncrement_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('EnglishAuction.GetPriceIncrement', args, GetPriceIncrement_Ret)
		return ret

	def GetReservePrice(self, auctionId: str) -> float:
		"""		Get the reserve price for the specified auction
		Args:
			auctionId (str):auction id
		Returns:
			Reserve price
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [auctionId]
		ret = None
		def GetReservePrice_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('EnglishAuction.GetReservePrice', args, GetReservePrice_Ret)
		return ret

	def GetStartingPrice(self, auctionId: str) -> float:
		"""		Get the starting price for the specified auction
		Args:
			auctionId (str):auction id
		Returns:
			Starting price
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [auctionId]
		ret = None
		def GetStartingPrice_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('EnglishAuction.GetStartingPrice', args, GetStartingPrice_Ret)
		return ret

	def CalcTimeRemaining(self, auctionId: str, now: float) -> float:
		"""		Get the time remaining for the specified auction
		Args:
			auctionId (str):auction id
			now (float):current unix timestamp
		Returns:
			Time remaining in seconds
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [auctionId, now]
		ret = None
		def CalcTimeRemaining_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('EnglishAuction.CalcTimeRemaining', args, CalcTimeRemaining_Ret)
		return ret

	def CalcMinimumBid(self, auctionId: str) -> float:
		"""		Get the minimum next bid for the specified auction
		Args:
			auctionId (str):auction id
		Returns:
			Minimum bid price
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [auctionId]
		ret = None
		def CalcMinimumBid_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('EnglishAuction.CalcMinimumBid', args, CalcMinimumBid_Ret)
		return ret

	def GetAuctionsEnding(self, endfrom: float, endto: float, page: float, perpage: float, sort: str, asc: bool) -> List[Any]:
		"""		Get a list of auctions based on their end time
		Args:
			endfrom (float):end from
			endto (float):end to
			page (float):
			perpage (float):number of auctions per page
			sort (str):field to sort by
			asc (bool):ascending (true) or descending (false)
		Returns:
			List of auctions ending in the specified period
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [endfrom, endto, page, perpage, sort, asc]
		ret = None
		def GetAuctionsEnding_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('EnglishAuction.GetAuctionsEnding', args, GetAuctionsEnding_Ret)
		return ret

	def GetAuctionsStarting(self, startfrom: float, startto: float, page: float, perpage: float, sort: str, asc: bool) -> List[Any]:
		"""		Get a list of auctions based on their start time
		Args:
			startfrom (float):start from
			startto (float):start to
			page (float):
			perpage (float):number of auctions per page
			sort (str):field to sort by
			asc (bool):ascending (true) or descending (false)
		Returns:
			List of auctions starting in the specified period
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [startfrom, startto, page, perpage, sort, asc]
		ret = None
		def GetAuctionsStarting_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('EnglishAuction.GetAuctionsStarting', args, GetAuctionsStarting_Ret)
		return ret

	def GetOpenAuctions(self, page: float, perpage: float, sort: str, asc: bool) -> List[Any]:
		"""		Get a list of currently running auctions
		Args:
			page (float):
			perpage (float):number of auctions per page
			sort (str):field to sort by
			asc (bool):ascending (true) or descending (false)
		Returns:
			List of open auctions
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [page, perpage, sort, asc]
		ret = None
		def GetOpenAuctions_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('EnglishAuction.GetOpenAuctions', args, GetOpenAuctions_Ret)
		return ret



