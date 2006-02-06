# From http://www.faqts.com/knowledge_base/view.phtml/aid/4448

"""
Packages: files;miscellaneous
"""

'''
In all kinds of circumstances it would be very useful to call an
external filter to process some data, and read the results back in.
What I needed was something like popen(), only working for both
reading and writing.  However, such a thing is hard to write in a
simple-minded fashion because of deadlocks that occur when handling
more than several bytes of data.  Deadlocks can either be caused by
both programs waiting for not-yet-generated input, or (in my case) by
both their writes being blocked waiting for the other to read.

The usual choices are to:

a) Write a deadlock-free communication protocol and use it on both
   ends.  This is rarely a good solution, because the program that
   needs to be invoked is in most cases an external filter that knows
   nothing about our deadlock problems.

b) Use PTY's instead of pipes.  Many programmers prefer to avoid this
   path because of the added system resources that the PTY's require,
   and because of the increased complexity.

Given these choices, most people opt to use a temporary file and get
it over with.

However, discussing this problem with a colleague, he thought of a
third solution: break the circularity by using a process only for
reading and writing.  This can be done whenever reading and writing
are independent, i.e. when the data read from the subprocess does not
influence future writes to it.

The function below implements that idea.  Usage is something like:

rwpopen("""Some long string here...""", "sed", ["s/long/short/"])
  -> 'Some short string here...'

I've put the function to good use in a program I'm writing.  In
addition to getting rid of temporary files, the whole operation timed
faster than using a tmpfile (that was on a single-CPU machine).  The
function will, of course, work only under Unix and its lookalikes.
Additional information is embedded in the docstring and the comments.

I'd like to hear feedback.  Do other people find such a thing useful?
Is there a fundamental flaw or a possibility of a deadlock that I'm
missing?
'''

def rwpopen(input, command, args=[]):
    """Execute command with args, pipe input into it, and read it back.
    Return the result read from the command.

    Normally, when a process tries to write to a child process and
    read back its output, a deadlock condition can occur easily,
    either by both processes waiting for not-yet-generated input, or
    by both their writes() being blocked waiting for the other to
    read.

    This function prevents deadlocks by using separate processes for
    reading and writing, at the expense of an additional fork().  That
    way the process that writes to an exec'ed command and the process
    that reads from the command are fully independent, and no deadlock
    can occur.  The child process exits immediately after writing.

    More precisely: the current process (A) forks off a process B,
    which in turns forks off a process C.  While C does the usual
    dup,close,exec thing, B merely writes the data to the pipe and
    exits.  Independently of B, A reads C's response.  A deadlock
    cannot occur because A and B are independent of each other -- even
    if B's write() is stopped because it filled up the pipe buffer, A
    will happily keep reading C's output, and B's write() will be
    resumed shortly.
    """
    # XXX Redo this as a class, with overridable methods for reading
    # and writing.
    #
    # XXX Provide error-checking and propagating exceptions from child
    # to parent.  This would require either wait()ing on the child
    # (which is a bag of worms), or opening another pipe for
    # transmitting error messages or serialized exception objects.
    #
    # XXX This function expects the system to wait for the child upon
    # receiving SIGCHLD.  This should be the case on most systems as
    # long as SIGCHLD is handled by SIG_DFL.  If this is not the case,
    # zombies will remain.

    def safe_traceback():
        # Child processes catch exceptions so that they can exit using
        # os._exit() without fanfare.  They use this function to print
        # the traceback to stderr before dying.
        import traceback
        sys.stderr.write("Error in child process, pid %d.\n" %
                         os.getpid())
        sys.stderr.flush()
        traceback.print_exc()
        sys.stderr.flush()

    # It would be nice if Python provided a way to see if pipes are
    # bidirectional.  In that case, we could open only one pipe
    # instead of two, with p_readfd == p_writefd and c_readfd ==
    # c_writefd.
    p_readfd, c_writefd = os.pipe()
    c_readfd, p_writefd = os.pipe()
    if os.fork():
        # Parent
        for fd in (c_readfd, c_writefd, p_writefd):
            os.close(fd)
        # Convert the pipe fd to a file object, so we can use its
        # read() method to read all data.
        fp = os.fdopen(p_readfd, 'r')
        result = fp.read()
        fp.close()                      # Will close p_readfd.
        return result
    else:
        # Child
        try:
            if os.fork():
                # Still the same child
                os.write(p_writefd, input)
            else:
                # Grandchild
                try:
                    # Redirect the pipe to stdin.
                    os.close(0)
                    os.dup(c_readfd)
                    # Redirect stdout to the pipe.
                    os.close(1)
                    os.dup(c_writefd)
                    # Now close unneeded descriptors.
                    for fd in (c_readfd, c_writefd, p_readfd, p_writefd):
                        os.close(fd)
                    # Finally, execute the external command.
                    os.execvp(command, [command] + args)
                except:
                    safe_traceback()
                    os._exit(127)
        except:
            safe_traceback()
            os._exit(127)
        else:
            os._exit(0)
