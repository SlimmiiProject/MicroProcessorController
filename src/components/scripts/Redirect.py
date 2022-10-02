def Redirect(target, timeout = 1000):
    return """<script type="text/javascript">
        setTimeout(() => window.location.replace("{target}"), {timeout})
    </script>""".format(target=target, timeout=timeout)