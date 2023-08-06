from ..variables.Variable import Variable


class Type:
    def __init__(self, type_id, name, description, vars):
        """
        Class storing Time Series type data

        Parameters
        ----------
        type_id : List [ str ]
                  The type ID, containing a maximum of 3 strings.
        name : str
               The name of the instance type.
        description : str
                      The description for the instance type.
        vars : List [ Variable ]
               The list of variables defined for the type.
        """
        self.type_id = type_id
        self.name = name
        self.description = description
        self.__vars = {v.name: v for v in vars} if vars is not None else None
        self.vars = vars

    def __getitem__(self, var_name):
        """
        Get the variable with the given name

        Parameters
        ----------
        var_name : str
                   The name of the variable that should be returned

        Returns
        -------
        Variable : The requested variable
        """
        return self.__vars[var_name]

    def __getattr__(self, var_name):
        """
        Get the variable with the given name

        Parameters
        ----------
        var_name : str
                   The name of the variable that should be returned

        Returns
        -------
        Variable : The requested variable
        """
        try:
            return self.__vars[var_name]
        except KeyError:
            raise AttributeError(f'Attribute {var_name} not defined for type {self.name}')

    def __repr__(self):
        return f'<Time Series Type {self.name} with ID {self.type_id}>'
