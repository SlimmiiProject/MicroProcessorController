def WifiSelector(*networks):
    return """<select name="ssid" id="ssid">
        {OPTIONS}
    </select>""".format(OPTIONS="\n".join(["<option value=\"{value}\">{value}</option>".format(value=i) for i in networks]))