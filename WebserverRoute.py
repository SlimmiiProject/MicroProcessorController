

class WebserverRoute:
    routes = []

    @staticmethod
    def __register(method, route, callback):
        """
            Push a new request handler to the routes stack.
        """
        WebserverRoute.routes.append((method, route, callback));
    
    @staticmethod
    def get(*args, **kwargs):
        # Controleer of een naamloze parameter is meegeven en deze een string is of een named parameter route is gevonden met een string waarde.
        assert (len(args) == 1 and isinstance(args[0], str)) \
            or ("route" in kwargs.keys() and isinstance(kwargs["route"], str))
        
        # Stel correcte parameter in op route variabele
        route = kwargs["route"] if "route" in kwargs.keys() else args[0]

        # Push de route op de routes stack en geef de originele functie terug (deze word enkel called op initializeren attribute )
        def targetFuncParser(func):
            WebserverRoute.__register("GET", route, func)
            return func
        
        return targetFuncParser 

    @staticmethod
    def fetch(targetMethod, targetRoute):
        for method, route, callback in WebserverRoute.routes:
            print((method, route, callback))
            print((method == targetMethod, route == targetRoute, callback))
            if method == targetMethod and route == targetRoute:
                return callback
        
        return False

    @staticmethod
    def status_404(params):
        return "Page not found"

    @staticmethod
    def status_503(params):
        return "<b>Server error:</b> {error}".format(error=params["error"])
