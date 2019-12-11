from copy import deepcopy
import math
import numpy as np


class StatError(Exception):
    """ Raised if something is wrong with the evaluation.
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Stat:
    """ The base class for all evaluations. Really just provides the essentials.
        This class should never be instanciated on its own.
    """
    def __str__(self):
        results = self.evaluateVariables()
        text = ""
        for key in results:
            text += key + ":\t\t" + str(results[key]) + ""
        return text

    def __add__(self, other):
        """ Allows us to add two ScalarStat objects. Only is valid, if all
            variables are the same.
        """
        # Checks, to see if the operation is valid.
        if not isinstance(other, self.__class__):
            raise StatError("Impossible to add " + str(other.__class__) + " and " + str(self.__class__) + " objects.")
        cLen = len(set(self.variables.keys() + other.variables.keys()))
        if not (cLen == len(self.variables) and cLen == len(other.variables)):
            raise StatError("Lists of variables are not equal.")

        # Copy the self object to a third one, such that the initial objects
        # remain untouched.
        result = deepcopy(self)
        for variable in other.variables:
            mu, var, n = other.variables[variable]
            result.combineSets(variable, mu, var, n)
        return result

    def __getitem__(self, key):
        """    Makes it possible to retrieve an evaluated variable by its name. The
            key can *not* be a list, since this is really meant to be a way to
            retrieve single quantities.
        """
        return self.evaluateVariables(key)[key]

    def deleteVariable(self, variable):
        """ Removes a scalar variable and returns the removed entry.
        """
        return self.variables.pop(variable)

    def setVariable(self, variable, mu, var, n):
        """ Sets a scalar variable to specified values. Can also be used to
            initialize.
        """
        self.addVariable(variable, mu, var, n)

    def resetVariable(self, variable):
        """    Resets a variable.
        """
        n = len(self.deleteVariable(variable)[0])
        self.addVariable([variable, n])

    def addValue(self, variable, mu, var=0., n=1):
        """ Updates the average, variance and number of values of the specified
            scalar variable with the provided value.
            Online calculation of the variable with WELFORD'S METHOD.
        """
        muOld, varOld, nOld = self.variables[variable]
        self.variables[variable][0] = (muOld*nOld + mu*n) / (nOld + n)
        self.variables[variable][2] += n
        self.variables[variable][1] = varOld + var + nOld*muOld**2 + n*mu**2 - (nOld*muOld + n*mu)**2 / (n + nOld)

    def evaluateVariables(self, variables=None):
        """ Returns the statistics of all specified observables in an
            ordered fashion.
        """
        if variables is None:
            realVariables = self.variables
        else:
            if isinstance(variables, str):
                variables = [variables]
            realVariables = variables

        evalTable = dict()
        for variable in realVariables:
            try:
                evalTable[variable] = [self.variables[variable][0], self._sqrt(self.variables[variable][1] / (self.variables[variable][2] - 1)), self.variables[variable][2]]
            except ZeroDivisionError:
                evalTable[variable] = [self.variables[variable][0], self._zero(variable), 0., self.variables[variable][2]]
        return evalTable

    
    
class ScalarStat(Stat):
    """    Container that provides an easy handling and statistical evaluation of 
        scalar variables. Stat objects can conveniently be added, merging two
        distinct datasets on the fly.
    """
    def __init__(self, variables=None):
        """ Initializes from an array of String objects. If no array is passed 
            an empty dictionary is created.
        """
        if variables is not None:
            if isinstance(variables, str):
                variables = [variables]
            self.variables = {variables[i] : [0., 0., 0] for i in range(0, len(variables))}
        else:
            self.variables = dict()
            
    def _zero(self, variable):
        return 0.
        
    def _sqrt(self, x):
        return math.sqrt(x)

    def addVariable(self, variable, mu=0., var=0., n=0):
        """ Adds a scalar variable and initializes it to the specified values.
        """
        self.variables[variable] = [mu, var, n]

    def combineSets(self, variable, mu, var, n):
        """ Takes mean, variance and number of samples and adds it to the 
            corresponding scalar variable.
        """
        self.addValue(variable, mu, var, n)

    def addList(self, variable, values):
        """ Adds multiple values to a scalar variable.
        """
        for value in values:
            self.addValue(variable, value)
            


class VectorStat(Stat):
    """    Container that provides an easy handling and statistical evaluation of 
        vector variables. Stat objects can conveniently be added, merging two
        distinct datasets on the fly.
    """
    def __init__(self, variables=None):
        """ Initializes from an array of String objects. If no array is passed 
            an empty dictionary is created.
        """
        if variables is not None:
            if isinstance(variables[0], str):
                variables = [variables]
            self.variables = {variables[i][0] : [np.zeros(variables[i][1]), np.zeros(variables[i][1]), 0] for i in range(0, len(variables))}
        else:
            self.variables = dict()
        
    def _zero(self, variable):
        return np.zeros(len(self.variables[variable][0]))
        
    def _sqrt(self, x):
        return np.sqrt(x)
        
    def addVariable(self, variable, mu=None, var=None, n=0):
        """ Adds a vector variable and initializes it to the specified values. 
            The length of the vector needs to be specified like
            
                addVariable(["key", length])
                
            Its possible to pass any iterable with a strucure (i.e. no sets).
        """
        if mu is None:
            mu = np.zeros(variable[1])
            var = np.zeros(variable[1])
        self.variables[variable[0]] = [mu, var, n]
        
    def combineSets(self, vector, mu, var, n):
        """ Takes mean, variance and number of samples and adds it to the 
            corresponding vector variable.
        """
        if len(mu) != len(self.variables[vector][0]):
            raise StatError("Cannot combine vectors with different lengths.")
        else:
            self.addValue(vector, mu, var, n)
    
    def addList(self, variable, vectors):
        """ Adds multiple values to a vector variable.
         """
        for vector in vectors:
            if len(vector) != self.variables[vector][0]:
                raise StatError("Cannot combine vectors with different lengths.")
            else:
                 self.addValue(variable, vector)
