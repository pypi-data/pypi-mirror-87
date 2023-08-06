# eMail Requestor and Processor

# OVERVIEW

The general intention for this package is to automate searching and extracting text from emails and take actions using found values.

Currently there is support for searching in Gmail and sending HTTP requests prior or following email search. HTTP responses can also be searched and text found in either emails or responses can be dynamically substituted in subsequent HTTP requests.

The general flow looks like this:

1. Send the specified pre-search requests and extract values from the responses matching the given regular expressions
2. Search for emails matching the given query
3. Send the specified post-search requests and extract values from the responses matching the given regular expressions. Named placeholders in those requests are replaced with whatever has matched in emails or responses to pre-search requests.
4. Repeat: go back to 1. but now named placeholders in the pre-search requests are replaced with whatever has matched in emails or responses to post-search requests from the previous run.

An example usage is a password reset where you send a request to get a password reset, fetch the email and extract the reset code, send another request with the code in it.

# SETUP

# Installation

`pip3 install emrap`

# Creating an OAuth client

This package uses the Gmail OAuth2 API and requires credentials for an OAuth client, which you can create in the Google dev console (no GSuite needed). Then you need to authorize the app to access the emails of the target account (which can be any Google account, not just the one that owns the client credentials). Follow these steps:

1. Go to https://console.developers.google.com/apis/ and create a project.

<p><img src="images/create-project-1.png" width="100%"></p><hr>
<p><img src="images/create-project-2.png" width="70%"></p>

2. Go to https://console.developers.google.com/apis/credentials/consent and configure your app. Select the project if not selected, then choose between Internal or External app. Enter your app name and click on Save and continue several times until you finish that wizard and then Back to Dashboard.

<p><img src="images/oauth-consent-1.png" width="60%"></p><hr>
<p><img src="images/oauth-consent-2.png" width="60%"></p>

3. Go to https://console.developers.google.com/apis/credentials and create credentials of type OAuth client ID. Select Desktop App as the Application Type and name it.

<p><img src="images/create-creds-1.png" width="80%"></p><hr>
<p><img src="images/create-creds-2.png" width="80%"></p>

4. Click on the download button to download your credentials JSON file (does not work in Firefox). Rename it to credentials.json and put it in the same directory as the python client.

<p><img src="images/download-creds.png" width="100%"></p>

5. Go to https://console.developers.google.com/apis/library/gmail.googleapis.com?q=gmail api and enable to Gmail API.

<p><img src="images/enable-api.png" width="70%"></p>

6. Start the client which will open the OAuth consent screen in the browser. Follow the prompts to allow it, ignoring the warning it's unverified (you'll need to [get it verified](https://support.google.com/cloud/answer/9110914?hl=en) if you want to use it for non-testing purposes). You'll only need to authorise this once.

<p><img src="images/authorise-1.png" width="60%"></p><hr>
<p><img src="images/authorise-2.png" width="60%"></p><hr>
<p><img src="images/authorise-3.png" width="60%"></p><hr>
<p><img src="images/authorise-4.png" width="60%"></p><hr>
<p><img src="images/authorise-5.png" width="60%"></p>

# USAGE

Import `actions.HttpAutomator` and `run` it. See the demos for examples.

    usage: demo.py --creds-file CREDS_FILE [--token-file TOKEN_FILE]
                   [--query QUERY]
                   [--latest | --earliest | --range MIN MAX MIN MAX]
                   [--extracts directive:value [directive:value ...]
                   [directive:value [directive:value ...] ...]]
                   [--mime-type MIME_TYPE]
                   [--pre-search PRE_SEARCH [PRE_SEARCH ...] | --pre-search-async
                   PRE_SEARCH_ASYNC [PRE_SEARCH_ASYNC ...]]
                   [--post-search POST_SEARCH [POST_SEARCH ...] |
                   --post-search-async POST_SEARCH_ASYNC [POST_SEARCH_ASYNC ...]]
                   [--origin ORIGIN | --is-ssl IS_SSL] [--max-threads MAX_THREADS]
                   [--timeout TIMEOUT] [--min-wait MIN_WAIT] [--max-wait MAX_WAIT]
                   [--success-codes 2XX 3XX [2XX 3XX ...] | --fail-codes 4XX 5XX
                   [4XX 5XX ...]] [--retry [N]] [--no-verify] [--no-redirect]
                   [--proxy PROXY | --raw-socket] [--output OUTPUT]
                   [--repeat REPEAT] [--cache-file CACHE_FILE] [--verbose]
                   [--help]
    
    HTTP request automator with email search capability. An automation app to send
    HTTP requests which may generate an email, search in gmail and extract value,
    then optionally send more requests. Good for automarting password resets for
    example. It can be used just to search in emails. Supports dynamic text
    substitution with values extracted from previous responses or emails.
    
    Options related to authentication:
      --creds-file CREDS_FILE, -c CREDS_FILE
                            JSON file containing OAuth client credentials
                            (default: None)
      --token-file TOKEN_FILE, -t TOKEN_FILE
                            Previously saved token pickle file containing user
                            access token. If it doesn't exist it is created.
                            (default: None)
    
    Options related to filtering emails:
      --query QUERY, -q QUERY
                            Search query to filter emails. See
                            https://support.google.com/mail/answer/7190?hl=en.
                            (default: None)
      --latest, -l          Take only the latest email that matches. (default:
                            None)
      --earliest, -e        Take only the earliest email that matches. (default:
                            None)
      --range MIN MAX MIN MAX, -r MIN MAX MIN MAX
                            Take only emails number MIN to MAX (including) when
                            sorted in descending order by time. (default: None)
    
    Options related to extracting text from responses or
                email:
      --extracts directive:value [directive:value ...] [directive:value [directive:value ...] ...], -E directive:value [directive:value ...] [directive:value [directive:value ...] ...]
                            This specifies how and where to search for and extract
                            text and gives a name each extracted set of values
                            that can be used to substitute in HTTP requests. The
                            flag is given once per substitution definition and can
                            be given as many times as needed. It takes one or more
                            of the following directives (each as a separate
                            argument). There should not be a space around either
                            side of the colon unless intended, e.g. if the
                            'default' directive value should contain leading
                            spaces.
                                name:{unique name} HTTP requests can then use
                                    '{%name%}' which will be substituted by
                                    whatever matched name. By default the first
                                    match is taken, specify another one by
                            appending
                                    _N, e.g. '{%name_2%}' for the second one.
                                    The results table will list all matches along
                                    with the name regardless if any HTTP requests
                                    were supplied.
                                stages:pre|fetch|post fetch matches in emails and
                                    pre|post in pre- or post- email search. If not
                                    given, then all three stages are searched.
                                where:to_address,from_address,subject,raw_headers,
                            body,content,time
                                    Any of these can be given. to/from_address,
                                    subject and body apply to emails, raw_headers
                                    and content to HTTP responses, time applies to
                                    both. Defaults to search headers/subject and
                                    body/content.
                                regex:{arbitrary regex} Emails (stage fetch) are
                                    searched in descending order of time and
                                    requests (stages pre and post) are searched in
                                    order they were received.
                                regex_group:{number} Default is to take the whole
                                    match.
                                regex_flags:{flags} One letter per flag, e.g. IM
                            for
                                    case Insensitive and Multiline (see doc on
                                    python.re).
                                default:{arbitrary text} Text to use if regex
                                    doesn't match. Default is empty. (default:
                            None)
      --mime-type MIME_TYPE, -M MIME_TYPE
                            Preferred MIME type to search in. Only applies to
                            searching in multipart emails. (default: text/plain)
    
    Options related to sending requests. HTTP requests are
                read from text files as raw HTTP requests. Dynamic
                replacements are supported.:
      --pre-search PRE_SEARCH [PRE_SEARCH ...], -b PRE_SEARCH [PRE_SEARCH ...]
                            List of files to send as HTTP requests before email
                            search. Requests will be sent synchronously, one after
                            the other. (default: None)
      --pre-search-async PRE_SEARCH_ASYNC [PRE_SEARCH_ASYNC ...], -B PRE_SEARCH_ASYNC [PRE_SEARCH_ASYNC ...]
                            List of files to send as HTTP requests before email
                            search. Requests will be sent by concurrent threads.
                            (default: None)
      --post-search POST_SEARCH [POST_SEARCH ...], -a POST_SEARCH [POST_SEARCH ...]
                            List of files to send as HTTP requests after email
                            search. Executed for each email that matched the
                            search. Requests will be sent synchronously, one after
                            the other. (default: None)
      --post-search-async POST_SEARCH_ASYNC [POST_SEARCH_ASYNC ...], -A POST_SEARCH_ASYNC [POST_SEARCH_ASYNC ...]
                            List of files to send as HTTP requests after email
                            search. Executed for each email that matched the
                            search. Requests will be sent by concurrent threads.
                            (default: None)
      --origin ORIGIN, -O ORIGIN
                            Specify origin as {protocol}://{host}[:{port}]. This
                            overrides the Host header for all requests. (default:
                            None)
      --is-ssl IS_SSL       Use SSL. This overrides guessing from the port number
                            in the Host header for all requests. If no port is
                            present in the Host header, it defaults to HTTP on
                            port 80. (default: None)
      --max-threads MAX_THREADS
                            Maximum number of threads to start in async mode.
                            (default: 5)
      --timeout TIMEOUT, -T TIMEOUT
                            Timeout in seconds for response (default: None)
      --min-wait MIN_WAIT, -w MIN_WAIT
                            Min seconds to wait before sending next request.
                            (default: 0)
      --max-wait MAX_WAIT, -W MAX_WAIT
                            Max seconds to wait before sending next request.
                            (default: 0)
      --success-codes 2XX 3XX [2XX 3XX ...]
                            List of codes considered a success. X matches any
                            digit. (default: ['2XX'])
      --fail-codes 4XX 5XX [4XX 5XX ...]
                            List of codes considered a failure. X matches any
                            digit. (default: None)
      --retry [N], -R [N]   Retry N times on failed response. N defaults to 1 if
                            omitted. (default: 0)
      --no-verify           Do not verify SSL certificate and ignore warnings.
                            (default: True)
      --no-redirect         Do not follow redirections. (default: True)
      --proxy PROXY, -x PROXY
                            HTTP proxy to use in the format of {hostname}:{port}.
                            (default: None)
      --raw-socket, -S      Send the request content over a raw IPv4 socket.
                            Default is to use python's requests package which may
                            add some headers as well as change Content-Length.
                            Using a proxy, following redirections and SSL
                            verification is not supported when using raw sockets.
                            (default: False)
      --repeat REPEAT, -n REPEAT
                            How many times to repeat each
                            [request->]search[->request cycle]. Extracted text
                            from previous cycles is available for substitution.
                            (default: 1)
    
    Options related to displaying output:
      --output OUTPUT, -o OUTPUT
                            Text file to print summary table to. '-' means
                            standard output. (default: None)
    
    Global options :
      --cache-file CACHE_FILE, -C CACHE_FILE
                            Previously saved cache to restore from. If it doesn't
                            exist it is created. (default: None)
      --verbose, -v         Be verbose. Can be given multiple times to increase
                            verbosity. Twice is for debugging, three times is to
                            flood your screen with virtually useless information.
                            (default: None)
      --help, -h            Show this help message and exit.
