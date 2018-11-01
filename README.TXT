JARED DUNBAR

Current problems:

Cannot specify the listening port for the server directly, it will always be one less than the client it is connecting to. TODO: add a command line argument for that to work.

Client/Server crashes randomly when extreme noncompliance encountered. Not enough time to debug this problem, the simple solution would be to make it automatically retry with a try/catch loop, but I'm not going to do that because it's better for the user to understand what failed.
