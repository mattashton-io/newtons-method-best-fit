## guess and then adjust by amount, f(x)/f'x

def f(x):
    y = x**2 - x - 1
    return y

tolerance = 0.001
guess = 1
delta = 0.0001
n = 0

while abs(f(guess)) > tolerance:
    slope = (f(guess + delta) - f(guess))/ delta
    if slope == 0:
        slope = (f(guess + 2*delta) - f(guess))/ 2*delta
    guess = guess - f(guess)/slope
    print("guess: " + str(guess))
    print("y: " + str(f(guess)))
    n+=1 
    print("count:" + str(n))

    if n > 100:
        break




## new guess will be subtraction from original x


