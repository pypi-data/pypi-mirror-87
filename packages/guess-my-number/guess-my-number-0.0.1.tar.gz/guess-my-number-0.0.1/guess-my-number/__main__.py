import random

n = random.randint(0,100)
p=1

while True:
	try:
		c = int(input('Guess my number (less than 100)!\n>>> '))
		if n<c:
			print('My number is lower than that!')
			p+=1
		if n>c:
			print('My number is higher than that!')
			p+=1
		if n==c:
			print('Great job! You guessed it in {} tries, my number is {}!'.format(p,c))
			if input('Type `go` to play again!') == 'go':
				n = random.randint(0,100)
				print('---------------')
			else:
				exit()
	except ValueError:
		print('Please say a number!')
	except KeyboardInterrupt:
		if input('End game? [y/n]')[0] == 'y':
			exit()
