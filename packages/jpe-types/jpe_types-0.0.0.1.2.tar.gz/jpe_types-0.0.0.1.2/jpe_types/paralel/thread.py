"better Threads and Thread logging"
import threading
import logging

class Thread(threading.Thread):
    """an extended version of the std python thread

    see https://docs.python.org/3/library/threading.html for more information on threads

    but dont sublass the run method or the return data will be lost, instead  replace run with execute

    this threads adds
        - thread inheritance so we can track how the thread was creted mostly for debugging
        - thread returns the ability to return a tupple form a thread
    """
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        """This constructor should always be called with keyword arguments. Arguments are:

        *group* should be None; reserved for future extension when a ThreadGroup
        class is implemented.

        *target* is the callable object to be invoked by the run()
        method. Defaults to None, meaning nothing is called.

        *name* is the thread name. By default, a unique name is constructed of
        the form "Thread-N" where N is a small decimal number.

        *args* is the argument tuple for the target invocation. Defaults to ().

        *kwargs* is a dictionary of keyword arguments for the target
        invocation. Defaults to {}.

        If a subclass overrides the constructor, it must make sure to invoke
        the base class constructor (Thread.__init__()) before doing anything
        else to the thread.

        """
        threading.Thread.__init__(self, group=group, target=target, name=name, args=args, kwargs=kwargs, daemon=daemon)

        self.parent = threading.current_thread()
        """witch tread initiated this thread

        the thread, that initiated this one, for inharitance.
        currently mostly for logging
        """

        self._returnVal = None
        """the result of the treads Function

        used to store the return value of the function the thread ran
        unill join is called at witch point return val is returned
        """

    def run(self):
        """runs the thread and saves the result
        """
        self._returnVal = self.execute()
        
    
    def execute(self):
        """Method representing the thread's activity.

        You may override this method in a subclass. The standard run() method
        invokes the callable object passed to the object's constructor as the
        target argument, if any, with sequential and keyword arguments taken
        from the args and kwargs arguments, respectively.

        """
        try:
            if self._target:
                val = self._target(*self._args, **self._kwargs)
        finally:
            # Avoid a refcycle if the thread is running a function with
            # an argument that has a member that points to the thread.
            del self._target, self._args, self._kwargs
        return val
    
    def join(self):
        """Wait until the thread terminates.

        This blocks the calling thread until the thread whose join() method is
        called terminates -- either normally or through an unhandled exception
        or until the optional timeout occurs.

        When the timeout argument is present and not None, it should be a
        floating point number specifying a timeout for the operation in seconds
        (or fractions thereof). As join() always returns None, you must call
        isAlive() after join() to decide whether a timeout happened -- if the
        thread is still alive, the join() call timed out.

        When the timeout argument is not present or None, the operation will
        block until the thread terminates.

        A thread can be join()ed many times.

        join() raises a RuntimeError if an attempt is made to join the current
        thread as that would cause a deadlock. It is also an error to join() a
        thread before it has been started and attempts to do so raises the same
        exception.

        """
        threading.Thread.join(self)
        return self._returnVal

class LockableThread(Thread):
    """a combination of a lock and a thread

    makes it easyer to keep track of locks and threads and unlock, lock them
    """
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, lock=threading.Lock, *, daemon=None):
        """This constructor should always be called with keyword arguments. Arguments are:

        *group* should be None; reserved for future extension when a ThreadGroup
        class is implemented.

        *target* is the callable object to be invoked by the run()
        method. Defaults to None, meaning nothing is called.

        *name* is the thread name. By default, a unique name is constructed of
        the form "Thread-N" where N is a small decimal number.

        *args* is the argument tuple for the target invocation. Defaults to ().

        *kwargs* is a dictionary of keyword arguments for the target
        invocation. Defaults to {}.

        If a subclass overrides the constructor, it must make sure to invoke
        the base class constructor (Thread.__init__()) before doing anything
        else to the thread.

        """
        Thread.__init__(self, group=group, target=target, name=name, args=args, kwargs=kwargs, daemon=daemon)

        self.lock = lock()
        "the lock used to lock the thread"
    
    def aquire(self, blocking=True, timeout=-1):
        """Acquire a lock, blocking or non-blocking.

        When invoked without arguments: if this thread already owns the lock,
        increment the recursion level by one, and return immediately. Otherwise,
        if another thread owns the lock, block until the lock is unlocked. Once
        the lock is unlocked (not owned by any thread), then grab ownership, set
        the recursion level to one, and return. If more than one thread is
        blocked waiting until the lock is unlocked, only one at a time will be
        able to grab ownership of the lock. There is no return value in this
        case.

        When invoked with the blocking argument set to true, do the same thing
        as when called without arguments, and return true.

        When invoked with the blocking argument set to false, do not block. If a
        call without an argument would block, return false immediately;
        otherwise, do the same thing as when called without arguments, and
        return true.

        When invoked with the floating-point timeout argument set to a positive
        value, block for at most the number of seconds specified by timeout
        and as long as the lock cannot be acquired.  Return true if the lock has
        been acquired, false if the timeout has elapsed.

        """
        self.lock.acquire(blocking=blocking, timeout=timeout)
    
    def releace(self):
        """Release a lock, decrementing the recursion level.

        If after the decrement it is zero, reset the lock to unlocked (not owned
        by any thread), and if any other threads are blocked waiting for the
        lock to become unlocked, allow exactly one of them to proceed. If after
        the decrement the recursion level is still nonzero, the lock remains
        locked and owned by the calling thread.

        Only call this method when the calling thread owns the lock. A
        RuntimeError is raised if this method is called when the lock is
        unlocked.

        There is no return value.

        """
        self.lock.release()
        

class threadInharitanceFilter(logging.Filter):
    """logging filter for thread inheritance
    
    thread inheritance filter

    adds the ability to incorporate the inheritance of the thread from witch the log call originated
    like this
    
    >>> log = logging.getLogger(__name__)

    >>> syslog = logging.FileHandler("app.log")
    >>> log.addFilter(jpe_types.paralel.threadInharitanceFilter())

    >>> formatter = logging.Formatter('%(asctime)s in thread %(threadInharitace)s : %(message)s')
    >>> syslog.setFormatter(formatter)
    >>> log.setLevel(logging.DEBUG)
    >>> log.addHandler(syslog)
    """
    def filter(self, record):
        """generate str or thred inheritance
        
        crates a str containing the inheritance of the thread that called this function
        
        the str will be of type
        parentName.thisThreadName 
        
        add to the same for the parent etc"""
        record.threadInharitace = threadInharitanceFilter.getThreadName(threading.current_thread())
        return True
    
    @staticmethod
    def getThreadName(thread: threading.Thread):
        "recursivly compute the thread inheritance string"
        if isinstance(thread, Thread):
            return threadInharitanceFilter.getThreadName(thread.parent) +"."+thread.name
        return thread.name
