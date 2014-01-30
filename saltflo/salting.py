""" salting.py saltstack integration behaviors


"""

#print "module %s" % __name__

from collections import deque

import salt.client.api
from salt.exceptions import EauthAuthenticationError

from ioflo.base.odicting import odict
from ioflo.base.globaling import *

from ioflo.base import aiding
from ioflo.base import storing 
from ioflo.base import deeding

from ioflo.base.consoling import getConsole
console = getConsole()



class SaltDeed(deeding.Deed):
    """ Base class for Deeds that interface with Salt
        Adds salt client interface attribute .client
            
        local attributes
            .client is salt client interface
    
    """
    def __init__(self, **kw):
        """ Initialize instance """
        #call super class method
        super(SaltDeed, self).__init__(**kw)
        
        self.client = salt.client.api.APIClient()    

class EventerSalt(SaltDeed, deeding.SinceDeed):
    """ Salt Eventer
            
        local attributes created by initio
            .inode is inode node
            .event is ref to event share, value is deque of events incoming
            .req is ref to subscription request share, value is deque of
                subscription requests
                each request is duple of tag, share
            .pub is ref to pub share, with tag fields,
                value list of publication to subscriber shares
                each pub share value is deque of events put there by Eventer
            .period is ref to period share
            .parm is ref to node.parm share with fields
                throttle is divisor or period max portion of period to consume each run
    """
    Ioinits = odict(
        period= '.meta.period',
        req=('req', deque()), 
        event=('event', odict(), True),
        pub=('pub', odict(), True), 
        parm=('parm', odict(throttle=0.0, tag='salt/'), True),) 
             
    def action(self, **kw):
        """ Process subscriptions and publications of events
            subscription request are duples (tag prefix, share)
            value is 
        """
        super(EventerSalt, self).action(**kw) #updates .stamp here
        
        #if not self.pub.value: #no pub to subscriptions so request one
            #publication = self.store.create("salt.pub.test").update(value=deque())
            #self.req.value.append(("salt/job/", publication))
        
        #loop to process sub requests
        while self.req.value: # some requests
            tag, share = self.req.value.popleft()
            console.verbose("     Eventer '{0}' subreq tag '{1}' "
                            "share '{2}'\n".format(self.name, tag, share.name))
            if not share: #value not inited to put empty deque()
                share.value = deque()
            if tag in self.pub.value and self.pub.value[tag] != share:
                self.pub.value[tag].append(share)
            else: #first time
                self.pub.value[tag] = [share]
        
        #eventually have realtime check to throttle ratio limit time 
        # in event loop processing events
        period = self.period.value
        throttle = self.parm.data.throttle
        try:
            limit =  period / throttle
        except ZeroDivisionError:
            limit = 0 # no limit
        
        #loop to get and process events from salt client api
        etag = self.parm.data.tag
        while True: #event loop
            edata =  self.client.get_event(wait=0.01, tag=etag, full=True)
            if not edata:
                break
            utag = '/'.join([edata['tag'], edata['data']['_stamp']])
            edata['data']['utag'] = utag
            self.event.value[utag] = edata #pub to odict of all events
            self.event.stampNow() # since modified value in place
            console.verbose("     Eventer '{0}' event tag '{1}'\n".format(self.name, utag))
            # loop to pub event to publications for subscribers
            for tag, shares in self.pub.value.items():
                if edata['tag'].startswith(tag):
                    for share in shares:
                        share.value.append(edata)
                        share.stampNow() # modified in place

        return None

