# Sets default options for a host.
def defaultOptions():
    # These are the only guaranteed options for a host
    return {
            'auth_method': 'password',
            'username': 'root',
            'key': None,
            'password': None,
            'port': 22
        }
# Valid YAML exerpt
# hosts:
#   - ns1:
#       auth_method: PSK
#       username: kindlehl
#       auth_secret: my password
#   - ns2:

def createHostsFromYaml(yaml):
    hosts = []
    for host_object in yaml['hosts']:
        if type(host_object) is str:
            hostname = host_object
            host_object = {hostname: None}
        else:
            hostname = list(host_object.keys())[0]

        if host_object[hostname] is None:
            hosts.append(Host(hostname, defaultOptions()))
        else:
            # Put all things like auth_method, auth_user in a variable called options on the host object
            options = defaultOptions()
            options.update(host_object[hostname])
            hosts.append(Host(hostname, options))
    return hosts

class Host:
    def __init__(self, hostname, yaml=defaultOptions()):
       self.hostname = hostname
       self.options = yaml

    def __str__(self):
        return "%s@%s" % (self.options['username'], self.hostname)

    def __repl__(self):
        return str(self)
 
    def __getitem__(self, index):
        return self.options[index]

    def __setitem__(self, index, val):
        self.options[index] = val
