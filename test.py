# -*- coding: utf-8 -*-
import stackless
import functools
from twisted.internet import defer
from twisted.internet import reactor

import time

__author__ = 'viruzzz-kun'


def deferredTasklet(func):
    """
    I'm a function decorator that makes a stacklessy-function (one
    that might 'block', etc) into one that returns a Deferred for
    integrating with Twisted.
    """
    @functools.wraps(func)
    def replacement(*args, **kwargs):
        d = defer.Deferred()

        def tasklet(*args, **kwargs):
            try:
                d.callback(func(*args, **kwargs))
            except:
                d.errback()
            print "deferredTasklet:replacement:tasklet: hey, I just callbacked or errbacked."
        print "deferredTasklet:replacement: task...", func.__name__
        crap = stackless.tasklet(tasklet)(*args, **kwargs)
        crap.run()
        print "deferredTasklet:replacement: ...let", func.__name__, crap
        return d
    return replacement


def blockOn(d):
    """
    Use me in stacklessy-code to wait for a Deferred to fire.
    XXX: If the result is an failure, raise its exception.
    """
    ch = stackless.channel()
    print "blockOn", d
    def cb(r):
        print "blockOn:cb: blockOnCB", r
        ch.send(r)
    d.addBoth(cb)
    return ch.receive()


def TEST():
    """
    Show off deferredTasklet and blockOn.
    """
    #let's make sure we're not blocking anywhere
    def timer():
        print "time!", time.time()
        reactor.callLater(0.5, timer)
    reactor.callLater(0, timer)

    @deferredTasklet
    def getDeferred():
        d = defer.Deferred()
        reactor.callLater(3, d.callback, 'goofledorf')
        print "TEST:getDeferred: blocking on", d
        r = blockOn(d)
        print "TEST:getDeferred: got", r, "from blocking"
        return r

    @deferredTasklet
    def getDeferred2():
        d = defer.Deferred()
        reactor.callLater(2, d.callback, 'yabadaba')
        print "TEST:getDeferred: blocking on", d
        r = blockOn(d)
        print "TEST:getDeferred: got", r, "from blocking"
        return r

    # below is our 'legacy' Twisted code that only knows about
    # Deferreds, not crazy stackless stuff.

    print "TEST: getDeferred is", getDeferred
    print '---------------------------------'
    d = getDeferred()
    print "TEST: d is", d
    print '---------------------------------'
    c = getDeferred2()
    print "TEST: c is", c

    def _cbJunk(r):
        print "TEST:_cbJunk: RESULT", r
        reactor.stop()

    defer.DeferredList([c, d]).addCallback(_cbJunk)
    print "TEST: kicking it off!"
    stackless.schedule()
    print "TEST: rescheduled"
    stackless.schedule()
    print "TEST: rescheduled 2"


if __name__ == '__main__':
    print('main a')
    # stackless.tasklet(TEST)().run()
    TEST()
    print('main b')
    # stackless.tasklet(reactor.run)().run()
    reactor.run()
    print('main c')