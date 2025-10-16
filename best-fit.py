"""
Finds best-fit curve coefficients for (x, y) data by minimizing squared error with Newton's method.
1. Set the `path` variable to your CSV file (must have 'x' and 'y' columns).
2. Define your model (e.g., `c[0]*x + c[1]`) in the `def f(x, c):` function.
3. Set initial coefficient guesses in the `c` list (e.g., `c = [1, 1]` for 2 coefficients).
"""
#import csv library to read in csv files
import csv

# x & y are actual data
x = []
y = []

##VARIABLES THAT MAY BE ALTERED##
delta = 0.000001      # A tiny step size used for numerically calculating derivatives (slopes).
tolerance = 0.000001  # How close to zero the derivative needs to be before stopping; controls the precision of the answer.
limit = 500           # Safety break to prevent the program from running forever.
c = [1,1]             # Initial guesses for the coefficients (e.g., m and b).
path = '/usr/local/google/home/mattashton/Documents/pyTutoring/tyler-sessions/newtons-method/36-over-x.csv' #make file path a variable

# y = mx+b -> line equation
def f(x, c):
    return c[0]/x + c[1] # return mx + b

#read in csv file with data values
with open(path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        x.append(float(row['x']))
        y.append(float(row['y']))

#squaring distances from real values (y_data) to expected
def sq_dist(y_line, y_data):
    return pow(y_data - y_line, 2)

##calculates and populates distance (dist) and derivative (derv) arrays
def calc_dist_derv():
    #define size of matrix
    rows, cols = (len(c), 3)

    #creates dist and derv arrays & populates columns and rows with all zeroes; dist has 3 cols, derv has 2 cols
    dist = [[0 for i in range(cols)] for j in range(rows)]
    derv = [[0 for i in range(2)] for j in range(len(c))]

    ##fill in dist with values in matrix   
    ## I loops through variables m and b 
    for i in range(len(dist)):
        ## j loops through all of the deltas
        for j in range(len(dist[0])):
            ## k loops through each data point
            for k in range(len(x)):
                temp = c.copy()
                temp[i] += j * delta
                dist[i][j]+= sq_dist(f(x[k], temp), y[k])

    #use dist to calculate derv with values in matrix 
    for i in range(len(derv)):
        for j in range(len(derv[0])):
            derv[i][j] = ((dist[i][j+1] - dist[i][j]) / delta)  
    return derv, dist   

#zero-finder function 
#input derv, dist and index
# iteratively calculates new guess 
def find_zeros(derv_pass, dist_pass):
    derv = derv_pass
    dist = dist_pass
    n = 0
    derv_two = [0 for i in range(len(c))]

    while abs(derv[0][0]) > tolerance:
        # i tells us whether we are adjusting m or b
        for i in range(len(derv_two)): #[i] represents the coefficent, as in c[i]
            derv_two[i] = (derv[i][1] - derv[i][0])/ delta

            #safety check so we do not divide by zero
            #check is guess[i] == 0, set up counter for iterative safety check
            counter = 2

            ##while slope is 0
            while derv_two[i] == 0.0:
                print("divide by zero detected. Entering derv_two adjustment loop.")
                print("i: ", i)
                print("derv_two: ", derv_two[i])
                print("counter: ", counter)
                temp = c.copy() ##c is variables m and b; temp is creating an out-of-band copy 
                temp[i] += (counter + 1) * delta #tweak value at temp[i], then calculate derivative 

                #update distances
                for k in range(len(x)): ##range(len(x)) finds the range all of the data points via x-values
                    dist[i][2]+= sq_dist(f(x[k], temp), y[k])

                #update dervs
                derv[i][1] = (dist[i][2] - dist[i][1])/ (counter) * delta

                #update derv_two[i] value
                derv_two[i] = (derv[i][1] - derv[i][0])/ counter * delta

                #update counter
                counter+=1
                print("counter: ", counter)
                
            #updating c-values
            c[i] = c[i] - derv[i][0] /derv_two[i]
            derv, dist = calc_dist_derv()
            
        #safety check so that iterations cap off at limit 
        n+=1 
        if n > limit:
            break
    print("count:" + str(n))
    print("coordinate c-values: ", c)


def app():
    #calc_dist_derv function will return multiple values
    derv, dist = calc_dist_derv()
    #pass derv and dist into find_zeros
    find_zeros(derv, dist)
app()
