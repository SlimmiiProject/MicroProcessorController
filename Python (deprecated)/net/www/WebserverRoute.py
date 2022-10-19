class WebserverRoute:
    routes = []

    @staticmethod
    def __register(method, route, callback):
        """
            Push a new request handler to the routes stack.
        """
        WebserverRoute.routes.append((method, route, callback));

    @staticmethod
    def __parseRouteFromArgs(*args, **kwargs):
        """
            Route parser for request method registrar attributes
        """
        # Controleer of een naamloze parameter is meegeven en deze een string is of een named parameter route is gevonden met een string waarde.
        assert (len(args) == 1 and isinstance(args[0], str)) \
            or ("route" in kwargs.keys() and isinstance(kwargs["route"], str))
        
        # Stel correcte parameter in op route variabele
        return kwargs["route"] if "route" in kwargs.keys() else args[0]
    
    
    @staticmethod
    def get(*args, **kwargs):
        """
            GET route register attribute
        """
        route = WebserverRoute.__parseRouteFromArgs(*args, **kwargs)
        # Push de route op de routes stack en geef de originele functie terug (deze word enkel called op initializeren attribute )
        def targetFuncParser(func):
            WebserverRoute.__register("GET", route, func)
            return func
        
        return targetFuncParser 

    @staticmethod
    def post(*args, **kwargs):
        """
            POST route register attribute
        """
        route = WebserverRoute.__parseRouteFromArgs(*args, **kwargs)
        # Push de route op de routes stack en geef de originele functie terug (deze word enkel called op initializeren attribute )
        def targetFuncParser(func):
            WebserverRoute.__register("POST", route, func)
            return func
        
        return targetFuncParser 

    @staticmethod
    def fetch(targetMethod, targetRoute):
        """
            Fetch a HTTP request parser
        """
        for method, route, callback in WebserverRoute.routes:
            if method == targetMethod and route == targetRoute:
                return callback
        
        return False
    
    @staticmethod
    def fetchRoute(targetMethod, targetRoute):
        """
            Fetch a HTTP request parser
        """
        for method, route, callback in WebserverRoute.routes:
            print((method, route, callback))
            if method == targetMethod and route == targetRoute:
            
                return callback
        
        return False

