""" Core module with cli """
import click
from pprint import pprint
from github import Github

@click.group()
def main():
    """
    Pygit is a cli tool for managing Github org users.
    It is a wrapper for the PyGitHub library.

    Example: pygit more-help --help
    """

@main.command()
@click.option("--helptext", is_flag=True, help="Print extra help")
def more_help(helptext):
    """ Various help options for usage information """
    result = "Use --help to view usage"
    if helptext:
        result = print_more_help()
    print(result)


@main.command("add-org-member", short_help="Add a user to the org")
@click.argument("github-user")
@click.argument("org-name")
@click.argument("personal-access-token")
def add_org_member(github_user, org_name, personal_access_token):
    """ Adds an existing Github user to the Organization """
    g = Github(personal_access_token)
    org = g.get_organization(org_name)
    userlist = g.search_users(github_user)
    org.add_to_members(userlist[0])


@main.command("get-org-members", short_help="Get a list of members in Org")
@click.argument("org-name")
@click.argument("personal-access-token")
def get_org_members(org_name, personal_access_token):
    """ Gets a list of members from provided organization """
    g = Github(personal_access_token)
    org = g.get_organization(org_name)
    members = org.get_members()
    for member in members:
        print(member)
    return members


@main.command("get-org-member", short_help="Get details of member")
@click.argument("org-name")
@click.argument("username")
@click.argument("personal-access-token")
def get_org_member(org_name, username, personal_access_token):
    """ Gets additional information about a member """
    g = Github(personal_access_token)
    member = g.get_user(username)
    print("ID:       ", member.id)
    print("Name:     ", member.name)
    print("URL:      ", member.repos_url)
    print("ORG_URL:  ", member.get_organization_membership(org_name))


@main.command("rm-org-member", short_help="Remove a member from the org")
@click.argument("github-user")
@click.argument("org-name")
@click.argument("personal-access-token")
def rm_org_member(github_user, org_name, personal_access_token):
    """ Removes an existing member from the Organization """
    g = Github(personal_access_token)
    org = g.get_organization(org_name)
    userlist = g.search_users(github_user)
    org.remove_from_membership(userlist[0])


def print_more_help():
    """ Prints help message """
    help_text = """
    This is some extra help TODO

    """
    return help_text

if __name__ == "__main__":
    main()

