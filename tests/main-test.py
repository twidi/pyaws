import unittest
import sys

# quick-n-dirty for debug only
sys.path.append('..')
import ecs

class ListTest(unittest.TestCase):
	def setUp(self):
		ecs.setLicenseKey("1MGVS72Y8JF7EC7JDZG2");

	def dump(self, list):
		print "ListId: ", list.ListId
		print "CustomerName: ", list.CustomerName
		print 

	def testListSearch(self):
		lists = ecs.ListSearch(ListType="WishList", City="Chicago", FirstName="Sam")
		self.assert_(len(lists) > 3)
		list = lists[0]
		self.assertNotEqual(list, None)
		# self.dump(list)
		self.assert_(list.CustomerName.find("Sam") > -1)

	def testListLookup(self):
		lists = ecs.ListLookup(ListType="WishList", ListId="13T2CWMCYJI9R")
		self.assertNotEqual(lists, None)
		self.assertEqual(lists[0].CustomerName, "Sam")

class QueryTest(unittest.TestCase):
	def setUp(self):
		ecs.setLicenseKey("1MGVS72Y8JF7EC7JDZG2");

	def dump(self, book):
		try:
			print "ASIN: ", book.ASIN
			print "Title : ", book.Title
			print "Author: ", book.Author
			print "Manufacturer: ", book.Manufacturer
			print 
		except :
			pass

	def testItemLookup(self):
		books = ecs.ItemLookup("0596009259")
		self.assertEqual(len(books), 1)
		book = books[0]
		self.assertNotEqual(book, None)

		self.assertEqual(book.ASIN, u'0596009259')
		self.assertEqual(book.ItemAttributes.Title, u'Programming Python')
		self.assertEqual(book.ItemAttributes.Manufacturer, u"O'Reilly Media")
		self.assertEqual(book.ItemAttributes.ProductGroup, u'Book')
		self.assertEqual(book.ItemAttributes.Author, u'Mark Lutz')


	def testItemSearch(self):
		books = ecs.ItemSearch("python", SearchIndex="Books")
		self.assert_(len(books) > 200, "We are expect more than 200 books are returned.")
		self.assertNotEqual(books[100], None)
	
	def testSimilarityLookup(self):
		books = ecs.SimilarityLookup("0596009259")
		#for book in books:
		#	self.dump(book)
		self.assert_(len(books) > 9, "We are expect more than 9 books are returned.")

class CartTest( unittest.TestCase ):
	def setUp(self):
		# prepare the python books to add 
		ecs.setLicenseKey("1MGVS72Y8JF7EC7JDZG2");
		self.books = ecs.ItemSearch("python", SearchIndex="Books")
		self.cart = None

	def testCartCreate(self):
		items = (self.books[0], self.books[1], self.books[2])
		qs = (1, 3, 5)

		self.cart = ecs.CartCreate(items, qs)
		for i in range(3):
			self.assertEqual(self.books[i].ASIN, self.cart[i].ASIN)
			self.assertEqual(qs[i], int(self.cart[i].Quantity))

	def testCartAdd(self):
		if self.cart == None:
			self.testCartCreate() 

		print self.cart

		l = []
		for x in self.cart:
			z = (int(x.ASIN), int(x.Quantity))
			l.append(z)
			
		items = (self.books[5], self.books[8])
		qs = (5, 8)
		z = (int(self.books[5].ASIN), 5)
		l.append(z)
		z = (int(self.books[8].ASIN), 8)
		l.append(z)

		self.cart = ecs.CartAdd(self.cart, items, qs)

		# check the item
		for item in self.cart:
			self.assert_( (int(item.ASIN), int(item.Quantity)) in l)

	def testCartGet(self):
		if self.cart == None:
			self.testCartCreate() 

		cart = ecs.CartGet(self.cart)
		for i in range(len(cart)):
			self.assertEqual(self.cart[i].ASIN, cart[i].ASIN)
			self.assertEqual(self.cart[i].Quantity, cart[i].Quantity)


if __name__ == "__main__" :
	unittest.main()

