from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page

def index(request):
	# query the database for a list of all the categories currently stored.
	# order the categories by no. likes in decending order.
	# retrieve  the top 5 only - or all if less than 5.
	# place the list in our context_dict dictionary
	# that will be passed to the template engine.

	category_list = Category.objects.order_by('-likes')[:5]

	page_list = Page.objects.order_by('-views')[:5]

	context_dict = {
					'categories': category_list,
					'pages': page_list,
					}

	# render the respone and send it back
	return render(request, 'rango/index.html', context_dict)

def about(request):
    return render(request, 'rango/about.html')

def show_category(request, category_name_slug):
	#create a context dictionary which we can passs
	# to the template rendering engine.
	context_dict = {}

	try:
 		# can we find a category name slug with the given name?
		# if we can't, the .get() method raises a DoesNotExist exception.
		category = Category.objects.get(slug=category_name_slug)
		# retrive all of the associated pages.
		# note that filter() will return a list of page objects or an empty list
		pages = Page.objects.filter(category=category)
		# adds our results list to the template context under name pages.
		context_dict['pages'] = pages
		# we also add the category object from the database to the context dictionary
		# we will use this in the template to verify that the category exists
		context_dict['category'] = category 
	except Category.DoesNotExist:
		# we get her if we didn't find the specified category
		# don't do anything - the template will display the "no category message for us"
		context_dict['category'] = None
		context_dict['pages'] = None

		# go render the respone and return it to the client
	return render(request, 'rango/category.html', context_dict)	