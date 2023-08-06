"""This is the main file that outlines the functionality of linkreaper"""
# Name: linkreaper
# Version: 0.1
# Author: Ruby Anne Bautista
# Description: A cli tool for finding dead links in local files given
# file path and searches through web pages for dead links given url
import json
import re
import certifi
import click
import urllib3


@click.group()
def main():
    """This main function"""


@main.command()
@click.argument("filepath", type=click.Path(exists=True, readable=True))
@click.option(
    "--secure",
    "-s",
    is_flag=True,
    help="change the http link schemes into https and output results",
)
@click.option(
    "--good", "-g", is_flag=True, help="Prints all the good links with 200 HTTP codes"
)
@click.option(
    "--bad",
    "-b",
    is_flag=True,
    help="Prints all the bad links with anything other than a 200 HTTP code",
)
@click.option(
    "--jsonout",
    "-j",
    is_flag=True,
    help="Prints out links and their responses in json format",
)
@click.option(
    "--alllinks",
    "-a",
    is_flag=True,
    default=True,
    help="Prints all the links and their status codes",
)
def readfile(filepath, secure, good, bad, jsonout):
    """Read from a local file and parse through the file for links"""
    try:
        with open(filepath, "r") as file:
            urls = collect_links(file.read(), secure)

    except PermissionError:
        click.echo("Invalid path- permission denied")

    else:
        # if the user inputted both good and bad, all the links will be displayed and
        # 'allinks' will override both options
        if bad and good:
            bad = False
            good = False

        if jsonout:
            output_json(urls, good, bad)
        else:
            output_codes(urls, good, bad)


@main.command()
@click.argument("url", default="")
@click.option(
    "--secure",
    "-s",
    is_flag=True,
    help="change the http link schemes into https and output results",
)
@click.option(
    "--good", "-g", is_flag=True, help="Prints all the good links with 200 HTTP codes"
)
@click.option(
    "--bad",
    "-b",
    is_flag=True,
    help="Prints all the bad links with anything other than a 200 HTTP code",
)
@click.option(
    "--jsonout",
    "-j",
    is_flag=True,
    help="Prints out links and their responses in json format",
)
# @click.option(
#     "--alllinks",
#     "-a",
#     is_flag=True,
#     default=True,
#     help="Prints all the links and their status codes",
# )
def readwebsite(url, secure, good, bad, jsonout):
    """Input a url to check page for dead links"""
    res = getwebsiteresponse(url)

    if res is None:
        click.echo("Url entered is not valid. Please input a different url.")
    else:

        urls = collect_links(res.data.decode("ISO-8859-1"), secure)

        # if the user inputted both g and b, all the links will be displayed and 'a'
        # will override both options
        if bad and good:
            bad = False
            good = False

        if jsonout:
            output_json(urls, good, bad)
        else:
            output_codes(urls, good, bad)


@main.command()
@click.argument("apiurl", default="")
def readtelescope(apiurl):
    """The command that reads from the telescope api and looks through the
    most recent blog posts for broken links"""

    res = getwebsiteresponse(apiurl)

    if res is None:
        click.echo("Url entered is not valid. Please input a different url.")
    else:

        posts = json.loads(res.data.decode("ISO-8859-1"))
        urls = collect_links(posts, api=True, baseurl=apiurl)

        for url in urls:
            click.echo(click.style("\nPost Link: " + url, fg="magenta"))
            res = getwebsiteresponse(url)
            if res is not None:
                posturls = collect_links(res.data.decode("ISO-8859-1"))
                output_codes(posturls)


def getwebsiteresponse(url):
    """Gets the websiteresponse"""
    try:
        pool = urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())
        # retrieve the html data from the given url
        res = pool.request("GET", url, timeout=5.0)
        pool.clear()
    except (urllib3.exceptions.MaxRetryError, urllib3.exceptions.LocationValueError):
        res = None

    return res


def output_codes(links, good_links=False, bad_links=False):
    """retrieves the http codes returned by the links,
    if good_links = True, bad_links = False automatically else,
    even if bad_links= False but good_links= False, it will still
    print bad links
    """
    # This is unclear and convoluted this needs to be fixed
    for link in links:

        try:
            pool = urllib3.PoolManager(
                num_pools=50, cert_reqs="CERT_REQUIRED", ca_certs=certifi.where()
            )
            response = pool.request("HEAD", link, timeout=5.0)

            if 299 >= response.status >= 200 and not bad_links:
                # successful responses
                click.echo(
                    click.style(
                        "GOOD      - Successful  : "
                        + str(response.status)
                        + " "
                        + link,
                        fg="green",
                    )
                )

            elif 399 >= response.status >= 300 and not good_links:
                # redirection message
                click.echo(
                    click.style(
                        "BAD       - Redirect    : "
                        + str(response.status)
                        + " "
                        + link,
                        fg="red",
                    )
                )

            elif 499 >= response.status >= 400 and not good_links:
                # client error responses
                click.echo(
                    click.style(
                        "BAD       - Client Error: "
                        + str(response.status)
                        + " "
                        + link,
                        fg="red",
                    )
                )

            elif 599 >= response.status >= 500 and not good_links:
                # server error response
                click.echo(
                    click.style(
                        "BAD       - Server Error: "
                        + str(response.status)
                        + " "
                        + link,
                        fg="red",
                    )
                )

        except urllib3.exceptions.HTTPError:
            # irregular responses- may return 200 but behaviour is irregular
            if not good_links:
                click.echo(
                    click.style("Irregular link          : " + link, fg="yellow")
                )


def output_json(links, good_links=False, bad_links=False):
    """Goes through a list of links, retrieves the response code and outputs the results in
    a json array with the url and corresponding code user has the option to display only
    certain types of links based on if the results were
    bad or good"""
    json_responses = []

    click.echo("Retrieving website responses...")
    # added progress bar to show the progress through each link
    with click.progressbar(links) as progbar:
        for link in progbar:
            website_response = {"url": link, "status": ""}
            try:
                pool = urllib3.PoolManager(
                    num_pools=50, cert_reqs="CERT_REQUIRED", ca_certs=certifi.where()
                )
                response = pool.request("HEAD", link, timeout=5.0)

                website_response["status"] = response.status

            except urllib3.exceptions.HTTPError:
                website_response["status"] = "irregular"

            # determine whether to add the response to the list depending on the
            # options the user inputted
            if (
                website_response["status"] != "irregular"
                and 300 > website_response["status"] <= 200
                and not bad_links
            ):
                json_responses.append(website_response)
            elif (
                website_response["status"] == "irregular"
                or website_response["status"] > 300
            ) and not good_links:
                json_responses.append(website_response)

    click.echo(json_responses)


def collect_links(raw_data, secure=False, api=False, baseurl=""):
    """parses through the raw data to find links and removes
    duplicates, if secure is true, parses through for http and
    turns them into https"""

    unique_urls = []

    if secure:  # if the user utilises the -s option

        urls_raw = re.findall(r"http?:[a-zA-Z0-9_.+-/#~%]+", raw_data)
        # get rid of duplicate links
        urls_raw = list(dict.fromkeys(urls_raw))

        for link in urls_raw:
            # changes the scheme of the links from http to https
            unique_urls.append(re.sub("http", "https", link))
    elif api:
        for postid in raw_data:
            unique_urls.append(baseurl + "/" + postid["id"])
    else:

        urls_raw = re.findall(r"https?:[a-zA-Z0-9_.+-/#~%]+", raw_data)
        # get rid of duplicate links
        unique_urls = list(dict.fromkeys(urls_raw))

    return unique_urls


if __name__ == "__main__":
    main()
