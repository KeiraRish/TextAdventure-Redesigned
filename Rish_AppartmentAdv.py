import os, sys, random, time

HEALTH_BAR = 50
BACKPACK = []
temp_outside = random.randint(20, 81)

#############Functions

### Happiness tracker function
def HEALTH(HEALTH_BAR, num):
	HEALTH_BAR += num
	if HEALTH_BAR < 1:
		os.system('clear')
		print('GAME OVER')
		print('Happiness went below 0')
		sys.exit()
	print('Happiness is currently at', HEALTH_BAR)
	return HEALTH_BAR
	
### Getting out of bed and making bed function
def BED(HEALTH_BAR):
	while 1==1:
		print("Options are 'Get up' or 'Stay in bed'")
		user_input = input('> ')
		if user_input == 'Get up':
			break
		elif user_input == 'Stay in bed':
			print()
			print('How lazy of you. Your happiness decreases -10')
			HEALTH_BAR = HEALTH(HEALTH_BAR, -10)
		else:
			print()
			print('Not a valid input')
	print()
	print('Yay! Goodmorning! Time to start your day')
	print()
	print('You turn around and take a look at your messy bed, would you like to make it?')
	while True:
		user_input = input("Type 'yes' or 'no' > ")
		if user_input == 'yes':
			print()
			print('Now your bed is so nice and pretty! Seeing this increases your happiness +10')
			HEALTH_BAR = HEALTH(HEALTH_BAR, 10)
			break
		elif user_input == 'no':
			print()
			print('How lazy of you. Your happiness decreses -10 points')
			HEALTH_BAR = HEALTH(HEALTH_BAR, -10)
			break
		else:
			print('Not a valid input')
			
	return HEALTH_BAR

## CLoset function that has the user pick out an outfit
def CLOSET(HEALTH_BAR, temp_outside):
	points = 0
	print()
	print('Today it will be', temp_outside, 'degrees outside, be sure to choose your outfit to fit the weather.')
	print()
	print('If it is below 60 degrees you should be wearing long pants and a long sleeve.')
	print('If it is below 35 degrees you should be wearing a coat.')
	print('Your happiness will decrease if you are not properly dressed for the weather outside.')

	## Determine if pants fit the weather outside
	print()
	print('Lets start with what bottoms to wear')
	while 1==1:
		print("Options are 'Sweatpants', 'Leggings', or 'Shorts'")
		user_input_pants = input('> ')
		if ((user_input_pants == 'Sweatpants') or (user_input_pants == 'Leggings')):
			if temp_outside < 60:
				print()
				print("Good choice! You'll be nice and warm. Happiness increases +5")
				HEALTH_BAR = HEALTH(HEALTH_BAR, 5)
			else:
				print()
				print("Bad choice, you'll be too warm! Happiness decreases -15")
				HEALTH_BAR = HEALTH(HEALTH_BAR, -15)
			break
		elif user_input_pants == 'Shorts':
			if temp_outside < 60:
				print()
				print("Bad choice, you'll freeze! Happiness decreses -15")
				HEALTH_BAR = HEALTH(HEALTH_BAR, -15)
			else:
				print()
				print("Good choice! You'll be nice and comfortable. Happiness increases +5")
				HEALTH_BAR = HEALTH(HEALTH_BAR, 5)
			break
		else:
			print()
			print('Not a valid input')
	
	## Determine if top fits the weather outside
	print()
	print('Now lets pick what top to wear')
	while 1==1:
		print("Options are 'Sweatshirt', 'Long sleeve', T-shirt', or 'Tank top'")
		user_input_top = input('> ')
		if (user_input_top == 'Sweatshirt') or (user_input_top == 'Long sleeve'):
			if temp_outside < 60:
				print()
				print("Good choice! You'll be nice and warm. Happiness increases +5")
				HEALTH_BAR = HEALTH(HEALTH_BAR, 5)
			else:
				print()
				print("Bad choice, you'll be too warm! Happiness decreases -15")
				HEALTH_BAR = HEALTH(HEALTH_BAR, -15)
			break
		elif (user_input_top == 'T-shirt') or (user_input_top == 'Tank top'):
			if temp_outside < 60:
				print()
				print("Bad choice, you'll freeze! Happiness decreases -15")
				HEALTH_BAR = HEALTH(HEALTH_BAR, -15)
			else:
				print()
				print("Good choice! You'll be nice and comfortable. Happiness increases +5")
				HEALTH_BAR = HEALTH(HEALTH_BAR, 5)
			break
		else:
			print()
			print('Not a valid input')
		
	## If user wants to wear a coat outside
	print()
	print('Since it is', temp_outside, 'degrees outside, would you like to wear a coat?')
	while 1==1:
		user_input = input("Type 'yes' or 'no' > ")
		if user_input == 'yes':
			if temp_outside < 35:
				print()
				print("Good choice, you'd be cold without one. Happiness increases +5")
				HEALTH_BAR = HEALTH(HEALTH_BAR, 5)
			else:
				print()
				print("Bad choice, you'll be way to warm. Happiness decreases -15")
				HEALTH_BAR = HEALTH(HEALTH_BAR, -15)
			break
		elif user_input == 'no':
			if temp_outside < 35:
				print()
				print("Bad choice, you'll freeze! Happiness decreases -15")
				HEALTH_BAR = HEALTH(HEALTH_BAR, -15)
			else:
				print()
				print("Good choice, you didn't need one anyways. Happiness increases +5")
				HEALTH_BAR = HEALTH(HEALTH_BAR, 5)
			break
		else:
			print('Not a valid input')
	return HEALTH_BAR



### If the user wants to do their hair or makeup 
def MAKEUP_HAIR(HEALTH_BAR, to_do):
	if to_do == 'Makeup':
		print()
		print('You put on a little bit of mascara as well as some lip gloss, you feel pretty and your happiness increases +10')
		HEALTH_BAR = HEALTH(HEALTH_BAR, 10)
	elif to_do == 'Hair':
		print()
		print('What would you like to do with your hair?')
		while 1==1:
			print("Options are 'Leave down', 'Claw clip', 'Ponytail'")
			user_input_hair = input('> ')
			if user_input_hair == 'Leave down':
				print()
				print('Your hair looks so pretty down, your happpiness increases +10')
				HEALTH_BAR = HEALTH(HEALTH_BAR, 10)
				break
			elif user_input_hair == 'Claw clip':
				print()
				print('Somehow it looks good on the first try, and your happiness increases +10')
				HEALTH_BAR = HEALTH(HEALTH_BAR, 10)
				break
			elif user_input_hair == 'Ponytail':
				print()
				print('Somehow your ponytail looks good on the first try, and your happiness increases +10')
				HEALTH_BAR = HEALTH(HEALTH_BAR, 10)
				break
			else:
				print('Not a valid input')
	return HEALTH_BAR


### This function is how the user makes their breakfast
def FOOD(HEALTH_BAR):
	Fridge = ['Eggs', 'Butter', 'Milk', 'Water']
	Pantry = ['Pancake mix', 'Oatmeal pack']
	ingredients = []
	print()
	print("You have three recipies to choose from: 'Scrambled eggs', 'Pancakes', or 'Oatmeal'")
	while 1==1: ## what ingredients you'll need for the recipe chosen
		user_input_recipe = input('> ')
		food = user_input_recipe
		if user_input_recipe == 'Scrambled eggs':
			print()
			print("You'll need: Eggs, butter, and milk")
			break
		elif user_input_recipe == 'Pancakes':
			print()
			print("You'll need: Pancake mix, water, and butter")
			break
		elif user_input_recipe == 'Oatmeal':
			print()
			print("You'll need: Oatmeal pack and water/milk")
			break
		else:
			print('Not one of the recipies.')
	
	print()
	print("Now that you know what you want to make, it's time to gather ingredients!")
	while 1==1: ## User decides if they want to go to the fridge or pantry and ends when they type 'Done'
		print()
		print("Where would you like to go? Options are 'Fridge' or 'Pantry'")
		print("Type 'Done' once you have all ingredients from both Fridge and Pantry")
		user_input = input('> ')
		if user_input == 'Done':
			break
		elif user_input == 'Fridge':
			print()
			while True: ## Only allows user to grab items that are permitted by recipe chosen
				print('Items in fridge: ', ', '.join(Fridge))
				print("Which items would you like to grab? Type 'Done' when you have all of them")
				fridge_grab = input('> ')
				if fridge_grab == 'Done':
					break
				elif food == 'Scrambled eggs':
					if (fridge_grab == 'Eggs') or (fridge_grab == 'Butter') or (fridge_grab == 'Milk'):
						print()
						print('Ingredient grabbed!')
						Fridge.remove(fridge_grab)
						ingredients.append(fridge_grab)
					elif (fridge_grab == 'Water'):
						print()
						print("You don't need this item for this recipe")
					else:
						print('Not an item in the fridge')		 
				elif food == 'Pancakes':
					if (fridge_grab == 'Water') or (fridge_grab == 'Butter'):
						print()
						print('Ingredient grabbed!')
						Fridge.remove(fridge_grab)
						ingredients.append(fridge_grab)
					elif (fridge_grab == 'Milk') or (fridge_grab == 'Eggs'):
						print()
						print("You don't need this item for this recipe")
					else:
						print('Not an item in the fridge')

				elif food == 'Oatmeal':
					if (fridge_grab == 'Milk') or (fridge_grab == 'Water'):
						print()
						print('Ingredient grabbed!')
						Fridge.remove(fridge_grab)
						ingredients.append(fridge_grab)
					elif (fridge_grab == 'Eggs') or (fridge_grab == 'Butter'):
						print()
						print("You don't need this item for this recipe")
					else:
						print('Not an item in the fridge')
		elif user_input == 'Pantry':
			print()
			while True: #same as the fridge loop above but for the pantry
				print('Items in the pantry: ', ', '.join(Pantry))
				print("Which items would you like to grab? Type 'Done' when you have all of them")
				pantry_grab = input('> ')
				if pantry_grab == 'Done':
					break
				elif food == 'Scrambled eggs':
					print()
					print("All ingredients for scrambled eggs are in the fridge")
				elif food == 'Pancakes':
					if (pantry_grab == 'Pancake mix'):
						print()
						print('Ingredient grabbed!')
						Pantry.remove(pantry_grab)
						ingredients.append(pantry_grab)
					elif (pantry_grab == 'Oatmeal pack'):
						print()
						print("You don't need this item for this recipe")
					else:
						print('Not an item in the pantry')
				elif food == 'Oatmeal':
					if pantry_grab == 'Oatmeal pack':
						print()
						print('Ingredient grabbed!')
						Pantry.remove(pantry_grab)
						ingredients.append(pantry_grab)
					elif pantry_grab == 'Pancake mix':
						print()
						print("You don't need this item for this recipe")
					else:
						print('Not an item in the pantry')	
		else:
			print('Not a valid input')

	print()	
	print("Now that you have all the ingredients, it's time to cook your food")
	print("Type 'Cook' to finish your breakfast")
	cook_input = input('> ')
	while 1==1:
		if cook_input == 'Cook':
			if food == 'Pancakes': ## if the user makes pancakes they get to see this yay
				os.system('clear')
				print('⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀⡀⠀                          ⠀')
				print('⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠤⠲⢉⡽⢈⣠⡞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ')
				print('⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠎⢀⠄⢢⠫⡀⠸⣇⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀')
				print('⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠃⡠⠃⠀⡇⠀⠱⠀⠀⠀⠉⠒⠤⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀')
				print('⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⠤⠋⢀⠇⠀⠀⠱⡀⠀⠑⢄⠀⠈⠐⠒⠤⡀⠑⢦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀')
				print('⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⣜⣻⣿⠿⠃⠠⠜⠃⠀⠀⠀⠀⠘⢄⡀⠀⠛⠤⠀⠀⠀⠘⡄⣸⣧⣘⡠⠤⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀')
				print('⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⢤⢲⠽⣿⣿⡿⠁⡄⠀⠀⠀⢀⠡⢄⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⢈⣿⣿⣿⣿⣿⣶⣬⣑⡠⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀')
				print('⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢤⠲⣍⡾⢣⢋⡕⣊⠿⡇⠀⣧⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⣿⣿⣿⣿⣿⣷⣦⣑⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀')
				print('⠀⠀⠀⠀⠀⠀⠀⢠⢊⢧⣋⢛⣥⣲⣥⣮⣴⣵⣾⣧⠀⢣⠱⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣮⣂⠄⡀⠀⠀⠀⠀⠀⠀')
				print('⠀⠀⠀⠀⠀⠀⢠⢧⣛⣴⣾⣿⡿⣿⣿⢿⣿⡿⣿⣿⣷⣄⣀⠈⠢⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣬⢦⠀⠀⠀⠀⠀')
				print('⠀⠀⠀⠀⠀⠀⢸⠘⣿⣿⣯⣷⣿⢿⣾⡿⣟⣿⣟⣯⣿⣿⣿⣿⣶⣶⣶⣤⣤⣀⣀⡀⠀⠀⠀⠀⢀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢾⠀⠀⠀⠀⠀')
				print('⠀⠀⠀⠀⠀⢀⡼⣆⢹⣿⣿⢷⣿⣻⣯⠿⣛⠫⠭⡍⡭⢭⣙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⡇⠀⠀⠀⠀⠀')
				print('⠀⠀⠀⠀⣰⣍⣶⠛⣄⠙⠻⢿⡛⠍⣆⠳⢌⢣⠓⣬⠱⢦⡩⢝⡲⣌⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⢁⡔⢠⠇⠀⠀⠀⠀⠀')
				print('⠀⠀⠀⠀⡟⣷⢣⠘⡄⣓⢄⡀⠉⠳⢬⣚⣌⡲⣉⠦⣋⢖⡩⢎⡵⢊⠷⣡⢿⣿⣿⣯⣿⣿⣿⡿⣿⣿⡿⣿⢿⡿⣿⢿⡿⣿⢿⣿⡿⠿⠛⠁⠀⠀⡎⣀⠎⠀⠀⠀⠀⠀⠀')
				print('⠀⠀⠀⠀⢧⠸⣇⠎⡰⢌⢊⡙⠲⣄⡀⠀⠈⠉⠉⠛⠚⠒⠛⠚⠒⠛⠓⠓⠚⢿⡿⣿⣿⣿⣿⣿⣏⣷⣹⡮⠷⠽⠾⠗⠛⠋⠉⠀⠀⠀⠀⠀⢀⣠⣿⠟⡆⠀⠀⠀⠀⠀⠀')
				print('⠀⠀⠀⠀⢸⠀⠙⢆⡱⣈⠦⣉⠳⢄⢫⠱⠦⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡽⣖⡳⣞⢶⣳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣠⣴⣶⢿⡿⠋⠀⡆⠀⠀⠀⠀⠀⠀')
				print('⠀⠀⠀⠀⠘⡆⠀⡀⠑⢦⡒⠥⡚⣌⠲⣉⠞⣰⠪⡝⢭⡓⢶⡒⣖⠲⣖⢲⢖⡺⣿⣷⣿⣾⣷⣿⣿⣤⣤⣤⣤⣤⢶⣶⢻⡟⡿⢯⡿⣽⣳⣯⠟⠁⡔⡀⡇⠀⠀⠀⠀⠀⠀')
				print('⠀⠀⠀⠀⠀⠙⣤⡈⠀⠀⠉⠓⠵⣌⡓⡌⡎⢥⡓⡜⡣⢞⡡⢏⡜⡳⢬⣋⢮⣕⢫⣝⣻⣛⢿⡹⢧⡳⣞⢶⡹⣎⠿⣜⣻⣼⣛⣯⢷⣯⠗⠋⢠⠞⡴⡯⣅⠀⠀⠀⠀⠀⠀')
				print('⠀⠀⠀⢀⠄⠊⢡⣿⣶⣄⠀⠀⠀⠈⠉⠓⠺⢥⣎⡵⣙⢬⠳⣩⢞⡱⢫⡜⡖⢮⣓⠾⣔⢯⣚⡽⣣⢟⡼⣣⡟⣭⠿⣭⣳⣞⡽⠞⠋⠁⠀⠀⣸⠾⡳⢦⡄⠱⢠⠀⠀⠀⠀')
				print('⠀⢀⡔⠁⠀⠀⣿⣿⢯⣟⣷⣦⣄⣀⠀⠀⠀⠀⠀⠈⠉⠉⠓⠓⠚⠓⠓⠛⠞⢣⣿⢾⡿⣾⢷⡿⣿⢿⡿⣿⢿⡿⣿⡿⠉⠁⠀⠀⢀⣠⠖⣫⠡⢒⡉⠳⣽⡀⠀⠑⢀⠀⠀')
				print('⢠⠏⢠⠎⠀⠸⡿⣿⣿⣞⣷⡻⡾⣽⣻⢶⣦⢤⣤⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠘⠻⠷⠿⠾⠷⢯⣽⢾⡽⠛⠋⠛⠋⢁⣀⡤⢴⡚⡍⢆⡓⠤⢃⠥⢨⣱⠏⠀⠈⢢⠈⢣⠀')
				print('⠛⢨⡇⠀⠀⠀⢣⠉⢻⣾⢳⣿⣽⢳⣽⡞⣵⢻⡜⢳⣯⣽⠛⣿⠛⡟⢻⢳⡞⣶⣶⡖⣶⠒⣶⠒⣿⣿⢲⠒⣶⠛⣭⠋⣦⢱⢢⢱⠘⣦⠘⠑⠊⡜⣶⠃⡆⠀⠀⠀⠃⠐⡆')
				print('⣻⠙⡄⠀⠀⠀⠈⠣⡄⠈⠙⠺⢷⣯⣗⣻⡭⣷⢻⡝⣮⢳⡻⣜⢯⡝⣧⢻⠼⣱⢎⡵⢣⣛⣴⣻⣼⣿⣿⣜⣦⣷⣼⣾⣾⣦⢉⡆⢳⡈⢖⣩⠶⠋⠀⢠⠃⠀⠀⠀⡘⠀⡇')
				print('⠸⣤⠐⡄⠀⠀⠀⠀⠈⢦⣑⠠⠀⡀⠈⠉⠛⠺⠷⣯⣳⣏⡷⣹⢮⡝⣮⠽⣭⠳⢮⣙⠧⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⡶⡬⠗⠚⢉⠀⠀⣀⠔⠁⠀⠀⠀⡰⠁⣸⠁')
				print('⠀⠈⢆⠈⠢⡀⠀⠀⠀⠀⠀⠉⠒⠦⢄⣀⠒⠠⠄⠀⠀⠈⠉⠉⠛⠚⠓⠻⠶⠯⠷⠭⠾⠥⠯⠯⠿⠿⣷⠟⠛⠛⠉⣉⣥⣴⣶⣾⣿⣿⣿⣿⠋⠀⠀⠀⠀⣀⠔⠀⡰⠁⠀')
				print('⠀⠀⠀⠑⢤⠈⠒⠄⡀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠒⠒⠦⠤⠤⣀⣀⣀⣀⡀⠀⠀⢀⣤⣤⣤⣤⣤⣤⣴⢿⣶⣶⡾⣿⠿⣟⣻⢻⣽⣹⠾⠋⠁⠀⠀⢀⠤⠊⢀⡴⠋⠀⠀⠀')
				print('⠀⠀⠀⠀⠀⠈⠒⢄⡈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠘⢥⣈⣆⣑⣪⣑⣎⣭⣓⣬⠷⠼⠿⠚⠋⠉⠀⠀⠀⠀⠀⠀⠈⣀⠤⠚⠉⠀⠀⠀⠀⠀')
				print('⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠒⠠⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡠⠔⠚⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀')
				print('⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠑⠐⠢⠤⠤⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣤⠤⠦⠶⠒⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀')
				print('⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠁⠉⠈⠁⠉⠈⠁⠈⠁⠁⠈⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀')

				print('Yay! You eat your delicious breakfast, your happiness increases +20')
				HEALTH_BAR = HEALTH(HEALTH_BAR, 20)
			else:
				print()
				print("Yay! You eat your delicious breakfast, your happiness increases +20")
				HEALTH_BAR = HEALTH(HEALTH_BAR, 20)
			break
		else:
			print('Not a valid input')
	return HEALTH_BAR




## this short function runs the kitchen and allows the user to choose weather or not to make food
def KITCHEN(HEALTH_BAR):
	print()
	print("You walk into your kitchen, and realize how hungry you are. Would you like to make yourself breakfast?")
	print("Type 'yes' or 'no'")
	while 1==1:
		user_input_breakfast = input('> ')
		if user_input_breakfast == 'yes':
			FOOD(HEALTH_BAR)
			break
		elif user_input_breakfast == 'no':
			print("Breakfast is really good for you, you shouldn't skip it. Happiness decreases -20")
			HEALTH_BAR = HEALTH(HEALTH_BAR, -20)
			break
		else:
			print('Not a valid input')
	print()
	print('You go to fill up your water bottle, what do you want to put in it?')
	print("Options are 'Water', 'Mio', or 'Iced Tea'")
	user_input_waterbottle = input('> ')
	print('Yay your water bottle is now filled with', user_input_waterbottle, "hopefully you'll stay hydrated today. Happiness increases +5")
	HEALTH_BAR = HEALTH(HEALTH_BAR, 5)
	return HEALTH_BAR





## short living room function that just allows user to add items to backpack
def LIVINGROOM(HEALTH_BAR):
	print()
	print('You walk into your living room and notice that you forgot to take your ipad and book back into your room last night. Oops.')
	print('Would you like to put them in your backpack?')
	print("Type 'yes' or 'no'")
	while 1==1:
		user_input = input('> ')
		if user_input == 'yes':
			BACKPACK.append('Ipad')
			BACKPACK.append('Book')
			print('Perfect!')
			break
		elif user_input == 'no':
			print('okay?')
			break
		else:
			print('Not a valid input')
	print('Backpack now has:', ', '.join(BACKPACK))
	return HEALTH_BAR













############### Main body of the program that implements the functions above
os.system('clear')
print("Complete all the objectives for each room and leave your appartment to complete the game! Watch out for your Happiness level and make sure it doesn't get to 0")
print()
print("You wake up in your big, comfy bed, perfectly content with staying there all day.")
print(" Unfortunately, it's a school day and you have lots to do.")
print()
print('You really should get out of bed, but what do you want to do?')

HEALTH_BAR = BED(HEALTH_BAR)
print('...')
time.sleep(3)

os.system('clear')
print('You walk over to your closet and decide that the first thing you need to acomplish is picking out an outfit')

temp_health = HEALTH_BAR #Incase the user decides to redo outfit
HEALTH_BAR = CLOSET(HEALTH_BAR, temp_outside)
print()
print("Keeping in mind that you'll lose the game if your Happiness goes to 0, would you like to redo your outfit?")
print("If you choose to do so your Happiness will reset to", temp_health, "- 10 for creating more laundry for yourself")
print('Would you like to redo your outfit?')
while 1==1:
	user_input_redo = input("Type 'yes' or 'no' > ")
	if user_input_redo == 'yes':
		os.system('clear')
		HEALTH_BAR = temp_health - 15
		CLOSET(HEALTH_BAR, temp_outside)
		print('...')
		time.sleep(3)
		os.system('clear')
		break
	elif user_input_redo == 'no':
		os.system('clear')
		break
	else:
		print('Not a valid input')


print('Great! Now that you have your outfit chosen, you walk over to your desk') 
print('It apears that after completing your homework last night, you failed to clean up and re-pack your backpack')
print('Your computer is sitting on your desk(at least you remembered to plug it in) your waterbottle sits nearby and your backpack is rested against the leg of your desk')
print()
print('You still have a bit of time to spare if you want to take a seat at your desk')
print("What would you like to do? Options are 'Hair', 'Makeup', 'Both', or 'Neither'")

while 1==1:
	user_input_makeup_hair = input('> ')
	if user_input_makeup_hair == 'Makeup':
		print()
		print('Moving your computer to the side, you take a seat at your desk')
		HEALTH_BAR = MAKEUP_HAIR(HEALTH_BAR, 'Makeup')
		break
	elif user_input_makeup_hair == 'Hair':
		print()
		print('Moving your computer to the side, you take a seat at your desk')
		HEALTH_BAR = MAKEUP_HAIR(HEALTH_BAR, 'Hair')
		break
	elif user_input_makeup_hair == 'Both':
		print()
		print('Moving your computer to the side, you take a seat at your desk')
		HEALTH_BAR = MAKEUP_HAIR(HEALTH_BAR, 'Makeup')
		HEALTH_BAR = MAKEUP_HAIR(HEALTH_BAR, 'Hair')
		break
	elif user_input_makeup_hair == 'Neither':
		break
	else:
		print('Not a vaild input')


print()
print("You realize you have to repack your backpack")
print('So you pick up your backpack from the floor and place it on your chair so you can put things in it')
print()
print("Some of the items on your desk include 'Computer', 'Lipgloss', 'Computer charger', 'Phone charger', 'Perfume', 'Airpods', 'Waterbottle', 'Clawclip'")
print("What would you like to put in your backpack? Type 'Done' When you are finished")
while 1==1:
	user_input_backpack = input('> ')
	if user_input_backpack == 'Done':
		break
	elif (user_input_backpack == 'Computer') or (user_input_backpack == 'Computer charger') or (user_input_backpack == 'Waterbottle'):
		print()
		print("Good job, you'd problably have a bad day if you forgot that. Happiness increases +10")
		HEALTH_BAR = HEALTH(HEALTH_BAR, 10)
		BACKPACK.append(user_input_backpack)
	elif (user_input_backpack == 'Phone charger') or (user_input_backpack == 'Airpods'):
		print()
		print("Might come in handy, definetley a good thing to pack. Happiness increases +5")
		HEALTH_BAR = HEALTH(HEALTH_BAR, 5)
		BACKPACK.append(user_input_backpack)
	elif (user_input_backpack == 'Lipgloss') or (user_input_backpack == 'Perfume') or (user_input_backpack == 'Clawclip'):
		print()
		print("Sure I guess, though I don't know why you'd need that.")
		BACKPACK.append(user_input_backpack)
	else: 
		print('Not a valid input')

print()
print('Items currently in backpack:', end=' ')
print(', '.join(BACKPACK))

print('You exit your bedroom and walk out into the hall. You can choose to walk into the Kitchen or into the Living room')
print("Where do you want to go? Options are 'Kitchen' or 'Living Room'")
while 1==1:
	user_input_destination = input('> ')
	if user_input_destination == 'Kitchen':
		os.system('clear')	
		KITCHEN(HEALTH_BAR)
		print('...')
		time.sleep(3)
		os.system('clear')
		LIVINGROOM(HEALTH_BAR)
		break
	elif user_input_destination == 'Living Room':
		os.system('clear')
		LIVINGROOM(HEALTH_BAR)
		print('...')
		time.sleep(3)
		os.system('clear')
		KITCHEN(HEALTH_BAR)
		break
	else:
		print('Not a valid input')

print()
print('Now that you are completely ready to take on the day, you run out the door(almost forgeting to grab your car keys on the way out)')
print('Thanks for playing!')
print('Your happiness ended at', HEALTH_BAR)
if HEALTH_BAR > 100:
	print('You did amazing!! Have the best day!')
elif HEALTH_BAR < 100:
	print('You did good! Have a great day!')
elif HEALTH_BAR < 50:
	print('You did okay, do more things that make you happy!')
else:
	print('wow.')
print()
print()
