# RECIPE PROGRAM
# Description: the recipe program helps users to store the recipes and books of recipe.
# Also, users can have access and manipulate the data if necessary

# import files
from time import sleep
import sqlite3, os

# initialize the database of recipes
conn = sqlite3.connect( "recipe.db" )
c = conn.cursor()

c.execute("PRAGMA foreign_keys = ON;")

# create table of data base
c.execute( """CREATE TABLE IF NOT EXISTS recipes
             (id int NOT NULL,
              title text NOT NULL,
              servings int NOT NULL DEFAULT 2,
              calories int,
              chef text,
              recipe_book text,
              CONSTRAINT RECIPEFK
              	FOREIGN KEY( recipe_book, chef ) REFERENCES
              		recipeBooks( name, chef )
              		ON DELETE SET NULL
              		ON UPDATE CASCADE,
              PRIMARY KEY( id, title ))""" )

# create table of database recipe books
c.execute( """CREATE TABLE IF NOT EXISTS recipeBooks
				(recipe_id int NOT NULL DEFAULT 1,
				 name text NOT NULL,
				 chef text NOT NULL,
				 data_of_books text,
				 cover_image text,
				 UNIQUE( name ),
				 PRIMARY KEY( name, chef ))""" )

# create table of database chef
c.execute( """CREATE TABLE IF NOT EXISTS chef
			  ( name text PRIMARY KEY NOT NULL,
			  	book text,
			  	CONSTRAINT CHEFFK
			  		FOREIGN KEY( book ) REFERENCES
			  			recipeBooks( name )
			  			ON DELETE SET NULL
			  			ON UPDATE CASCADE
			  )""" )

# main function to process the user's choice
def main_driver_recipes( user_selection ):
	# check for user wants to show all recipes
	if user_selection == 1:
		# call function to show all recipes
		show_all_recipes()

	# check for users wants to find recipes
	if user_selection == 2:
		# call function to find the recipe
		find_recipe()

	# check for users want to insert new recipe
	elif user_selection == 3:
		# call function to insert new recipe
		insert_recipe()

	# check for users want to update the recipe
	elif user_selection == 4:
		# call function to update recipe
		update_recipe()

	# check for users want to delete the recipe
	elif user_selection == 5:
		# call function to delete recipe
		delete_recipe()

def main_driver_recBook( user_selection ):
	# check for user wants to show all recipes
	if user_selection == 1:
		# call function to show all recipes
		show_all_books_ordered_by_id()

	# check for users wants to find recipes
	if user_selection == 2:
		# call function to find the recipe
		find_book()

	# check for users want to insert new recipe
	elif user_selection == 3:
		# call function to insert new recipe
		insert_book()

	# check for users want to delete the recipe
	elif user_selection == 4:
		# call function to delete recipe
		delete_book()

# function to display title of program
def display_title():
	# print out the title line
	print( "\n\n***WELCOME TO RECIPE STORAGE PROGRAM***\n" )

# function to display main menu
def display_main_menu():
	#print out the main menu lines
	print( "\nChoose category to access:\n" )
	print( "\t1. Recipe\n" )
	print( "\t2. Recipe books\n" )
	print( "\t3. Exit the program" )

# function to display recipe-book menu
def display_menu_recipe_book():
	# print out the recipe-book menu
	print( "\n   Menu:\n" )
	print( "\t1. Show all books\n" )
	print( "\t2. Find the book\n" )
	print( "\t3. Insert new book\n" )
	print( "\t4. Delete the book\n" )
	print( "\t5. Exit\n" )

# function to display recipe-book menu when storing no data
def display_menu_recBook_no_records():
	# print out the recipe-book menu
	print( "\n   Menu:\n" )
	print( "\t1. Show all books   (NOT AVAILABLE)\n" )
	print( "\t2. Find the book    (NOT AVAILABLE)\n" )
	print( "\t3. Insert new book\n" )
	print( "\t4. Delete the book  (NOT AVAILABLE)\n" )
	print( "\t5. Exit\n" )

# function to display the delete book menu
def display_delete_book_menu():
	# print out the delete-book menu
	print( "\n**Delete the book**" )
	print( "\nList the category to find:\n" )
	print( "\t1. Title" )
	print( "\t2. All of books" )
	print( "\t3. Exit to main menu" )

# function to display recipe menu
def display_menu_recipes():
	# print out the recipe menu
	print( "\n   Menu:\n" )
	print( "\t1. Show all recipes\n" )
	print( "\t2. Find the recipe\n" )
	print( "\t3. Insert new recipe\n" )
	print( "\t4. Update the recipe\n" )
	print( "\t5. Delete the recipe\n" )
	print( "\t6. Exit\n" )

# function to display recipe menu when storing no data
def display_menu_recipes_no_records():
	# print out the recipe menu
	print( "\n   Menu:\n" )
	print( "\t1. Show all recipes   (NOT AVAILABLE)\n" )
	print( "\t2. Find the recipe    (NOT AVAILABLE)\n" )
	print( "\t3. Insert new recipe\n" )
	print( "\t4. Update the recipe  (NOT AVAILABLE)\n" )
	print( "\t5. Delete the recipe  (NOT AVAILABLE)\n" )
	print( "\t6. Exit\n" )

# function to show recipes menu
def display_show_recipe_menu():
	# print out the show-recipes menu
	print( "\n**Show all recipes**\n" )
	print( "\tChoose the category to sort:\n" )
	print( "\t1. ID" )
	print( "\t2. Title" )
	print( "\t3. Servings" )
	print( "\t4. Calories" )
	print( "\t5. Exit to main menu" )

# function to display delete-recipe menu
def display_delete_recipe_menu():
	# print out the delete-recipe menu
	print( "\n**Delete the recipe**" )
	print( "\nList the category to delete:\n" )
	print( "\t1. ID" )
	print( "\t2. Title" )
	print( "\t3. Servings" )
	print( "\t4. All of recipes" )
	print( "\t5. Exit to main menu" )

# function to display find-recipe menu
def display_find_recipe_menu():
	# print out find-recipe menu
	print( "\nFind the recipe\n" )
	print( "\nChoose the category to find:\n" )
	print( "\t1. Title" )
	print( "\t2. Servings" )
	print( "\t3. Calories" )
	print( "\t4. Exit to main menu" )

# function to display find-book menu
def display_find_book_menu():
	# print out the find-book menu
	print( "\n**Find the book**\n" )
	print( "\nChoose the category to find:\n" )
	print( "\t1. Title" )
	print( "\t2. Exit to main menu" )

# function to process user selection
def recBook_process_selection():
	# initialize variables
	running_flag = True

	# main while loop to run the program
	while running_flag:
		# select all data from book of recipes database
			# function: execute
		c.execute( "SELECT * FROM recipeBooks" )

		# change datatype to list and assigned to variable
			# function: fetchall
		books = c.fetchall()

		# check for no data
		if len( books ) == 0:
			# call function to display menu
			display_menu_recBook_no_records()

		# otherwise, there are data in storage
		else:
			# call function to display menu
			display_menu_recipe_book()

		# get user's input
		user_selection = int( input( "Select the option (1, 2, 3, 4 or 5): " ) )

		# check for valid input
		if user_selection in [1, 2, 3, 4]:
			# call function to process user's input
			main_driver_recBook( user_selection )

		# check for exit choice
		elif user_selection == 5:
			# set running flag false
			running_flag = False

			# print out the exit message
			print( "\n***EXIT RECIPE BOOK PROGRAM***\n" )

		# otherwise, invalid input
		else:
			# print out the invalid message
			print( "\n!!!Your selection is invalid!!!\n" )
			print( "   Please select the option again\n" )

	# return user's input
	return user_selection

# function to process user's input in  recipe program
def recipe_process_selection():
	# initialize variables
	running_flag = True

	# main loop to run the process
	while running_flag:

		# select all data from book of recipes database
			# function: execute
		c.execute( "SELECT * FROM recipes" )

		# change datatype to list and assigned to variable
			# function: fetchall
		recipes = c.fetchall()

		# check for no data
		if len(recipes) == 0:
			# call function display recipe menu with no data
			display_menu_recipes_no_records()

		# otherwise, having data
		else:
			# call function to display recipe menu with data
			display_menu_recipes()

		# get user's input
		user_selection = int( input( "Select the option (1, 2, 3, 4, 5 or 6): " ) )

		# check for valid input
		if user_selection in [1, 2, 3, 4, 5]:
			# call function to process user's input
			main_driver_recipes( user_selection )

		# check for exit choice
		elif user_selection == 6:
			# set running flag false
			running_flag = False

			# print out exit message
			print( "\n***EXIT RECIPE PROGRAM***\n" )

		# otherwise, invalid input
		else:
			# print out invalid message
			print( "\n!!!Your selection is invalid!!!\n" )
			print( "   Please select the option again   \n" )

	# return user's input
	return user_selection

# function to show all the recipes
def show_all_recipes():
	# initialize variables
	exit_choice = 5

	# call function to display menu
	display_show_recipe_menu()
	# get user's input
	user_selection = int( input( "\nPlease enter number to choose: " ) )

	# main loop to process
	while user_selection != exit_choice:
		# check for invalid input
		if user_selection > 5 or user_selection < 1:
			# print out invalid message
			print( "\n!!!Your selection is invalid!!!\n" )
			print( "   Please select the option again\n" )
		
		# otherwise, valid input
		else:
			# check for first selection
			if user_selection == 1:
				# call function to order by id
				show_all_recipes_ordered_by_id()

			# check for second selection
			elif user_selection == 2:
				# call function to order by title
				show_all_recipes_ordered_by_title()

			# check for third selection
			elif user_selection == 3:
				# call function to order by servings
				show_all_recipes_ordered_by_servings()

			# check for fourth selection
			elif user_selection == 4:
				# call function to order by calories
				show_all_recipes_ordered_by_calories()

		# call function to display menu
		display_show_recipe_menu()

		# get user's input
		user_selection = int( input( "\nPlease enter number to choose: " ) )

	# print out the exit message
	print( "\n**EXIT TO MAIN MENU**\n" )

# function to show all recipes by calories
def show_all_recipes_ordered_by_calories():
	c.execute( "SELECT * FROM recipes ORDER BY calories" )
	items = c.fetchall()

	if len( items ) == 0 :
		print( "\n!!NO RECIPES FOUND!!\n" )
	else:
		print( "\n>>RECIPES:\n" )
		for item in items:
			print( f"\tID: {item[0]}; Title: {item[1]}; Servings: {item[2]}; Calories: {item[3]}", end="\n\n" )

	sleep(1)
	return items

# function to show all recipes by servings
def show_all_recipes_ordered_by_servings():
	c.execute( "SELECT * FROM recipes ORDER BY servings" )
	items = c.fetchall()

	if len( items ) == 0 :
		print( "\n!!NO RECIPES FOUND!!\n" )
	else:
		print( "\n>>RECIPES:\n" )
		for item in items:
			print( f"\tID: {item[0]}; Title: {item[1]}; Servings: {item[2]}; Calories: {item[3]}", end="\n\n" )

	sleep(1)
	return items

# function to show all recipes by title
def show_all_recipes_ordered_by_title():
	c.execute( "SELECT * FROM recipes ORDER BY title" )
	items = c.fetchall()

	if len( items ) == 0 :
		print( "\n!!NO RECIPES FOUND!!\n" )
	else:
		print( "\n>>RECIPES:\n" )
		for item in items:
			print( f"\tID: {item[0]}; Title: {item[1]}; Servings: {item[2]}; Calories: {item[3]}", end="\n\n" )

	sleep(1)
	return items

# function to show all recipes by id
def show_all_recipes_ordered_by_id():
	c.execute( "SELECT * FROM recipes ORDER BY id" )
	items = c.fetchall()

	if len( items ) == 0 :
		print( "\n!!NO RECIPES FOUND!!\n" )
	else:
		print( "\n>>RECIPES:\n" )
		for item in items:
			print( f"\tID: {item[0]}; Title: {item[1]}; Servings: {item[2]}; Calories: {item[3]}", end="\n\n" )

	sleep(1)
	return items

# function to show all books by id
def show_all_books_ordered_by_id():
	c.execute( "SELECT * FROM recipeBooks ORDER BY name" )
	items = c.fetchall()

	if len( items ) == 0 :
		print( "\n!!NO RECIPES FOUND!!\n" )
	else:
		print( "\n>>RECIPES:\n" )
		for item in items:
			print( f"\tName: {item[1]}; ID recipe: {item[0]}; Chef: {item[2]}; number of chapters: {item[3]}", end="\n\n" )
	sleep(1)
	return items

# function to delete recipe
def delete_recipe():
	display_delete_recipe_menu()
	user_selection = int( input( "\nChoose the category to delete: " ) )

	show_all_recipes_ordered_by_id()

	while user_selection != 5:
		if user_selection == 2:
			delete_title = input( "\nEnter the title to delete (press ENTER to cancel): " )
			with conn:
				c.execute( """DELETE from recipes WHERE title = :title""", { 'title': delete_title } )
		elif user_selection == 3:
			delete_servings = int( input( "\nEnter the servings to delete (press ENTER to cancel): " ) )
			with conn:
				c.execute( """DELETE from recipes WHERE servings = :servings""", { 'servings': delete_servings } )
		elif user_selection == 4:
			with conn:
				c.execute( """DELETE from recipes""" )
		elif user_selection == 1:
			delete_id = input( "\nEnter the id to delete (press ENTER to cancel): " )
			with conn:
				c.execute( """DELETE from recipes WHERE id = :id""", { 'id': delete_id } )

		if user_selection != 5:
			print( "\n**SUCCESSFUL DELETE RECIPE**\n" )

		display_delete_recipe_menu()

		user_selection = int( input( "\nChoose the category to delete: " ) )

	print( "\n**EXIT TO MAIN MENU**\n" )

# function delete book
	# function: DELETE from...WHERE
def delete_book():
	display_delete_book_menu()
	user_selection = int( input( "\nPlease enter number to choose: " ) )

	show_all_books_ordered_by_id()

	while user_selection != 3:
		if user_selection == 1:
			deleted_title = input( "\nPlease enter the name to delete (if not press ENTER): " )

			if len( deleted_title ) != 0:
				with conn:
					c.execute( """DELETE from recipeBooks WHERE name = :title""", { 'title': deleted_title } )
		else:
			with conn:
				c.execute( """DELETE from recipes""" )

		print( "\n**SUCCESSFUL DELETE RECIPE**\n" )

		display_delete_book_menu()

		user_selection = int( input( "\nPlease enter number to choose: " ) )

	print( "\n**EXIT TO MAIN MENU**\n" )

# function to update recipe
	# function: execute, UPDATE..SET..WHERE
def update_recipe():
	input_running = True

	c.execute( "SELECT * FROM recipes" )
	results = c.fetchall()

	show_all_recipes_ordered_by_id()
	
	if( len( results ) == 0 ):
		print( "\n!!UNSUCCESSFUL UPDATE RECIPE!!\n" )
	else:
		search_id = int( input( "\nEnter the id to search: " ) )

		for recipe in results:
			if recipe[ 0 ] == search_id:
				print( f"\n\tID: {recipe[0]}; Title: {recipe[1]}; Servings: {recipe[2]}; Calories: {recipe[3]}", end="\n\n" )

		new_title = input( "\nEnter new value for title (if not press ENTER): " )
		new_servings = input( "\nEnter new number for servings (if not press ENTER): " )
		new_calories = input( "\nEnter new number for calories (if not press ENTER): " )
		
		if len( new_title ) != 0 and len( new_servings ) != 0 and len( new_calories ) != 0:
			with conn:
				c.execute( """UPDATE recipes SET title = :title, servings = :servings, calories = :calories WHERE id = :id""",
				{ 'title': new_title, 'servings': new_servings, 'calories': new_calories, 'id': search_id } )

		elif len( new_title ) != 0 and len( new_servings ) != 0:
			with conn:
				c.execute( """UPDATE recipes SET title = :title, servings = :servings WHERE id = :id""",
				{ 'title': new_title, 'servings': new_servings, 'id': search_id } )

		elif len( new_title ) != 0 and len( new_calories ) != 0:
			with conn:
				c.execute( """UPDATE recipes SET title = :title, calories = :calories WHERE id = :id""",
				{ 'title': new_title, 'calories': new_calories, 'id': search_id } )

		elif len( new_servings ) != 0 and len( new_calories ) != 0:
			with conn:
				c.execute( """UPDATE recipes SET servings = :servings, calories = :calories WHERE id = :id""",
				{ 'servings': new_servings, 'calories': new_calories, 'id': search_id } )

		elif len( new_title ) != 0:
			with conn:
				c.execute( """UPDATE recipes SET title = :title WHERE id = :id""",
				{ 'title': new_title, 'id': search_id } )

		elif len( new_servings ) != 0:
			with conn:
				c.execute( """UPDATE recipes SET servings = :servings WHERE id = :id""",
				{ 'servings': new_servings, 'id': search_id } )

		elif len( new_calories ) != 0:
			with conn:
				c.execute( """UPDATE recipes SET calories = :calories WHERE id = :id""",
				{ 'calories': new_calories, 'id': search_id } )

		print( "\n**SUCCESSFUL UPDATE RECIPE**\n" )

# function to find recipe
	# function: SELECT...FROM...WHERE, LIKE operator
def find_recipe():
	exit_choice = 4

	display_find_recipe_menu()
	user_selection = int( input( "\nSelect the number: " ) )

	while user_selection != exit_choice:
		if user_selection == 1:
			input_title = input( "\tType the title to find: " )
			c.execute( "SELECT title, servings, calories FROM recipes WHERE title LIKE ? ", ('%' + input_title + '%', ) )
		elif user_selection == 2:
			input_servings = input( "\tType the servings to find: " )
			c.execute( "SELECT title, servings, calories FROM recipes WHERE servings = ?", (input_servings, ) )
		elif user_selection == 3:
			input_calories = input( "\tType the calories to find: " )
			requirement = input( "\tFind the recipes with (TYPE 'greater' or 'less') calories: " )

			if requirement == "greater":
				c.execute( "SELECT title, servings, calories FROM recipes WHERE calories >= ?", (input_calories, ) )
			else:
				c.execute( "SELECT title, servings, calories FROM recipes WHERE calories <= ?", (input_calories, ) )
		else:
			print( "\nWrong input\n" )

		results = c.fetchall()

		if( len( results ) == 0 ):
			print( "\n**NO RESULTS**\n" )
		else:
			print( "\n**RECIPES RESULTS:**\n" )
			for recipe in results:
				print( f"\tTitle: {recipe[0]}; Servings: {recipe[1]}; Calories: {recipe[2]}", end="\n" )
			print( "\n" )

		display_find_recipe_menu()
		user_selection = int( input( "\nSelect the number: " ) )

# function to find book
	# function: SELECT...FROM...WHERE, LIKE operator
def find_book():
	exit_choice = 2

	display_find_book_menu()
	user_selection = int( input( "\nSelect the number: " ) )

	while user_selection != exit_choice:
		if user_selection == 1:
			input_title = input( "\tType the title to find: " )
			c.execute( "SELECT name, chef FROM recipeBooks WHERE name LIKE ? ", ('%' + input_title + '%', ) )
		else:
			print( "\nWrong input\n" )

		sleep( 1 )

		results = c.fetchall()

		if( len( results ) == 0 ):
			print( "\n>>NO RESULTS\n" )
		else:
			print( "\n>>BOOKS:\n" )
			for recipe in results:
				print( f"\tTitle: {recipe[0]}; Chef(author): {recipe[1]}", end="\n" )
			print( "\n" )

		sleep( 1 )

		display_find_book_menu()
		user_selection = int( input( "\nSelect the number: " ) )

# function to insert book
	# function: INSERT INTO...VALUES
def insert_book():
	print( "\n**Insert new book:**\n" )

	recipe_id = int( input( "\tPlease enter id of recipe: " ) )
	name_book = input( "\tPlease enter name of book: " )
	chef_book = input( "\tPlease enter chef(author) of book: " )
	numOfChapters_book = input( "\tPlease enter number of chapters: " )
	numOfPages_book = input( "\tPlease enter number of pages: " )
	coverImage_book = input( "\tPlease enter file's name of cover image with '.img' tail: " )

	while len( coverImage_book ) <= 4 or coverImage_book[-4:] != ".img":
		print( "\n\t!!!Your input for cover image is invalid!!!\n" )
		coverImage_book = input( "\tPlease enter file's name of cover image with '.img' tail: " )

	with conn:
		c.execute( "INSERT INTO recipeBooks VALUES (?, ?, ?, ?, ?)", ( recipe_id, name_book, chef_book, numOfChapters_book + " " + numOfPages_book, coverImage_book ) )

	print( f"\n**SUCCESSFULLY INSERT NEW BOOK**\n" )

# function to insert recipe
	# function: INSERT INTO...VALUES
def insert_recipe():
	print( "\nInsert new recipe:\n" )

	show_all_recipes_ordered_by_id()

	print( "\n**Insert new recipe**\n" )

	id_recipe = int( input( "\tPlease enter id of recipe: " ) )
	title_recipe = input( "\tPlease enter title of recipe: " )
	servings_recipe = int( input( "\tPlease enter servings of recipe: " ) )
	calories_recipe = int( input( "\tPlease enter calories of recipe: " ) )

	with conn:
		c.execute( "INSERT INTO recipes (id, title, servings, calories) VALUES (?, ?, ?, ?)", ( id_recipe, title_recipe, servings_recipe, calories_recipe ) )

	print( f"\n**SUCCESSFULLY INSERT NEW RECIPE**\n" )

# main function
def main():
	# initialize variables
	exit_choice = 3

	# call function to display title and menu
	display_title()
	display_main_menu()

	# get user's input
	user_selection = int( input( "\nPlease enter the number to choose: " ) )

	# main loop
	while user_selection != exit_choice:
		# check for recipe access
		if user_selection == 1:
			# call function to process recipe menu
			recipe_process_selection()

		# check for book of recipes access
		elif user_selection == 2:
			# call function to process book of recipes
			recBook_process_selection()

		# call function to display menu
		display_main_menu()

		# get user's input
		user_selection = int( input( "\nPlease enter the number to choose: " ) )

	# check for exit choice
	if user_selection == exit_choice:
		# print out exit message
		print( "\n***EXIT PROGRAM***\n" )

if __name__ == "__main__":
	# call main function to run
	main()

	# commint changes to database
	conn.commit()

	# close the database
	conn.close()
