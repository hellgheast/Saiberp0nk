"""
Input functions

Input functions are always called from the client (they handle server
input, hence the name).

This module is loaded by being included in the
`settings.INPUT_FUNC_MODULES` tuple.

All *global functions* included in this module are considered
input-handler functions and can be called by the client to handle
input.

An input function must have the following call signature:

    cmdname(session, *args, **kwargs)

Where session will be the active session and *args, **kwargs are extra
incoming arguments and keyword properties.

A special command is the "default" command, which is will be called
when no other cmdname matches. It also receives the non-found cmdname
as argument.

    default(session, cmdname, *args, **kwargs)

"""

# def oob_echo(session, *args, **kwargs):
#     """
#     Example echo function. Echoes args, kwargs sent to it.
#
#     Args:
#         session (Session): The Session to receive the echo.
#         args (list of str): Echo text.
#         kwargs (dict of str, optional): Keyed echo text
#
#     """
#     session.msg(oob=("echo", args, kwargs))
#
#
# def default(session, cmdname, *args, **kwargs):
#     """
#     Handles commands without a matching inputhandler func.
#
#     Args:
#         session (Session): The active Session.
#         cmdname (str): The (unmatched) command name
#         args, kwargs (any): Arguments to function.
#
#     """
#     pass

## Custom inputfuncs from the evelite-client

def get_map(session, *args, **kwargs):
    """Custom inputfunc to request the character's visible map."""
    mapstr = None
    if (obj := session.puppet) and obj.location:
        # this is where you fetch the map string for the character and their location
        # e.g. mapstr = obj.location.get_map(obj)
        pass

    if not mapstr:
        # no valid map so just don't do anything
        return

    # send the message
    session.msg(map=mapstr)


def get_channels(session, *args, **kwargs):
    """Request channel information for all channels the sender's account is subscribed to"""
    if session.account:
        from typeclasses.channels import Channel

        # this will send custom protocol-command messages to the session for each channel they're connected to
        for chan in Channel.objects.all():
            if chan.has_connection(session.account):
                session.msg(chaninfo=(chan.id, chan.key, True))
