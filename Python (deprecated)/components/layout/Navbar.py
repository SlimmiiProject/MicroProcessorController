def Navbar(): 
    return """<nav>
        <ul>
            <li onclick="window.location.replace(`/wifi`)">Connect to wifi</li>
            <li onclick="window.location.replace(`/change_adhoc`)">Access point</li>
        </ul>
    </nav>"""