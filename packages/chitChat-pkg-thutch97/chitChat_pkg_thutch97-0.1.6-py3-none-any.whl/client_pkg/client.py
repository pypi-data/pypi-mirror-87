import requests

# print("Please input the address for your server.")
# BASE = "http://" + input("http://")
BASE = 'http://127.0.0.1:5000/' # The endpoint of the API

''' Functions '''
def register():
	# Give username
	username = input('Please provide a username. ')
	if username == 'back': return False # To go back to previous layer

	# Give display name
	display_name = input('Please provide a display name. ')
	if display_name == 'back': return False # To go back to previous layer

	# Give password
	while True:
		password1 = input('Please provide a password. ')
		if password1 == 'back':
			return False # To go back to previous layer
		password2 = input('Please repeat the password. ')
		if password2 == 'back':
			return False # To go back to previous layer
		if password1 == password2:
			password = password1
			break
		else:
			print('Sorry, the passwords do not match, please try again.')

	# Giving friends names
	print('If applicable, please provide usernames for friends who already use chitChat.')
	print("Leave empty if you don't have any friends. ;(")
	response = input('Please leave a space between each username. ')
	if response == 'back':
		return False
	names = response.split()

	# Check friends exist in the database
	checked_names = []
	for friend_name in names:
		if requests.get(BASE + "user_info", {"username": friend_name}).json() != {
			'None': 'There is no user by this username.'
		}:
			checked_names.append(friend_name)
		else:
			print(f"The username {friend_name} does not exist.")

	# Create new friends' names string
	friends = " ".join(checked_names)

	# Make the register API call
	args = {
		"username": username,
		"password": password,
		"display_name": display_name,
		"friends": friends
	}
	result = requests.post(BASE + "register", args).json()

	''' If username taken, try again. If not, login '''
	if 'user_added' in result:
		print('')
		return True

	else:
		print('Sorry, this username is taken, please try a different username.')


def login():
	username = input('Please provide a username. ')
	if username == 'back': return ['back', None] # This will allow the login/register screen to reset

	password = input('Please provide a password. ')
	if password == 'back': return ['back', None] # This will allow the login/register screen to reset

	''' Creating arguments for register API call '''
	argKeys = ['username', 'password']
	argValues = [username, password]
	args = dict(zip(argKeys, argValues))

	''' Making the API call '''
	response = requests.get(BASE + "login", args)
	result = response.json()

	''' Respond appropriately '''
	if result == {'success': 'Passwords match.'}:
		return [True, username]

	elif result == {'error': 'Passwords do not match.'}:
		print('Sorry, your password is incorrect, please try again.')

	elif result == {'error': 'This user does not exist.'}:
		print('Sorry, this user does not exist, please try another username.')


def border(message, where='topAndBottom', border='-'):
	
	length = len(message)

	if where == 'top':
		print(length * border)
		print(message)

	elif where == 'bottom':
		print(message)
		print(length * border)

	else:
		print(length * border)
		print(message)
		print(length * border)
	

def home(username):

	# Find conversations via API call
	response = requests.get(BASE + "home", {'username': username})
	result = response.json()

	# If no conversations
	if 'None' in result:
		to_print = ["You don't have any conversations, why don't you start a new one?", '']
		return [None, to_print]

	else:
		to_print, chat_poss = [], []
		for convo in result:
			# Present each conversation nicely
			friend_display_name, friend_user_name = result[convo][0], convo
			chat_poss.append([friend_display_name, friend_user_name])
			message = result[convo][1][:35]
			space_size = 15-len(friend_display_name)
			spaces = " " * space_size
			print_format = f"{friend_display_name}{spaces}{message}"

			# Print in correct order
			time_sent = result[convo][-1]
			if not to_print:
				to_print.append([print_format, time_sent])
			else:
				added = False
				for index, item in enumerate(to_print):
					if time_sent > item[1]:
						to_print.insert(index, [print_format, time_sent])
						added = True
						break
				if not added:
					to_print.append([print_format, time_sent])

		to_print = [x[0] for x in to_print]
		to_print.insert(0, "")
		to_print.insert(0, "Here are your ongoing conversations.")

		return [chat_poss, to_print]


def chat_name(username, display_name, friend_username, friend_display_name):
	''' API call to get chat messages '''
	response = requests.get(BASE + "chat_name", {'username':username, 'friend':friend_username})
	result = response.json()

	convo = result['conversation']

	# Present nicely
	border('Here is your conversation with {}'.format(friend_display_name))
	to_return = []
	for message in convo:
		sender, content = message[0], message[1]
		display_sender = display_name if sender == username else friend_display_name
		to_print = f"{display_sender}>> {content}"
		print(to_print)
		to_return.append(to_print)
	print('')

	return to_return


def chat_new(username, friend_name):

	''' Create new conversation using API call '''
	requests.post(BASE + "chat_new", {'username':username, 'friend_name': friend_name})

	''' API call to find display name for friend '''
	response = requests.get(BASE + "user_info", {'username': friend_name})
	result = response.json()
	friend_display_name = result['User_info'][0]
	return friend_display_name


def find_new_chat_friend(username, still_finding_friend, found_friend, new_convo):
	"""
	Once a client decides they want to chat with someone new, this function sets up the conversation for them.
	"""

	# Ask for friend's name
	print('')
	maybe_friend = input('Please give the name for a friend you would like to chat to. ')
	print('')

	if maybe_friend == 'back':
		still_finding_friend = False
	else:
		# Find user details for given input
		api_result = requests.get(BASE + "user_info", {"display_name": maybe_friend}).json()

		if "None" in api_result:
			print('You do not have a friend by that display name, please try a different username.')
			print('')

		else:
			# There exists at least one user by that display name
			# See if user/s are client's friend/s
			maybe_friend_usernames = [x[0] for x in list(api_result.values())[0]]
			user_info = requests.get(BASE + "user_info", {'username': username}).json()
			friends = user_info["User_info"][1]
			poss_friends = []
			for maybe_friend_username in maybe_friend_usernames:
				if maybe_friend_username in friends:
					poss_friends.append(maybe_friend_username)

			# If there is only one possible friend the client might want to chat with,
			# create new conversation and jump into it
			if len(poss_friends) == 1:
				friend_username = maybe_friend_username
				friend_display_name = maybe_friend
				chat_new(username, friend_username)
				still_finding_friend, found_friend, new_convo = False, True, True

			# If there are several friends by the same display name
			elif len(poss_friends) > 1:
				# Keep client in loop till they enter a valid response
				while True:
					print("Which of the following people would you like to chat with?")
					for poss_friend in poss_friends:
						print(poss_friend)
					print('')
					chat_new_friend = input("")

					# If user inputs 'back'
					if chat_new_friend == "back":
						break

					# If they do not choose a valid option
					elif chat_new_friend not in poss_friends:
						print("Sorry that is not one of the options, please try again.")
						continue

					else:
						friend_username = chat_new_friend
						friend_display_name = maybe_friend
						chat_new(username, friend_username)
						still_finding_friend, found_friend, new_convo = False, True, True
						break

	if "friend_username" not in locals():
		friend_username = None
	if "friend_display_name" not in locals():
		friend_display_name = None

	return [still_finding_friend, found_friend, new_convo, friend_username, friend_display_name]


def main():
	"""
	Defines the client's interaction with the server.
	"""
	border('Welcome to chitChat!')

	while True: # Layer 1 - login/register/leave
		logged_in = False
		print('Would you like to login, register or leave? ')
		print("(Type 'back' to return to previous stage at any time)")
		print('')
		response = input('')
		print('') # Line space

		# Handling response
		if response == 'leave': break

		elif response != 'leave' and response != 'login' and response != 'register':
			print('Please choose from the following options.')
			print('')
			continue

		if response == 'register':
			still_registering, registered = True, False
			# Keep users in loop while trying to register
			while still_registering:
				register_value = register()
				if register_value is not None:
					if register_value is False:
						# If user pressed 'back', they restart process
						still_registering = False
						print('')
					# User successfully registers
					else:
						still_registering, registered = False, True
				# If user entered incorrect values
				else:
					print('')

			if not registered: continue

		# Logging in
		still_logging_in, logged_in = True, False
		while still_logging_in: # Keep users in loop while trying to register
			try:
				success, username = login()
				if [success, username] == ['back', None]:
					still_logging_in = False
					print('')
				# User successfully logs in
				else:
					still_logging_in, logged_in = False, True
			# If user entered incorrect values
			except:
				pass
		if not logged_in:
			continue

		# Find display name to greet user with
		user_info = requests.get(BASE + "user_info", {'username': username}).json()
		display_name = user_info["User_info"][0]
		border(f"Welcome {display_name}, you are now logged in!")
		# border('Welcome {}, you are now logged in!'.format(username))

		new_convo = False
		while True: # Layer 2 - Home screen (view conversations)

			chatPoss, toPrint = home(username)
			for line in toPrint:
				print(line)
			# If user has ongoing conversations
			if chatPoss:
				display_names = [poss[0] for poss in chatPoss]
				usernames = [poss[1] for poss in chatPoss]
			else:
				display_names = []

			print('')
			print("Chat with a friend in your conversations list by typing their display name,")
			print("start a new chat by typing 'new'")
			print("check for new messages with 'refresh'")
			print("or log-out of chat server by typing 'log-out'")
			print('')
			response = input('')

			if response == 'log-out':
				print('')
				# Take users back to login/registration
				break

			elif response == 'refresh':
				print('')
				continue

			elif response not in display_names and response != 'new':
				print('Please choose from the following options.')
				print('')
				continue

			elif response == 'new':
				still_finding_friend, found_friend = True, False
				# Keep asking for input until user inputs valid name
				while still_finding_friend == True:
					# Find new friend and start new chat
					returns = find_new_chat_friend(username, still_finding_friend, found_friend, new_convo)
					still_finding_friend, found_friend, new_convo, friend_username, friend_display_name = returns

				if not found_friend: continue # Sends user back to home screen
				# if found_friend == True: response = friend_display_name # Create variable response so that it can be used in chat_name

			# Start conversation
			# If friend_username exists, then new conversation started, jump into that
			# (Only for when first created though)
			if "friend_username" in locals() and "new_convo" in locals() and friend_username and new_convo:
				chat_name(username, display_name, friend_username, friend_display_name)
				new_convo = False
				print('')

			# If opening existing conversation
			else:
				friend_display_name = response
				occurrences = display_names.count(friend_display_name)
				# If display name only appears once in client's conversations
				if occurrences == 1:
					index = display_names.index(friend_display_name)
					friend_username = usernames[index]
					chat_name(username, display_name, friend_username, friend_display_name)

				# If display name appears multiple times in client's conversations
				else:
					# Make user choose who they want to start conversation with
					# Find possible people they might want to choose
					poss_friends, displays_copy, users_copy = [], display_names, usernames
					for i in range(occurrences):
						index = displays_copy.index(friend_display_name)
						friend_username = users_copy[index]
						poss_friends.append(friend_username)
						displays_copy = displays_copy[:index]+displays_copy[index+1:]
						users_copy = users_copy[:index] + users_copy[index + 1:]

					# Have users choose someone to chat with
					while True:
						print('')
						print("Which of the following people would you like to chat with?")
						for poss_friend in poss_friends:
							print(poss_friend)
						print('')
						chat_friend = input("")

						# If user inputs 'back'
						if chat_friend == "back":
							break

						# If they do not choose a valid option
						elif chat_friend not in poss_friends:
							print("Sorry that is not one of the options, please try again.")
							continue

						else:
							friend_username = chat_friend
							chat_name(username, display_name, friend_username, friend_display_name)
							break

			while True: # Layer 3 - Sending messages
				# Check for commands
				message = input('>> ')
				if message == 'back':
					print('')
					break # Send user back to home screen

				if message == 'refresh':
					chat_name(username, display_name, friend_username, friend_display_name)
					print('')
					continue

				# Send message
				requests.post(BASE + "send", {'username': username, 'friend_name': friend_username, 'message': message})
				chat_name(username, display_name, friend_username, friend_display_name)
				print('')


if __name__ == "__main__":
	main()