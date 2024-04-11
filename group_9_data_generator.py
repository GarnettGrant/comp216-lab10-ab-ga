import random


class DataGenerator:
    '''
    # Data Generator Class
    ###### Created by Abdoullahi Isse & Garnett Grant
    ## Description:
    This class will generate random values in a given range. \n
    Transformation is then applied to the random values in the generator to fit the desired range

    ## Parameters:
    xmin: Lower Boundary
    xmax: Upper Boundary
    n: Number of values to generate

    ## Methods:
    generator: Private method that will generate random values in range 0-1
    transformer: Public property that will use the generator method to return a value in the preferred range (xmin, xmax)
    plot: public method which handles the plotting of the graph
    '''

    def __init__(self, xmin, xmax, n, method='Uniform'):

        ## Lower Boundary
        '''
        xmin: Lower Boundary
        xmax: Upper Boundary
        n: Number of values to generate
        '''
        self.xmin = xmin
        ## Upper Boundary
        self.xmax = xmax
        ## Number of values to generate
        self.n = n

    ## Create a private method that will generate random values in range 0-1, this method may take an argument that can be passed by a property
    def __generator(self, method='uniform', arg=1.0):
        '''
        This generator gives you a uniform random number in a 0-1 range
        Using the Method defined by the user. Default is Uniform in Range 0-1
        arg: Upper Boundary(When Methodis : Uniform/Constant) or Delta(When Method is: Gaussian)
        '''
        if str(method).lower() == 'uniform':
            return random.uniform(0.0, arg)
        elif str(method).lower() == 'constant':
            # return [i / self.n for i in range(self.n)]
            return [pow(i / self.n, 2) for i in range(self.n)]
        elif str(method).lower() == 'gaussian':
            return random.gauss(0.0, arg)
        else:
            return random.uniform(0.0, 1)

    ## create a public property that will use the above member to return a value in your preferred range
    @property
    def transformer(self):
        '''
        This method will transform the random value to fit the desired range
        Returns the transformed value (y) and the original value (x)
        '''
        # User-defined preferred range [xmax - xmin]
        m = (self.xmax - self.xmin)

        # C is the minimum value, adding it shifts the graph up by C
        c = self.xmin

        # list_x is the returned value (output of the method _generator() when using the parameter("constant"))
        list_x = self.__generator("constant")  # returns a list of normalized values between 0 and 1
        # print(f"x: {list_x}")

        # y = mx + c, the required linear transformation
        y = [(m * x) + c for x in list_x]
        return y

    def plot(self):
        '''
        This method will add noise to the transformed data, and then plot it to a graph.
        Nuber of Values to plot is specified by self.n
        '''

        y = []
        x = []
        transformed_y = self.transformer  # list of y values transformed from a range of 0 - 1, transformed to range
        # (x-min, x-max)

        y = [abs(self.__generator("gaussian", i * 0.035)) + self.__generator("uniform") * 5 + i for i in
             transformed_y]  # y used for plotting
        x = [i * 135.0 / self.n + 1880 for i in
             range(self.n)]  # x used for plotting, determines the numbers on the x axis
        #
        # plt.figure("Water Levels Figure", figsize=(12, 4))
        # plt.plot(x, y, 'r')
        # plt.bar(x, y, 100 / self.n)
        # # plt.plot(x, y, 'r.')
        # # plt.fill_between(x, y)
        # plt.xlabel('Time, in years')
        # plt.ylabel('Rise in global sea levels, in millimeters')
        # plt.title('Global rise in sea levels since 1880')
        # plt.show()
        return x, y
